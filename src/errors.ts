export class RigError extends Error {
  public suggestion: string | undefined;

  constructor(message: string, suggestion?: string) {
    super(message);
    this.suggestion = suggestion;
    this.name = "RigError";
  }
}

export class NetworkError extends RigError {
  public url: string | undefined;

  constructor(message: string, url?: string) {
    const sug = `Check your internet connection and try again. ${url ? "URL: " + url : ""}`;
    super(message, sug);
    this.url = url;
    this.name = "NetworkError";
  }
}

export class PermissionError extends RigError {
  public command: string | undefined;

  constructor(message: string, command?: string) {
    const sug = `This operation requires administrator privileges. ${command ? "Try running with sudo: sudo " + command : "Try running with sudo."}`;
    super(message, sug);
    this.command = command;
    this.name = "PermissionError";
  }
}

export class PackageManagerError extends RigError {
  public packageName: string | undefined;

  constructor(message: string, packageName?: string) {
    const parts: string[] = ["Try updating package lists: sudo apt update"];
    if (packageName) {
      parts.push(
        `Check if package exists: apt search ${packageName}`,
        `Try installing manually: sudo apt install ${packageName}`,
      );
    }
    parts.push("Check for locked files: sudo killall apt apt-get");
    super(message, parts.join(" | "));
    this.packageName = packageName;
    this.name = "PackageManagerError";
  }
}

export class CommandNotFoundError extends RigError {
  constructor(command: string) {
    const message = `Command not found: ${command}`;
    const suggestion = `Install ${command} using your package manager (apt, yum, etc.)`;
    super(message, suggestion);
    this.name = "CommandNotFoundError";
  }
}

export class InstallationError extends RigError {
  public tool: string | undefined;
  public recoverySteps: string[] | undefined;

  constructor(message: string, tool?: string, recoverySteps?: string[]) {
    let suggestion: string;
    if (recoverySteps) {
      suggestion = recoverySteps.join(" | ");
    } else if (tool) {
      suggestion =
        `Try installing ${tool} manually | Check system logs for more details | Ensure all dependencies are installed`;
    } else {
      suggestion = "Check system logs for more details";
    }
    super(message, suggestion);
    this.tool = tool;
    this.recoverySteps = recoverySteps;
    this.name = "InstallationError";
  }
}
