#!/usr/bin/env node
import { SetupManager } from "./setup-manager.js";
import { yellow } from "./utils/ansi.js";

function main(): void {
  const verbose = process.argv.includes("--verbose") || process.argv.includes("-v") || process.env["RIG_VERBOSE"] === "1";
  if (verbose) process.env["RIG_VERBOSE"] = "1";

  const manager = new SetupManager();
  manager.run()
    .catch((e: unknown) => {
      if (e instanceof Error && e.name === "ExitPromptError") {
        process.stdout.write(`\n${yellow("⚠")} Setup interrupted by user\n`);
        process.exit(1);
      }
      if (e instanceof Error) {
        process.stdout.write(`✖ Fatal error: ${e.message}\n`);
      } else {
        process.stdout.write(`✖ Fatal error: ${e}\n`);
      }
      process.exit(1);
    });
}

main();
