import type { InstallerResult } from "./types.js";
import { SetupLogger, CommandRunner, updateShellConfig } from "./utils/index.js";
import {
  createBootstrapInstaller,
  createGitHubCLIInstaller,
  createUVInstaller,
  createNodeJSInstaller,
  createPNPMInstaller,
  createNeovimInstaller,
  createBTopInstaller,
  createNginxInstaller,
  createCertbotInstaller,
  createUFWInstaller,
  createFail2banInstaller,
  createImageViewerInstaller,
  createCurlpadInstaller,
  createDevToolsInstaller,
  createSSHKeyInstaller,
  createFastfetchInstaller,
  createPodmanInstaller,
  createZshInstaller,
  createGitInstaller,
  createRkhunterInstaller,
  createChkrootkitInstaller,
  createVRMSInstaller,
} from "./installers/index.js";
import { showWelcome } from "./ui/welcome.js";
import { showSummary } from "./ui/summary.js";
import { showNextSteps } from "./ui/next-steps.js";
import { confirm, askChoice } from "./utils/prompt.js";
import { RigError } from "./errors.js";
import { Spinner, bold, green, red, yellow, cyan, dim, brightCyan } from "./utils/ansi.js";

interface InstallerEntry {
  name: string;
  install: () => Promise<InstallerResult>;
  description: string;
}

const BLACKLIST_CHECK: Record<string, string[]> = {
  "Bootstrap": [],
  "GitHub CLI": ["gh"],
  "uv": ["uv"],
  "Node.js": [],
  "pnpm": ["pnpm"],
  "Neovim": ["nvim"],
  "btop": ["btop"],
  "nginx": ["nginx"],
  "Certbot": ["certbot"],
  "UFW": ["ufw"],
  "Fail2ban": ["fail2ban-client"],
  "Image Viewer": ["aiv"],
  "curlpad": ["curlpad"],
  "Developer Tools": [],
  "SSH Key": [],
  "fastfetch": ["fastfetch"],
  "podman": ["podman"],
  "zsh": ["zsh"],
  "git": ["git"],
  "rkhunter": ["rkhunter"],
  "chkrootkit": ["chkrootkit"],
  "vrms": ["vrms"],
};

const DEV_PRESET = new Set([
  "GitHub CLI", "uv", "Node.js", "pnpm", "Neovim",
  "Developer Tools", "SSH Key", "fastfetch", "git", "zsh", "podman", "btop",
]);

const SERVER_PRESET = new Set([
  "GitHub CLI", "Node.js", "pnpm", "nginx", "Certbot",
  "UFW", "Fail2ban", "SSH Key", "fastfetch", "git", "rkhunter", "chkrootkit",
]);

const SECURITY_PRESET = new Set(["UFW", "Fail2ban", "rkhunter", "chkrootkit", "vrms"]);

function getPreset(choice: string): Set<string> {
  if (choice === "dev") return DEV_PRESET;
  if (choice === "server") return SERVER_PRESET;
  if (choice === "security") return SECURITY_PRESET;
  return new Set();
}

export class SetupManager {
  private logger: SetupLogger;
  private runner: CommandRunner;
  private installOptions: InstallerEntry[];
  private results: Array<{ name: string; result: InstallerResult }> = [];
  private startTime = 0;

  constructor() {
    this.logger = new SetupLogger();
    this.runner = new CommandRunner(this.logger);
    this.installOptions = this.createInstallOptions();
  }

  private checkToolInstalled(name: string): boolean {
    const bins = BLACKLIST_CHECK[name];
    if (!bins || bins.length === 0) return false;
    for (const bin of bins) {
      try {
        const r = this.runner.run(["which", bin], { check: false, capture: true });
        if ((r.status ?? 1) === 0) return true;
      } catch {}
    }
    return false;
  }

