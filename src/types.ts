export interface InstallerResult {
  success: boolean;
  message: string;
  error?: string;
}

export interface InstallerOption {
  name: string;
  installer: {
    install: () => Promise<InstallerResult>;
    is_installed?: () => boolean;
  };
  description: string;
}
