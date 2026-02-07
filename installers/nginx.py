# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""nginx installer."""

import os
import shutil
import tempfile

from utils.base import BaseInstaller
from utils.types import InstallerResult
from utils.errors import PackageManagerError, InstallationError

# Basic webserver: static files from /var/www/html
NGINX_WEBSERVER_CONF = """# Basic webserver - rig
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
"""

# Basic reverse proxy: edit server_name and proxy_pass for your app
NGINX_REVERSE_PROXY_CONF = """# Basic reverse proxy - rig
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
"""


class NginxInstaller(BaseInstaller):
    """Install nginx with basic webserver and reverse-proxy configs."""
    
    SITES_AVAILABLE = "/etc/nginx/sites-available"
    RIG_WEBSERVER = "rig-webserver"
    RIG_REVERSE_PROXY = "rig-reverse-proxy"
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("nginx"):
            return False
        
        try:
            result = self.runner.run(["nginx", "-v"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def _write_site_config(self, filename: str, content: str) -> bool:
        """Write a config file to sites-available only if it does not exist. Returns True if written, False if skipped."""
        path = os.path.join(self.SITES_AVAILABLE, filename)
        result = self.runner.run(
            ["test", "-f", path],
            sudo=True,
            check=False,
            capture_output=True,
        )
        if result.returncode == 0:
            return False
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            try:
                f.write(content)
                f.flush()
                self.runner.run(
                    ["cp", f.name, path],
                    sudo=True,
                    description=f"Writing {filename}",
                )
            finally:
                os.unlink(f.name)
        return True
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing nginx")
            
            self.runner.run(
                ["apt", "install", "-y", "nginx"],
                sudo=True,
                description="Installing nginx"
            )
            
            self.runner.run(
                ["systemctl", "enable", "nginx"],
                sudo=True,
                description="Enabling nginx service"
            )
            
            self.console.print("[blue]ℹ[/blue] Adding basic webserver and reverse-proxy configs")
            wrote_webserver = self._write_site_config(self.RIG_WEBSERVER, NGINX_WEBSERVER_CONF)
            wrote_reverse_proxy = self._write_site_config(self.RIG_REVERSE_PROXY, NGINX_REVERSE_PROXY_CONF)
            if not wrote_webserver and not wrote_reverse_proxy:
                self.console.print("[dim]Configs already present, skipping.[/dim]")
            self.console.print(
                "[dim]Configs: /etc/nginx/sites-available/rig-webserver, "
                "rig-reverse-proxy (enable and reload nginx to use)[/dim]"
            )
            
            return InstallerResult(True, "nginx installed with basic webserver and reverse-proxy configs")
        except (PackageManagerError, InstallationError):
            # Re-raise custom errors as-is
            raise
        except Exception as e:
            # Convert other exceptions to installation errors with helpful suggestions
            raise InstallationError(
                "Failed to install nginx web server",
                "nginx",
                [
                    "Check your internet connection",
                    "Ensure you have sudo privileges",
                    "Try: sudo apt update && sudo apt install nginx"
                ]
            ) from e