  private createInstallOptions(): InstallerEntry[] {
    const bootstrap = createBootstrapInstaller(this.runner, this.logger);
    const gh = createGitHubCLIInstaller(this.runner, this.logger);
    const uv = createUVInstaller(this.runner, this.logger);
    const node = createNodeJSInstaller(this.runner, this.logger);
    const pnpm = createPNPMInstaller(this.runner, this.logger);
    const nvim = createNeovimInstaller(this.runner, this.logger);
    const btop = createBTopInstaller(this.runner, this.logger);
    const nginx = createNginxInstaller(this.runner, this.logger);
    const cert = createCertbotInstaller(this.runner, this.logger);
    const ufw = createUFWInstaller(this.runner, this.logger);
    const f2b = createFail2banInstaller(this.runner, this.logger);
    const img = createImageViewerInstaller(this.runner, this.logger);
    const curl = createCurlpadInstaller(this.runner, this.logger);
    const dev = createDevToolsInstaller(this.runner, this.logger);
    const ssh = createSSHKeyInstaller(this.runner, this.logger);
    const fast = createFastfetchInstaller(this.runner, this.logger);
    const pod = createPodmanInstaller(this.runner, this.logger);
    const z = createZshInstaller(this.runner, this.logger);
    const g = createGitInstaller(this.runner, this.logger);
    const rk = createRkhunterInstaller(this.runner, this.logger);
    const chk = createChkrootkitInstaller(this.runner, this.logger);
    const vrms = createVRMSInstaller(this.runner, this.logger);

    function entry(name: string, inst: { install: () => Promise<InstallerResult> }, desc: string): InstallerEntry {
      return { name, install: inst.install, description: desc };
    }

    return [
      entry("Bootstrap", bootstrap, "Initialize system with essential packages"),
      entry("GitHub CLI", gh, "Install GitHub CLI (gh)"),
      entry("uv", uv, "Install uv (Astral Python manager)"),
      entry("Node.js", node, "Install Node.js via nvm"),
      entry("pnpm", pnpm, "Enable pnpm via corepack"),
      entry("Neovim", nvim, "Install Neovim (latest release)"),
      entry("btop", btop, "Install btop system monitor"),
      entry("nginx", nginx, "Install nginx web server"),
      entry("Certbot", cert, "Install Certbot (Let's Encrypt)"),
      entry("UFW", ufw, "Install and configure UFW firewall"),
      entry("Fail2ban", f2b, "Install and configure Fail2ban"),
      entry("Image Viewer", img, "Install Advance Image Viewer"),
      entry("curlpad", curl, "Install curlpad"),
      entry("Developer Tools", dev, "Install developer tools (openssl, clangd, build-essential, etc.)"),
      entry("SSH Key", ssh, "Generate SSH key pair (RSA 4096-bit) and display public key"),
      entry("fastfetch", fast, "Install fastfetch system information tool"),
      entry("podman", pod, "Install podman container engine"),
      entry("zsh", z, "Install zsh and set it as default shell"),
      entry("git", g, "Install git version control system"),
      entry("rkhunter", rk, "Install rkhunter (Rootkit Hunter) security scanner"),
      entry("chkrootkit", chk, "Install chkrootkit security scanner"),
      entry("vrms", vrms, "Install vrms (Virtual Richard M. Stallman - lists non-free packages)"),
    ];
  }

