import { bold, dim, green, cyan, brightWhite, brightBlue, blue } from "../utils/ansi.js";

const W = 70;
const t = brightBlue;

function strip(s: string): string {
  return s.replace(/\x1b\[[0-9;]*m/g, "");
}

function visLen(s: string): number {
  let n = 0;
  let i = 0;
  while (i < s.length) {
    const c = s.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF) {
      n += 2;
      i += 2;
    } else {
      if (c >= 0x2600 && c <= 0x27BF) n += 2;
      else if (c >= 0x2300 && c <= 0x23FF) n += 2;
      else if (c >= 0x2700 && c <= 0x27BF) n += 2;
      else if (c >= 0xFE00 && c <= 0xFE0F) n += 0;
      else n += 1;
      i += 1;
    }
  }
  return n;
}

export function showWelcome(): void {
  const lines: string[] = [];
  const sp = " ".repeat(W);

  const LEFT = `${t("│")} `;
  const RIGHT = ` ${t("│")}`;
  const lw = strip(LEFT).length;
  const rw = strip(RIGHT).length;
  const totalW = lw + W + rw;

  function sideLine(content: string): string {
    const pad = W - visLen(strip(content));
    const padded = pad > 0 ? content + " ".repeat(pad) : content.slice(0, W);
    return LEFT + padded + RIGHT;
  }

  const titleLeft = `${t("┌─")} ${t("✨")} ${bold(t("Welcome to rig"))} ${t("✨")} `;
  const titleDash = totalW - visLen(strip(titleLeft)) - visLen(strip(t("┐")));
  lines.push(`${titleLeft}${t("─".repeat(titleDash))}${t("┐")}`);

  lines.push(sideLine(`${t("🚀")} ${brightWhite("rig")} - ${bold("Opinionated system setup tool")} ${dim(cyan("v0.1.5"))}`));
  lines.push(sideLine(sp));
  lines.push(sideLine(`${blue("✨")}  Opinionated system setup tool with basic tools`));
  lines.push(sideLine(`   to get started with in any Linux distribution.`));
  lines.push(sideLine(`${cyan("📦")}  No custom configurations, just the essential tools`));
  lines.push(sideLine(`   needed to be installed.`));
  lines.push(sideLine(sp));
  lines.push(sideLine(`${dim("─".repeat(W))}`));
  lines.push(sideLine(sp));
  lines.push(sideLine(`${dim("©")}  ${dim("Copyright (C) 2025 Akshat Kotpalliwar")}`));
  lines.push(sideLine(`${dim("📜")}  ${dim("License:")} ${bold(dim(green("GPL-3.0-only")))}`));

  const bottomDash = totalW - visLen(strip(t("└"))) - visLen(strip(t("┘")));
  lines.push(`${t("└")}${t("─".repeat(bottomDash))}${t("┘")}`);

  process.stdout.write("\n");
  for (const line of lines) process.stdout.write(line + "\n");
  process.stdout.write("\n");
}
