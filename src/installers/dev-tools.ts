import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createDevToolsInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    const keyTools = ["gcc", "make", "cmake", "pkg-config"];
    let count = 0;
    for (const tool of keyTools) {
      try {
        const r = runner.run(["which", tool], { check: false, capture: true });
        if ((r.status ?? 1) === 0) count++;
      } catch {}
    }
    return count >= 3;
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing developer tools\n`);
      const packages = ["openssl", "clangd", "build-essential", "pkg-config", "cmake", "git"];
      runner.run(
        ["apt", "install", "-y", ...packages],
        { sudo: true, description: "Installing developer tools" },
      );
      return { success: true, message: "Developer tools installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install developer tools", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
