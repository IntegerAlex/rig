import { homedir } from "node:os";
import { join } from "node:path";
import { existsSync } from "node:fs";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

const MIN_NODE_MAJOR = 24;
const DEFAULT_NODE_MAJOR = 24;

export function createPNPMInstaller(runner: CommandRunner, logger: SetupLogger) {
  function getNodeMajor(): number | null {
    try {
      const r = runner.run(["which", "node"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return null;
      const rr = runner.run(["node", "--version"], { check: false, capture: true });
      if ((rr.status ?? 1) !== 0 || !rr.stdout) return null;
      const v = rr.stdout.toString().trim();
      const major = parseInt(v.startsWith("v") ? v.substring(1) : v, 10);
      return isNaN(major) ? null : major;
    } catch {
      return null;
    }
  }

  function hasNvm(): boolean {
    const nvmDir = join(homedir(), ".nvm");
    return existsSync(join(nvmDir, "nvm.sh"));
  }

  function enableViaNvm(nodeMajor: number): void {
    const cmd =
      `export NVM_DIR="$HOME/.nvm"; ` +
      `[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"; ` +
      `nvm install ${nodeMajor}; nvm use ${nodeMajor}; corepack enable pnpm; `;
    runner.run(["bash", "-lc", cmd], { description: `Installing/using Node ${nodeMajor} via nvm and enabling pnpm` });
  }

  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", "pnpm"], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run(["pnpm", "--version"], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Enabling pnpm\n`);

      const nodeMajor = getNodeMajor();
      let corepackAvailable = false;
      try {
        const r = runner.run(["which", "corepack"], { check: false, capture: true });
        corepackAvailable = (r.status ?? 1) === 0;
      } catch {}

      if (!corepackAvailable || nodeMajor === null || nodeMajor < MIN_NODE_MAJOR) {
        if (!hasNvm()) {
          return {
            success: false,
            message: "Failed to enable pnpm (corepack requires Node 24+)",
            error: "corepack/node not available and nvm not found. Install Node.js (via nvm) first, then rerun pnpm.",
          };
        }
        enableViaNvm(DEFAULT_NODE_MAJOR);
      } else {
        runner.run(["corepack", "enable", "pnpm"], { description: "Enabling pnpm via corepack" });
      }

      return { success: true, message: "pnpm enabled successfully" };
    } catch (e) {
      return { success: false, message: "Failed to enable pnpm", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
