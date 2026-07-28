import { existsSync } from "node:fs";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createCertbotInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "certbot"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["certbot", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing Certbot\n`);

      runner.run(
        ["apt", "install", "-y", "python3", "python3-dev", "python3-venv", "libaugeas-dev", "gcc"],
        { sudo: true, description: "Installing Certbot dependencies" },
      );

      runner.run(["mkdir", "-p", "/opt/certbot"], { sudo: true });

      const certbotVenv = "/opt/certbot/bin/python";
      if (!existsSync(certbotVenv)) {
        runner.run(
          ["python3", "-m", "venv", "/opt/certbot"],
          { sudo: true, description: "Creating Certbot virtual environment" },
        );
      }

      runner.run(
        ["/opt/certbot/bin/pip", "install", "--upgrade", "pip"],
        { sudo: true, description: "Upgrading pip" },
      );

      runner.run(
        ["/opt/certbot/bin/pip", "install", "certbot", "certbot-nginx"],
        { sudo: true, description: "Installing Certbot" },
      );

      runner.run(
        ["ln", "-sf", "/opt/certbot/bin/certbot", "/usr/bin/certbot"],
        { sudo: true, description: "Creating certbot symlink" },
      );

      return { success: true, message: "Certbot installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install Certbot", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
