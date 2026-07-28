import type { InstallerResult } from "../types.js";
import { bold, dim, cyan, brightBlue } from "../utils/ansi.js";

const hints: Record<string, string> = {
  "GitHub CLI": "Run 'gh auth login' to authenticate with GitHub.",
  git: "Configure your identity: git config --global user.name/email.",
  "SSH Key": "Add '~/.ssh/id_rsa.pub' to GitHub or your servers.",
  "Node.js": "Open a new shell so nvm is loaded, then run 'node -v'.",
  pnpm: "Run 'pnpm -v' to verify pnpm is available via corepack.",
  Neovim: "Run 'nvim' and start customizing your config.",
  nginx: "Edit 'rig-webserver' or 'rig-reverse-proxy' in /etc/nginx/sites-available, enable, then 'sudo nginx -t && sudo systemctl reload nginx'.",
  UFW: "Enable firewall: sudo ufw enable; check with: sudo ufw status verbose.",
  Fail2ban: "Check jails after some time: sudo fail2ban-client status.",
  zsh: "Log out and back in for the default shell change to take effect.",
  podman: "Run 'podman info' to confirm rootless containers work.",
  fastfetch: "Run 'fastfetch' to view your system summary.",
};

export function showNextSteps(results: Array<{ name: string; result: InstallerResult }>): void {
  const steps: Array<[string, string]> = [];
  for (const { name, result } of results) {
    if (result.success && hints[name]) {
      steps.push([name, hints[name]]);
    }
  }

  if (steps.length === 0) return;

  process.stdout.write("\n");
  process.stdout.write(`${brightBlue("┌─")} ${brightBlue("🧭")} ${bold(brightBlue("Next steps"))} ${brightBlue("─".repeat(35))}${brightBlue("┐")}\n`);
  process.stdout.write(`${dim("│")} ${cyan("Tool")}${" ".repeat(10)}${dim("│")} ${bold("Suggestion")}${" ".repeat(37)}${dim("│")}\n`);
  process.stdout.write(`${dim("│")}${"─".repeat(14)}${dim("│")}${"─".repeat(46)}${dim("│")}\n`);

  for (const [name, hint] of steps) {
    const nameDisplay = name.length > 10 ? name.substring(0, 10) + "..." : name;
    process.stdout.write(`${dim("│")} ${bold(nameDisplay.padEnd(12))}${dim("│")} ${hint.substring(0, 44).padEnd(44)}${dim("│")}\n`);
  }

  process.stdout.write(`${brightBlue("└")}${brightBlue("─".repeat(62))}${brightBlue("┘")}\n`);
  process.stdout.write("\n");
}
