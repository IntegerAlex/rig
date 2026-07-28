import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createBTopInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "btop"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["btop", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch { return false; }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing btop\n`);
      runner.run(["apt", "install", "-y", "btop"], { sudo: true, description: "Installing btop" });
      return { success: true, message: "btop installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install btop", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
