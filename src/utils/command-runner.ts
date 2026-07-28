import { spawnSync } from "node:child_process";
import { Spinner, dim } from "./ansi.js";
import type { SetupLogger } from "./logger.js";
import { NetworkError, CommandNotFoundError, PermissionError, PackageManagerError } from "../errors.js";

export interface RunOptions {
  check?: boolean;
  capture?: boolean;
  sudo?: boolean;
  description?: string;
  timeout?: number;
}

function isNetworkCmd(command: string[]): boolean {
  const s = command.join(" ").toLowerCase();
  return ["curl", "wget", "apt update", "apt-get update"].some((x) => s.includes(x));
}

function isLongRunning(command: string[]): boolean {
  const s = command.join(" ").toLowerCase();
  return ["apt update", "apt install", "apt-get update", "apt-get install", "curl", "wget", "git clone"].some(
    (x) => s.includes(x),
  );
}

function sudoAvailable(): boolean {
  try {
    const r = spawnSync("sudo", ["-n", "true"], { timeout: 2000 });
    if (r.status === 0) return true;
    spawnSync("which", ["sudo"], { timeout: 1000 });
    return true;
  } catch {
    return false;
  }
}

export class CommandRunner {
  verbose: boolean;
  private logger: SetupLogger;

  constructor(logger: SetupLogger) {
    this.logger = logger;
    this.verbose = process.env["RIG_VERBOSE"] === "1";
  }

  run(
    command: string[],
    options: RunOptions = {},
  ) {
    const { check = true, capture = false, sudo = false, description, timeout } = options;

    let cmd = [...command];

    if (sudo) {
      if (!sudoAvailable()) {
        throw new Error("sudo is required but not available. Please ensure sudo is installed.");
      }
      cmd = ["sudo", ...cmd];
    }

    const isApt = cmd.some((c) => c === "apt" || c === "apt-get");

    if (isApt) {
      const aptIdx = cmd.indexOf("apt") !== -1 ? cmd.indexOf("apt") : cmd.indexOf("apt-get");
      if (aptIdx !== -1) {
        if (!cmd.some((c) => c.startsWith("-q"))) {
          const before = cmd.slice(0, aptIdx + 1);
          const after = cmd.slice(aptIdx + 1);
          cmd = [...before, "-qq", ...after];
        }
      }
    }

    const cmdStr = cmd.join(" ");
    this.logger.info(`CMD: ${cmdStr}`);
    if (this.verbose) process.stdout.write(`${dim(`$ ${cmdStr}`)}\n`);

    if (description) {
      process.stdout.write(`${dim(`→ ${description}`)}\n`);
    }

    const showProgress = isLongRunning(command) && !capture && !sudo;
    const spinner = showProgress ? new Spinner(description || `Running: ${command[0]}`) : null;
    if (spinner) spinner.start();

    try {
      const oldDebian = process.env["DEBIAN_FRONTEND"];
      const oldAptLists = process.env["APT_LISTCHANGES_FRONTEND"];
      if (isApt) {
        process.env["DEBIAN_FRONTEND"] = "noninteractive";
        process.env["APT_LISTCHANGES_FRONTEND"] = "none";
      }

      const result = spawnSync(cmd[0], cmd.slice(1), {
        timeout: timeout ?? (sudo ? 0 : 300_000),
        stdio: capture || showProgress ? "pipe" : "inherit",
        encoding: "utf8",
      });

      if (isApt) {
        if (oldDebian === undefined) delete process.env["DEBIAN_FRONTEND"]; else process.env["DEBIAN_FRONTEND"] = oldDebian;
        if (oldAptLists === undefined) delete process.env["APT_LISTCHANGES_FRONTEND"]; else process.env["APT_LISTCHANGES_FRONTEND"] = oldAptLists;
      }

      if (spinner) spinner.stop();

      if (check && result.status !== 0) {
        const stderr = (result.stderr || "") as string;
        const stdoutText = (result.stdout || "") as string;

        if (isNetworkCmd(command)) {
          throw new NetworkError(
            `Network request failed: ${cmdStr} (exit code: ${result.status})`,
            command.find((a) => a.startsWith("http")) || undefined,
          );
        }

        if (sudo && result.status === 1) {
          throw new PermissionError(`Permission denied running: ${cmdStr}`, cmdStr);
        }

        const lowerStderr = stderr.toString().toLowerCase();
        const lowerStdout = stdoutText.toString().toLowerCase();
        if (lowerStderr.includes("lock") || lowerStdout.includes("lock")) {
          throw new PackageManagerError(`Package manager is locked: ${cmdStr}`);
        }

        throw new Error(`Command failed: ${cmdStr} (exit: ${result.status})`);
      }

      return result;
    } catch (e: unknown) {
      if (spinner) spinner.stop();

      if (e instanceof Error && "code" in e && (e as NodeJS.ErrnoException).code === "ENOENT") {
        throw new CommandNotFoundError(command[0]);
      }

      throw e;
    }
  }
}
