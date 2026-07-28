const ESC = "\x1b";

export const RESET = `${ESC}[0m`;
export const BOLD = `${ESC}[1m`;
export const DIM = `${ESC}[2m`;
export const ITALIC = `${ESC}[3m`;

export const RED = `${ESC}[31m`;
export const GREEN = `${ESC}[32m`;
export const YELLOW = `${ESC}[33m`;
export const BLUE = `${ESC}[34m`;
export const MAGENTA = `${ESC}[35m`;
export const CYAN = `${ESC}[36m`;
export const WHITE = `${ESC}[37m`;
export const GRAY = `${ESC}[90m`;

export const BG_RED = `${ESC}[41m`;
export const BG_GREEN = `${ESC}[42m`;
export const BG_YELLOW = `${ESC}[43m`;
export const BG_BLUE = `${ESC}[44m`;
export const BG_CYAN = `${ESC}[46m`;

export const BRIGHT_WHITE = `${ESC}[97m`;
export const BRIGHT_BLUE = `${ESC}[94m`;
export const BRIGHT_CYAN = `${ESC}[96m`;
export const BRIGHT_GREEN = `${ESC}[92m`;
export const BRIGHT_YELLOW = `${ESC}[93m`;

export const HIDE_CURSOR = `${ESC}[?25l`;
export const SHOW_CURSOR = `${ESC}[?25h`;
export const CLEAR_LINE = `${ESC}[2K`;
export const CLEAR_SCREEN = `${ESC}[2J`;
export const MOVE_UP = (n = 1) => `${ESC}[${n}A`;
export const MOVE_DOWN = (n = 1) => `${ESC}[${n}B`;
export const MOVE_FORWARD = (n = 1) => `${ESC}[${n}C`;
export const MOVE_BACK = (n = 1) => `${ESC}[${n}D`;
export const CARRIAGE_RETURN = "\r";

export function color(text: string, code: string): string {
  return `${code}${text}${RESET}`;
}

export function bold(text: string): string {
  return `${BOLD}${text}${RESET}`;
}

export function dim(text: string): string {
  return `${DIM}${text}${RESET}`;
}

export function red(text: string): string {
  return color(text, RED);
}

export function green(text: string): string {
  return color(text, GREEN);
}

export function yellow(text: string): string {
  return color(text, YELLOW);
}

export function blue(text: string): string {
  return color(text, BLUE);
}

export function cyan(text: string): string {
  return color(text, CYAN);
}

export function white(text: string): string {
  return color(text, WHITE);
}

export function gray(text: string): string {
  return color(text, GRAY);
}

export function brightWhite(text: string): string {
  return color(text, BRIGHT_WHITE);
}

export function brightBlue(text: string): string {
  return color(text, BRIGHT_BLUE);
}

export function brightCyan(text: string): string {
  return color(text, BRIGHT_CYAN);
}

export function brightGreen(text: string): string {
  return color(text, BRIGHT_GREEN);
}

export function brightYellow(text: string): string {
  return color(text, BRIGHT_YELLOW);
}

const spinnerFrames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];

export class Spinner {
  private frame = 0;
  private interval: ReturnType<typeof setInterval> | null = null;
  private message: string;

  constructor(message: string) {
    this.message = message;
  }

  start(): void {
    process.stdout.write(HIDE_CURSOR);
    this.render();
    this.interval = setInterval(() => this.render(), 80);
  }

  private render(): void {
    const f = spinnerFrames[this.frame % spinnerFrames.length];
    this.frame++;
    process.stdout.write(`${CARRIAGE_RETURN}${CYAN}${f}${RESET} ${DIM}${this.message}${RESET}`);
  }

  stop(): void {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
    process.stdout.write(`${CARRIAGE_RETURN}${CLEAR_LINE}`);
    process.stdout.write(SHOW_CURSOR);
  }

  succeed(text?: string): void {
    this.stop();
    if (text) process.stdout.write(`${GREEN}✓${RESET} ${text}\n`);
  }

  fail(text?: string): void {
    this.stop();
    if (text) process.stdout.write(`${RED}✖${RESET} ${text}\n`);
  }
}

export function info(msg: string): void {
  process.stdout.write(`${BLUE}ℹ${RESET} ${msg}\n`);
}

export function success(msg: string): void {
  process.stdout.write(`${GREEN}✓${RESET} ${msg}\n`);
}

export function fail(msg: string): void {
  process.stdout.write(`${RED}✖${RESET} ${msg}\n`);
}

export function warn(msg: string): void {
  process.stdout.write(`${YELLOW}⚠${RESET} ${msg}\n`);
}

export function step(msg: string): void {
  process.stdout.write(`\n${BOLD}${msg}${RESET}\n`);
}

export function separator(): void {
  process.stdout.write(`${DIM}${"─".repeat(50)}${RESET}\n`);
}
