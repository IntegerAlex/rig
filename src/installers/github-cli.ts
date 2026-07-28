import type { CommandRunner } from "../utils/command-runner.js";
import type { SetupLogger } from "../utils/logger.js";
import type { InstallerResult } from "../types.js";
import { blue } from "../utils/ansi.js";

export function createGitHubCLIInstaller(runner: CommandRunner, logger: SetupLogger) {
  function checkInstalled(): boolean {
    try {
      const r = runner.run(["gh", "--version"], { check: false, capture: true });
      return (r.status ?? 1) === 0;
    } catch {
      return false;
    }
  }

  async function doInstall(): Promise<InstallerResult> {
    try {
      process.stdout.write(`${blue("\u2139")} Installing GitHub CLI\n`);

      runner.run(["mkdir", "-p", "/etc/apt/keyrings"], { sudo: true });
      const keyringUrl = "https://cli.github.com/packages/githubcli-archive-keyring.gpg";
      runner.run(
        ["bash", "-c", `wget -qO- ${keyringUrl} | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null`],
        { description: "Downloading GitHub CLI keyring" },
      );
      runner.run(["chmod", "go+r", "/etc/apt/keyrings/githubcli-archive-keyring.gpg"], { sudo: true });

      const arch = runner.run(["dpkg", "--print-architecture"], { capture: true }).stdout?.toString().trim() || "amd64";
      const repoLine = `deb [arch=${arch} signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main`;
      runner.run(
        ["bash", "-c", `echo '${repoLine}' | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null`],
        { description: "Adding GitHub CLI repository" },
      );

      runner.run(["apt", "update"], { sudo: true });
      runner.run(["apt", "install", "-y", "gh"], { sudo: true, description: "Installing GitHub CLI" });

      return { success: true, message: "GitHub CLI installed successfully" };
    } catch (e) {
      return { success: false, message: "Failed to install GitHub CLI", error: String(e) };
    }
  }

  return { is_installed: checkInstalled, install: doInstall };
}
