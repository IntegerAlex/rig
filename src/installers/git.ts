import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createGitInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "git"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["git", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch { return false; }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing git\n`);
      runner.run(["apt", "install", "-y", "git"], { sudo: true, description: "Installing git" });
      return { success: true, message: "git installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install git", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
