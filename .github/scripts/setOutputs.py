# Copyright (C) 2025-2026 NV Access Limited, Noelia Ruiz Martínez
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import sys

sys.path.insert(0, os.getcwd())
import buildVars


def main():
	addonId = buildVars.addon_info["addon_name"]
	name = "addonId"
	value = addonId
	with open(os.environ["GITHUB_OUTPUT"], "a") as f:
		_ = f.write(f"{name}={value}\n")


if __name__ == "__main__":
	main()
