import { readFileSync } from "node:fs";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue, yellow } from "../utils/ansi.js";
import { createAptPackageInstaller } from "./apt-package.js";

export function createZshInstaller(runner: CommandRunner, logger: SetupLogger) {
  const base = createAptPackageInstaller(runner, logger, {
    packageName: "zsh",
    successMessage: "zsh installed and set as default shell",
  });

  function checkInstalled(): boolean {
    if (!base.is_installed()) return false;
    try {
      const passwd = readFileSync("/etc/passwd", "utf8");
      const username = process.env["USER"] || process.env["USERNAME"] || "";
      if (username) {
        for (const line of passwd.split("\n")) {
          if (line.startsWith(`${username}:`)) {
            const shell = line.split(":")[line.split(":").length - 1]?.trim() || "";
            return shell.endsWith("/zsh");
          }
        }
      }
    } catch {}
    return true;
  }

  async function doInstall(): Promise<InstallerResult> {
    const result = await base.install();
    if (!result.success) return result;

    try {
      process.stdout.write(`${blue("\u2139")} Setting zsh as default shell\n`);
      let zshPath = "/usr/bin/zsh";
      try {
        const r = runner.run(["which", "zsh"], { capture: true });
        zshPath = r.stdout?.toString().trim() || zshPath;
      } catch {}
      runner.run(["chsh", "-s", zshPath], { description: "Setting zsh as default shell" });
      process.stdout.write(`${yellow("\u26a0")} Default shell changed to zsh. The change will take effect after you log out and log back in.\n`);
    } catch (e) {
      return { success: false, message: "zsh installed but failed to set as default shell", error: String(e) };
    }
    return { success: true, message: "zsh installed and set as default shell" };
  }

  return { is_installed: checkInstalled, install: doInstall };
}
