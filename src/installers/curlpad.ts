import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createCurlpadInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "curlpad"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["curlpad", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing curlpad\n`);
      runner.run(
        ["bash", "-c", "curl -fsSL curlpad-installer.gossorg.in/install.sh | bash"],
        { description: "Installing curlpad" },
      );
      return { success: true, message: "curlpad installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install curlpad", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
