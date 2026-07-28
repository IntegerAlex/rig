import { readFileSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { existsSync } from "node:fs";
import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue, yellow, bold, cyan, dim } from "../utils/ansi.js";

export function createSSHKeyInstaller(runner: CommandRunner, logger: SetupLogger) {
  function displayPublicKey(pubKeyPath: string): void {
    try {
      if (existsSync(pubKeyPath)) {
        const publicKey = readFileSync(pubKeyPath, "utf8").trim();
        process.stdout.write("\n");
        process.stdout.write(`${bold(cyan("Your SSH public key:"))}\n`);
        process.stdout.write(`${dim(publicKey)}\n`);
        process.stdout.write("\n");
        process.stdout.write(`${dim("Add this key to GitHub, GitLab, or your server's ~/.ssh/authorized_keys")}\n`);
      }
    } catch (e) {
      process.stdout.write(`${yellow("\u26a0")} Could not read public key: ${e}\n`);
    }
  }

  function checkInstalled(): boolean {
    const sshDir = join(homedir(), ".ssh");
    return existsSync(join(sshDir, "bot")) && existsSync(join(sshDir, "bot.pub"));
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Generating SSH key pair\n`);

      const sshDir = join(homedir(), ".ssh");
      mkdirSync(sshDir, { recursive: true, mode: 0o700 });

      const botKey = join(sshDir, "bot");
      const botPub = join(sshDir, "bot.pub");

      if (existsSync(botKey) && existsSync(botPub)) {
        process.stdout.write(`${yellow("\u26a0")} SSH key already exists, skipping generation\n`);
        displayPublicKey(botPub);
        return { success: true, message: "SSH key already exists" };
      }

      runner.run(
        ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", botKey, "-N", "", "-q"],
        { description: "Generating SSH key pair" },
      );

      try { process.stdout.write(`${dim("Setting permissions...")}\n`); } catch {}

      displayPublicKey(botPub);

      return { success: true, message: "SSH key generated successfully" };
    } catch (e) {
      return { success: false, message: "Failed to generate SSH key", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
