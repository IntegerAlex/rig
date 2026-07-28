import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue, yellow } from "../utils/ansi.js";

export function createUFWInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "ufw"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["ufw", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing UFW\n`);

      runner.run(["apt", "install", "-y", "ufw"], { sudo: true, description: "Installing UFW" });
      runner.run(["ufw", "default", "deny", "incoming"], { sudo: true, description: "Setting default deny incoming" });
      runner.run(["ufw", "default", "allow", "outgoing"], { sudo: true, description: "Setting default allow outgoing" });
      runner.run(["ufw", "allow", "22/tcp"], { sudo: true, description: "Allowing SSH" });
      runner.run(["ufw", "allow", "80"], { sudo: true, description: "Allowing HTTP" });
      runner.run(["ufw", "allow", "443"], { sudo: true, description: "Allowing HTTPS" });

      process.stdout.write(`${yellow("\u26a0")} UFW configured but NOT enabled. Enable manually with: sudo ufw enable\n`);

      return { success: true, message: "UFW installed and configured (not enabled)" };
    } catch (e) {
      return { success: false, message: "Failed to install UFW", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
