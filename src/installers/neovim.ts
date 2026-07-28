import { unlinkSync } from "node:fs";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createNeovimInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "nvim"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["nvim", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    let tmpPath = "";
    try {
      process.stdout.write(`${blue("\u2139")} Installing Neovim\n`);

      const tmpDir = mkdtempSync(join(tmpdir(), "nvim-"));
      tmpPath = join(tmpDir, "nvim.tar.gz");

      const url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz";
      runner.run(["curl", "-L", url, "-o", tmpPath], { description: "Downloading Neovim" });

      runner.run(["rm", "-rf", "/opt/nvim-linux-x86_64"], { sudo: true });
      runner.run(["tar", "-C", "/opt", "-xzf", tmpPath], { sudo: true, description: "Extracting Neovim" });
      runner.run(
        ["ln", "-sf", "/opt/nvim-linux-x86_64/bin/nvim", "/usr/local/bin/nvim"],
        { sudo: true, description: "Creating symlink" },
      );

      return { success: true, message: "Neovim installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install Neovim", error: String(e) };
    } finally {
      if (tmpPath) {
        try { unlinkSync(tmpPath); } catch {}
      }
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
