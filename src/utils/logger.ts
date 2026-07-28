import { appendFileSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const LOG_FILE_VAR = "/var/log/rig.log";
const HOME_LOG = join(homedir(), ".rig.log");

function logTimestamp(): string {
  const iso = new Date(Date.now()).toISOString();
  return iso.slice(0, 10) + " " + iso.slice(11, 19);
}

export function getLogPath(): string {
  try {
    const dir = "/var/log";
    if (!existsSync(dir)) mkdirSync(dir);
    appendFileSync(LOG_FILE_VAR, "");
    return LOG_FILE_VAR;
  } catch {
    return HOME_LOG;
  }
}

export class SetupLogger {
  logFile: string;

  constructor(logFile?: string) {
    this.logFile = logFile ?? getLogPath();
    this.ensureLogFile();
  }

  private ensureLogFile(): void {
    try {
      const dir = this.logFile.substring(0, this.logFile.lastIndexOf("/"));
      if (!existsSync(dir)) mkdirSync(dir);
      if (!existsSync(this.logFile)) writeFileSync(this.logFile, "");
      appendFileSync(this.logFile, "");
    } catch {
      this.logFile = HOME_LOG;
      try { writeFileSync(this.logFile, ""); } catch {}
    }
  }

  log(level: string, message: string): void {
    const ts = logTimestamp();
    const line = `[${ts}] [${level.toUpperCase()}] ${message}\n`;
    try {
      appendFileSync(this.logFile, line);
    } catch {
      appendFileSync(HOME_LOG, line);
    }
  }

  info(message: string): void { this.log("info", message); }
  error(message: string): void { this.log("error", message); }
  warn(message: string): void { this.log("warn", message); }
  debug(message: string): void { this.log("debug", message); }
}
