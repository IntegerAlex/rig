import { homedir } from "node:os";
import { join } from "node:path";
import { existsSync } from "node:fs";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue, yellow } from "../utils/ansi.js";

export function createNodeJSInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    const nvmDir = join(homedir(), ".nvm");
    return existsSync(join(nvmDir, "nvm.sh"));
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing Node.js via nvm\n`);
      runner.run(
        ["bash", "-c", "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash"],
        { description: "Installing nvm" },
      );
      process.stdout.write(`${yellow("\u26a0")} Please run: source ~/.bashrc (or ~/.zshrc) to use nvm\n`);
      return { success: true, message: "Node.js (nvm) installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install Node.js", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
