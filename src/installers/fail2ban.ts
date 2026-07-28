import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createFail2banInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "fail2ban-client"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["fail2ban-client", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing Fail2ban\n`);
      runner.run(["apt", "install", "-y", "fail2ban"], { sudo: true, description: "Installing Fail2ban" });
      return { success: true, message: "Fail2ban installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install Fail2ban", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
