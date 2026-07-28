import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { PackageManagerError } from "../errors.js";

export function createBootstrapInstaller(runner: CommandRunner, logger: SetupLogger) {
  async function doInstall(): Promise<InstallerResult> {
    try {
      console.log("ℹ Initializing system");
      runner.run(["apt", "update"], { sudo: true, description: "Updating package lists" });
      runner.run(
        ["apt", "install", "-y", "ca-certificates", "curl", "wget", "gnupg", "lsb-release", "lsof"],
        { sudo: true, description: "Installing essential packages" },
      );
      return { success: true, message: "System initialized successfully" };
    } catch (e) {
      if (e instanceof PackageManagerError) throw e;
      throw new PackageManagerError("Failed to initialize system with essential packages");
    }
  }

  return { install: doInstall };
}
