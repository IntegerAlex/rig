# Changelog

All notable changes to this project will be documented in this file.

## [0.1.3] - 2025-01-02

### Added

- Automatic shell configuration: Detects bash/zsh and auto-updates .bashrc/.zshrc with PATH
- Enhanced error handling: Custom exception classes with actionable recovery suggestions
- Retry logic: Network operations retry 3 times with exponential backoff
- CLI beautification: Progress bars and spinners for better visual feedback
- Enhanced summary display: Statistics panel with success rates, timing, and better formatting
- Improved welcome screen: Better formatting, emojis, and visual enhancements

### Changed

- Suppressed non-critical log warnings for cleaner output
- Better error messages: Specific, actionable suggestions instead of generic errors
- Enhanced installation summary: Better table formatting with icons and color coding
- Improved installer: Automatic shell config update eliminates manual PATH setup

### Fixed

- Fixed shell configuration error (duplicate import issue)
- Better handling of network failures with retry logic
- Improved error categorization and recovery suggestions

## [0.1.2] - 2025-01-02

### Added

- Cloudflare Worker installer at `https://rig-installer.inquiry-akshatkotpalliwar.workers.dev`
- Automatic rig execution after installation
- Improved bootstrap failure handling - shows available tools even without sudo
- Graceful error messages when sudo access is not available

### Changed

- Enhanced installer to run rig automatically after installation
- Better user experience when bootstrap fails due to sudo requirements
- Improved error handling and user guidance

## [0.1.1] - 2025-12-31

### Added

- Added vrms (Virtual Richard M. Stallman) installer - lists non-free packages

## [0.1.0] - 2025-12-31

### Added (Initial Release)

- Initial release: Opinionated system setup tool for Linux distributions
- Installable tools: GitHub CLI, uv, Node.js, pnpm, Neovim, btop, nginx, Certbot, UFW, Fail2ban, Image Viewer, curlpad, Developer Tools, SSH Key, fastfetch, podman, zsh, git, rkhunter, chkrootkit
- Rich UI with interactive prompts and installation summaries
- Automatic detection of already installed tools
- Comprehensive error handling and logging
- SPDX copyright headers and GPL-3.0-only license

### Changed

- Migrated from shell script to Python with enhanced features

### Fixed

- Fixed apt CLI warnings, command not found errors, and hanging issues

[0.1.0]: https://github.com/integeralex/rig/releases/tag/v0.1.0
