import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createChkrootkitInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "chkrootkit"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["chkrootkit", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch { return false; }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing chkrootkit\n`);
      runner.run(["apt", "install", "-y", "chkrootkit"], { sudo: true, description: "Installing chkrootkit" });
      return { success: true, message: "chkrootkit installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install chkrootkit", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
