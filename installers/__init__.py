# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Installers for various tools and packages."""

from .bootstrap import BootstrapInstaller
from .github_cli import GitHubCLIInstaller
from .uv import UVInstaller
from .nodejs import NodeJSInstaller
from .pnpm import PNPMInstaller
from .neovim import NeovimInstaller
from .btop import BTopInstaller
from .nginx import NginxInstaller
from .certbot import CertbotInstaller
from .ufw import UFWInstaller
from .fail2ban import Fail2banInstaller
from .image_viewer import ImageViewerInstaller
from .curlpad import CurlpadInstaller
from .dev_tools import DevToolsInstaller
from .ssh_key import SSHKeyInstaller
from .fastfetch import FastfetchInstaller
from .podman import PodmanInstaller
from .zsh import ZshInstaller
from .git import GitInstaller
from .rkhunter import RkhunterInstaller
from .chkrootkit import ChkrootkitInstaller

__all__ = [
    "BootstrapInstaller",
    "GitHubCLIInstaller",
    "UVInstaller",
    "NodeJSInstaller",
    "PNPMInstaller",
    "NeovimInstaller",
    "BTopInstaller",
    "NginxInstaller",
    "CertbotInstaller",
    "UFWInstaller",
    "Fail2banInstaller",
    "ImageViewerInstaller",
    "CurlpadInstaller",
    "DevToolsInstaller",
    "SSHKeyInstaller",
    "FastfetchInstaller",
    "PodmanInstaller",
    "ZshInstaller",
    "GitInstaller",
    "RkhunterInstaller",
    "ChkrootkitInstaller",
]

