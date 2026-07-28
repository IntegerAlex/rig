import type { InstallerResult } from "../types.js";
import { bold, dim, green, red, yellow, cyan, white, brightGreen, brightBlue, brightCyan } from "../utils/ansi.js";

export function showSummary(results: Array<{ name: string; result: InstallerResult }>, startTime: number): void {
  let successCount = 0;
  let failCount = 0;
  let skippedCount = 0;

  process.stdout.write("\n");
  process.stdout.write(`${brightBlue("┌─")} ${brightBlue("📊")} ${bold(brightBlue("Installation Summary"))} ${brightBlue("─".repeat(30))}${brightBlue("┐")}\n`);
  process.stdout.write(`${dim("│")} ${brightCyan("Tool")}${" ".repeat(17)}${dim("│")} ${cyan("Status")}${" ".repeat(8)}${dim("│")} ${white("Details")}${" ".repeat(28)}${dim("│")}\n`);
  process.stdout.write(`${dim("│")}${"─".repeat(20)}${dim("│")}${"─".repeat(14)}${dim("│")}${"─".repeat(36)}${dim("│")}\n`);

  for (const { name, result } of results) {
    let status: string;
    if (result.success) {
      if (result.message.toLowerCase().includes("already installed") || result.message.toLowerCase().includes("already exists")) {
        status = `${dim("⏭️  Skipped")}`;
        skippedCount++;
      } else {
        status = `${green("✅ Success")}`;
        successCount++;
      }
    } else {
      status = `${red("❌ Failed")}`;
      failCount++;
    }

    let msg = result.message;
    if (result.error) {
      msg += result.error.length > 57
        ? ` (${red(result.error.substring(0, 54) + "...")})`
        : ` (${red(result.error)})`;
    }

    const nameDisplay = name.length > 18 ? name.substring(0, 15) + "..." : name;
    process.stdout.write(`${dim("│")} ${bold(nameDisplay.padEnd(18))}${dim("│")} ${status.padEnd(12)}${dim("│")} ${msg.substring(0, 34).padEnd(34)}${dim("│")}\n`);
  }

  process.stdout.write(`${brightBlue("└")}${brightBlue("─".repeat(72))}${brightBlue("┘")}\n`);
  process.stdout.write("\n");

  const total = results.length;
  const successRate = total > 0 ? ((successCount / total) * 100).toFixed(1) : "0.0";
  const endTime = Date.now();
  const duration = ((endTime - startTime) / 1000).toFixed(1);

  process.stdout.write(`${brightGreen("┌─")} ${brightGreen("📈")} ${bold(brightGreen("Statistics"))} ${brightGreen("─".repeat(36))}${brightGreen("┐")}\n`);
  process.stdout.write(`${dim("│")}  ${green("✅ Successful")}    ${bold(String(successCount).padStart(3))}                              ${dim("│")}\n`);
  process.stdout.write(`${dim("│")}  ${red("❌ Failed")}        ${bold(String(failCount).padStart(3))}                              ${dim("│")}\n`);
  process.stdout.write(`${dim("│")}  ${yellow("⏭️  Skipped")}      ${bold(String(skippedCount).padStart(3))}                              ${dim("│")}\n`);
  process.stdout.write(`${dim("│")}  ${white("📊 Total")}        ${bold(String(total).padStart(3))}                              ${dim("│")}\n`);
  process.stdout.write(`${dim("│")}  ${cyan("🎯 Success Rate")}  ${bold(`${successRate}%`.padStart(5))}                              ${dim("│")}\n`);
  process.stdout.write(`${dim("│")}  ${cyan("⏱️  Total Time")}   ${bold(`${duration}s`.padStart(5))}                              ${dim("│")}\n`);
  process.stdout.write(`${brightGreen("└")}${brightGreen("─".repeat(54))}${brightGreen("┘")}\n`);
  process.stdout.write("\n");
}