  async run(): Promise<void> {
    this.startTime = Date.now();
    showWelcome();

    const bootstrapEntry = this.installOptions[0];
    process.stdout.write(`${bold("Running bootstrap...")}\n`);

    let result: InstallerResult;
    try {
      result = await bootstrapEntry.install();
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : String(e);
      process.stdout.write(`✖ Bootstrap failed: ${msg}\n\n`);
      process.stdout.write(`${yellow("⚠")} rig requires sudo access for system package installation.\n`);
      process.stdout.write(`${cyan("💡")} To use rig, run it in an interactive terminal: rig\n\n`);
      process.stdout.write("Available tools include: GitHub CLI, uv, Node.js, Neovim, nginx, and more!\n");
      return;
    }

    this.results.push({ name: bootstrapEntry.name, result });

    if (!result.success) {
      process.stdout.write(`✖ Bootstrap failed: ${result.message}\n\n`);
      process.stdout.write(`${yellow("⚠")} rig requires sudo access for system package installation.\n`);
      process.stdout.write(`${cyan("💡")} To use rig, run it in an interactive terminal: rig\n\n`);
      process.stdout.write("Available tools include: GitHub CLI, uv, Node.js, Neovim, nginx, and more!\n");
      return;
    }

    process.stdout.write(`${green("✓")} Bootstrap completed\n\n`);

    const presetChoice = await askChoice(
      "Select preset (optional)",
      ["none", "dev", "server", "security"],
      "none",
    );
    const presetTools = getPreset(presetChoice);

    if (presetChoice !== "none") {
      if (presetTools.size > 0) {
        const toolsList = [...presetTools].sort().join(", ");
        process.stdout.write(`${dim(`→ Using '${presetChoice}' preset (pre-selecting: ${toolsList})`)}\n`);
      }
    }

    const selectedOptions: InstallerEntry[] = [];
    for (const entry of this.installOptions.slice(1)) {
      const spinner = new Spinner(`Checking ${entry.name}...`);
      spinner.start();
      const installed = this.checkToolInstalled(entry.name);
      spinner.stop();
      if (installed) {
        process.stdout.write(`${dim(`→ ${entry.name} is already installed, skipping`)}\n`);
        continue;
      }

      if (presetTools.has(entry.name)) {
        process.stdout.write(`${dim(`→ ${entry.name} selected via '${presetChoice}' preset`)}\n`);
        selectedOptions.push(entry);
        continue;
      }

      const answer = await confirm(`Install ${entry.name}?`, false);
      if (answer) {
        selectedOptions.push(entry);
      }
    }

    if (selectedOptions.length === 0) {
      process.stdout.write(`${yellow("No tools selected for installation.")}\n`);
      return;
    }

    process.stdout.write(`\n${bold(`Installing ${selectedOptions.length} tool(s)...`)}\n\n`);

    for (const entry of selectedOptions) {
      process.stdout.write(`${bold(brightCyan(`Installing ${entry.name}...`))}\n`);
      try {
        result = await entry.install();

        if (result.success) {
          process.stdout.write(`${green("✓")} ${result.message}\n`);
        } else {
          process.stdout.write(`${red("✖")} ${result.message}\n`);
          if (result.error) process.stdout.write(`${dim(red(result.error))}\n`);
        }

        this.results.push({ name: entry.name, result });
      } catch (e: unknown) {
        if (e instanceof RigError) {
          const errResult: InstallerResult = { success: false, message: e.message, error: e.message };
          this.results.push({ name: entry.name, result: errResult });
          process.stdout.write(`${red("✖")} ${e.message}\n`);
          if (e.suggestion) process.stdout.write(`${cyan("💡")} ${e.suggestion}\n`);
          this.logger.error(`Error installing ${entry.name}: ${e.message}`);
        } else if (e instanceof Error && e.name === "ExitPromptError") {
          process.stdout.write(`\n${yellow("⚠")} Installation interrupted by user\n`);
          break;
        } else {
          const msg = e instanceof Error ? e.message : String(e);
          const errResult: InstallerResult = { success: false, message: `Unexpected error: ${msg}`, error: msg };
          this.results.push({ name: entry.name, result: errResult });
          process.stdout.write(`${red("✖")} Unexpected error: ${e}\n`);
          this.logger.error(`Unexpected error installing ${entry.name}: ${e}`);
        }
      }
    }

    showSummary(this.results, this.startTime);
    process.stdout.write("\n");
    updateShellConfig(".local/bin");
    showNextSteps(this.results);
    process.stdout.write("\n");
    process.stdout.write(`${green("✓")} Setup completed successfully 🎉\n`);
    process.stdout.write(`${dim(`📄 Log file: ${this.logger.logFile}`)}\n`);
  }
}
