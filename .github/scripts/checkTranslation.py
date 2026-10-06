# Copyright (C) 2026 NV Access Limited, Abdel
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sys
import os
from crowdin_api import CrowdinClient


def findFileId(client: CrowdinClient, projectId: int, baseTarget: str, searchExt: str) -> int | None:
	"""
	Iterates through all project files (using pagination) to find the ID of the source file matching the target name and extension.

	:param client: The Crowdin API client instance.
	:param projectId: The ID of the Crowdin project.
	:param base_target: The base name of the file (e.g., 'myAddon).
	:param search_ext: The extension to look for (e.g., '.pot').
	:return: The file ID if found, otherwise None.
	"""
	offset = 0
	limit = 100

	while True:
		resp = client.source_files.list_files(
			projectId=projectId,
			limit=limit,
			offset=offset,
		)

		data = resp["data"]
		for f in data:
			path_crowdin = f["data"]["path"].lower()
			# Check if the path ends with addon_id.pot or addon_id.xliff.
			if path_crowdin.endswith(f"{baseTarget}{searchExt}"):
				fileId = f["data"]["id"]
				print(f"DEBUG: Match found: {path_crowdin} (ID: {fileId})")
				return fileId

		if len(data) < limit:
			break

		offset += limit

	return None


def getScoreFromApi(fileNameToSearch: str, langId: str) -> float:
	"""
	Retrieves the translation progress score for a specific language and file.
	Handles pagination for both file listing and language status.

	:param fileNameToSearch: The local path or name of the file to check.
	:param langId: The language code (e.g., 'fr' or 'pt_BR').
	:return: The translation ratio between 0.0 and 1.0.
	"""
	token = os.environ.get("crowdinAuthToken")
	projectIdEnv = os.environ.get("CROWDIN_PROJECT_ID")

	if not token or not projectIdEnv:
		print("ERROR: Missing environment variables 'crowdinAuthToken' or 'CROWDIN_PROJECT_ID'.")
		return 0.0

	client = CrowdinClient(token=token)
	projectId = int(projectIdEnv)

	try:
		# Clean and prepare search patterns.
		# Example: 'addon/locale/fr/LC_MESSAGES/myAddon.po' -> base_target: 'myAddon'.
		baseTarget = fileNameToSearch.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0].lower()
		extTarget = fileNameToSearch.split(".")[-1].lower()

		# On Crowdin, the source for a .po file is usually a .pot file.
		searchExt = ".pot" if extTarget == "po" else f".{extTarget}"

		print(f"DEBUG: Searching for source file: {baseTarget}{searchExt}")

		fileId = findFileId(client, projectId, baseTarget, searchExt)

		if fileId is None:
			print(f"WARNING: File '{baseTarget}{searchExt}' not found on Crowdin.")
			return 0.0

		# Pagination for translation status (Progress).
		offset = 0
		limit = 100

		while True:
			resp = client.translation_status.get_file_progress(
				projectId=projectId,
				fileId=fileId,
				limit=limit,
				offset=offset,
			)

			data = resp["data"]
			for item in data:
				langApi = item["data"]["languageId"]

				# Flexible matching (e.g., 'fr' will match 'fr' or 'fr-FR' from API).
				# Also handles underscore to dash conversion for Crowdin compatibility
				if langApi.lower().startswith(langId.lower().replace("_", "-")):
					progress = float(item["data"]["translationProgress"])
					return progress

			# Check pagination total.
			total = resp["pagination"]["totalCount"]
			if offset + limit >= total:
				break
			offset += limit

		print(f"DEBUG: Language '{langId}' not found in progress list for this file.")
		return 0.0

	except Exception as e:
		print(f"API ERROR: {e}")
		return 0.0


def main():
	if len(sys.argv) < 3:
		print("Usage: python checkTranslation.py <filePath> <langId>")
		sys.exit(2)

	input_file = sys.argv[1]
	lang = sys.argv[2]

	score = getScoreFromApi(input_file, lang)

	# Output formatted for capture by the PowerShell script.
	print(f"translationRatio={score}")

	# Identify extension to provide a specific score label.
	ext = input_file.lower().split(".")[-1]
	if ext == "md":
		print(f"mdScore={score}")
	elif ext == "xliff":
		print(f"xliffScore={score}")
	else:
		# Default to poScore for .po and other localization files.
		print(f"poScore={score}")


if __name__ == "__main__":
	main()
