import { createInterface } from "node:readline";
import { cyan, dim, yellow } from "./ansi.js";

export function confirm(prompt: string, defaultVal = false): Promise<boolean> {
  return new Promise((resolve) => {
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    const suffix = defaultVal ? "Y/n" : "y/N";
    rl.question(`${cyan("👉")} ${prompt} [${suffix}] `, (answer) => {
      rl.close();
      const a = answer.trim().toLowerCase();
      if (a === "") resolve(defaultVal);
      else resolve(a === "y" || a === "yes");
    });
  });
}

export function askChoice(
  prompt: string,
  choices: string[],
  defaultChoice: string,
): Promise<string> {
  return new Promise((resolve) => {
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    const choiceStr = choices.join("/");
    rl.question(`${cyan("?")} ${prompt} [${choiceStr}] (${defaultChoice}) `, (answer) => {
      rl.close();
      const a = answer.trim().toLowerCase();
      if (a === "") resolve(defaultChoice);
      for (const c of choices) {
        if (c.toLowerCase() === a) resolve(c);
      }
      resolve(defaultChoice);
    });
  });
}
