import type { CommandRunner, RunOptions } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";

interface AptPackageOpts {
  packageName: string;
  checkCommand?: string;
  versionArgs?: string[];
  displayName?: string;
  successMessage?: string;
}

export function createAptPackageInstaller(
  runner: CommandRunner,
  logger: SetupLogger,
  opts: AptPackageOpts,
) {
  const packageName = opts.packageName;
  const checkCommand = opts.checkCommand ?? opts.packageName;
  const versionArgs = opts.versionArgs ?? ["--version"];
  const displayName = opts.displayName ?? opts.packageName;
  const successMessage = opts.successMessage ?? `${displayName} installed successfully`;

  function checkInstalled(): boolean {
    try {
      const r = runner.run(["which", checkCommand], { check: false, capture: true });
      if ((r.status ?? 1) !== 0) return false;
      const rr = runner.run([checkCommand, ...versionArgs], { check: false, capture: true });
      return (rr.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      runner.run(["apt", "install", "-y", packageName], { sudo: true, description: `Installing ${displayName}` });
      return { success: true, message: successMessage };
    } catch (e) {
      return { success: false, message: `Failed to install ${displayName}`, error: String(e) };
    }
  }

  return {
    is_installed: checkInstalled,
    install: doInstall,
  };
}
