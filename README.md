# rig

Opinionated system setup tool with basic tools to get started with in any Linux distribution.
No custom configurations, just the essential tools needed to be installed.

## Installation

### Quick Install (Recommended)

For Debian-based Linux distributions (Ubuntu, Debian, etc.):

```bash
curl https://rig-installer.gossorg.in | bash
```

This will:

- Download the latest binary release
- Install it to `~/.local/bin/rig`
- Make it executable
- Add it to PATH for the current session
- Provide usage instructions

**Usage:**

```bash
rig  # Run rig (requires sudo for system tools)
```

**Note:** rig requires sudo access for installing system packages, so run it in an interactive terminal where it can prompt for your password.

### From Source (Development)

```bash
git clone https://github.com/integeralex/rig.git
cd rig
uv sync
python3 main.py

# or

uv run main.py
```

## tools

- GitHub CLI (gh)
- uv - Python manager (pip alternative but better)
- Node.js - JavaScript runtime (nobody uses bun or deno)
- pnpm - JavaScript package manager (npm alternative but better)
- Neovim - text editor (vim alternative but better)
- btop - system monitor (top/htop alternative but better)
- nginx - web server (apache alternative but better for reverse proxy)
- Certbot - Let's Encrypt certificate manager (free SSL certificates)
- UFW - firewall (userfriendly firewall)
- Fail2ban - intrusion detection system (intrusion detection system)
- Image Viewer - advance image viewer (image viewer with A.I capabilities)
- curlpad - curlpad (curl alternative but better)
- Developer Tools - linux developer tools
- SSH Key - RSA 4096-bit generation and display
- fastfetch - system information tool (neofetch is deprecated)
- podman - container engine (it is rootless without extra efforts)
- zsh - shell (zsh as many plugins as you want)
- git - version control system (git is a must have some systems don't have it)
- rkhunter - Rootkit Hunter security scanner (security scanner)
- chkrootkit - security scanner (security scanner)

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.
