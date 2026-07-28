import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createVRMSInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "vrms"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["vrms", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch { return false; }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing vrms\n`);
      runner.run(["apt", "install", "-y", "vrms"], { sudo: true, description: "Installing vrms" });
      return { success: true, message: "vrms installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install vrms", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
