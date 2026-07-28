import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createImageViewerInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "aiv"], { check: false, capture: true });
      if ((r.status ?? 1) === 0) return true;
      const rr = runner.run(["which", "advance-image-viewer"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing Advance Image Viewer\n`);
      runner.run(
        ["bash", "-c", "curl -fsSL https://advance-image-viewer.gossorg.in | bash"],
        { description: "Installing Advance Image Viewer" },
      );
      return { success: true, message: "Advance Image Viewer installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install Advance Image Viewer", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
