import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { green, dim, red, blue } from "./ansi.js";

function detectShell(): string {
  const shell = process.env["SHELL"] || "";
  if (shell.includes("zsh")) return "zsh";
  if (shell.includes("bash")) return "bash";
  try {
    const passwd = readFileSync("/etc/passwd", "utf8");
    const uid = process.getuid?.();
    if (uid !== undefined) {
      for (const line of passwd.split("\n")) {
        const parts = line.split(":");
        if (parts[2] === String(uid)) {
          const sh = parts[parts.length - 1]?.toLowerCase() || "";
          if (sh.includes("zsh")) return "zsh";
          if (sh.includes("bash")) return "bash";
        }
      }
    }
  } catch {}
  return "bash";
}

function getShellConfig(shell: string): string {
  const home = homedir();
  const candidates = shell === "zsh"
    ? [".zshrc", ".zprofile", ".zshenv"]
    : [".bashrc", ".bash_profile", ".profile"];

  for (const c of candidates) {
    const p = join(home, c);
    if (existsSync(p)) return p;
  }
  return shell === "zsh" ? join(home, ".zshrc") : join(home, ".bashrc");
}

function addToPath(configPath: string, pathToAdd: string): boolean {
  try {
    let content = existsSync(configPath) ? readFileSync(configPath, "utf8") : "";
    const exportLine = `export PATH="${pathToAdd}:$PATH"`;

    if (content.includes(exportLine)) {
      process.stdout.write(`${dim(`→ PATH entry already exists in ${configPath.split("/").pop()}`)}\n`);
      return false;
    }

    const altFormats = [
      `export PATH="${pathToAdd}:\\$PATH"`,
      `export PATH=${pathToAdd}:$PATH`,
      `export PATH=${pathToAdd}:\\$PATH`,
      `PATH="${pathToAdd}:$PATH"`,
      `PATH=${pathToAdd}:$PATH`,
    ];

    for (const alt of altFormats) {
      if (content.includes(alt)) {
        process.stdout.write(`${dim(`→ PATH entry already exists in ${configPath.split("/").pop()}`)}\n`);
        return false;
      }
    }

    if (content.length > 0 && !content.endsWith("\n")) content += "\n";
    content += `\n# Added by rig installer\n${exportLine}\n`;

    const dir = configPath.substring(0, configPath.lastIndexOf("/"));
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    writeFileSync(configPath, content, "utf8");
    process.stdout.write(`${green(`✓ Added PATH entry to ${configPath.split("/").pop()}`)}\n`);
    return true;
  } catch (e) {
    process.stdout.write(`${red(`✖ Failed to update ${configPath.split("/").pop()}: ${e}`)}\n`);
    return false;
  }
}

export function updateShellConfig(installDir: string): boolean {
  try {
    process.stdout.write(`${blue("ℹ")} Configuring shell...\n`);
    const shell = detectShell();
    process.stdout.write(`${dim(`→ Detected shell: ${shell}`)}\n`);

    const configFile = getShellConfig(shell);
    process.stdout.write(`${dim(`→ Config file: ${configFile.split("/").pop()}`)}\n`);

    const pathEntry = `$HOME/${installDir}`;
    const success = addToPath(configFile, pathEntry);

    if (success) {
      process.stdout.write(`${green("✓ Shell configuration updated")}\n`);
      process.stdout.write(
        `${dim(`→ Run: source ~/${configFile.split("/").pop()} to apply changes immediately`)}\n`,
      );
    }

    return success;
  } catch (e) {
    process.stdout.write(`${red(`✖ Failed to configure shell: ${e}`)}\n`);
    return false;
  }
}
