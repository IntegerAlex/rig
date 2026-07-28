import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createUVInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "uv"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["uv", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing uv\n`);
      runner.run(
        ["bash", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
        { description: "Installing uv" },
      );
      return { success: true, message: "uv installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install uv", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
