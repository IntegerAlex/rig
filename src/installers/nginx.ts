import { writeFileSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue, dim } from "../utils/ansi.js";
import { InstallationError, PackageManagerError } from "../errors.js";

const NGINX_WEBSERVER_CONF = `# Basic webserver - rig
# Enable: sudo ln -sf /etc/nginx/sites-available/rig-webserver /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx
server {
    listen 80;
    listen [::]:80;
    server_name _;
    root /var/www/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
`;

const NGINX_REVERSE_PROXY_CONF = `# Basic reverse proxy - rig
# Enable: sudo ln -sf /etc/nginx/sites-available/rig-reverse-proxy /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx
# Edit server_name and proxy_pass to match your app
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
`;

const SITES_AVAILABLE = "/etc/nginx/sites-available";
const RIG_WEBSERVER = "rig-webserver";
const RIG_REVERSE_PROXY = "rig-reverse-proxy";

export function createNginxInstaller(runner: CommandRunner, logger: SetupLogger) {
  function writeSiteConfig(filename: string, content: string): boolean {
    const path = join(SITES_AVAILABLE, filename);
    const r = runner.run(["test", "-f", path], { sudo: true, check: false, capture: true });
    if (r.status === 0) return false;

    const tmpDir = mkdtempSync(join(tmpdir(), "nginx-"));
    const tmpFile = join(tmpDir, filename);
    writeFileSync(tmpFile, content, "utf8");
    try {
      runner.run(["cp", tmpFile, path], { sudo: true, description: `Writing ${filename}` });
    } finally {
      try { unlinkSync(tmpFile); } catch {}
    }
    return true;
  }

  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "nginx"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["nginx", "-v"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing nginx\n`);

      runner.run(["apt", "install", "-y", "nginx"], { sudo: true, description: "Installing nginx" });
      runner.run(["systemctl", "enable", "nginx"], { sudo: true, description: "Enabling nginx service" });

      process.stdout.write(`${blue("\u2139")} Adding basic webserver and reverse-proxy configs\n`);
      const wroteWs = writeSiteConfig(RIG_WEBSERVER, NGINX_WEBSERVER_CONF);
      const wroteRp = writeSiteConfig(RIG_REVERSE_PROXY, NGINX_REVERSE_PROXY_CONF);
      if (!wroteWs && !wroteRp) {
        process.stdout.write(`${dim("Configs already present, skipping.")}\n`);
      }
      process.stdout.write(`${dim("Configs: /etc/nginx/sites-available/rig-webserver, rig-reverse-proxy (enable and reload nginx to use)")}\n`);

      return { success: true, message: "nginx installed with basic webserver and reverse-proxy configs" };
    } catch (e) {
      if (e instanceof PackageManagerError || e instanceof InstallationError) throw e;
      throw new InstallationError(
        "Failed to install nginx web server",
        "nginx",
        ["Check your internet connection", "Ensure you have sudo privileges", "Try: sudo apt update && sudo apt install nginx"],
      );
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
