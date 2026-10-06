import re
import sys


def find_missing_comments(pot_content: str):
	blocks = re.split(r"\n\s*\n", pot_content.strip())
	missing = []
	total = 0

	for block in blocks:
		b = block.strip()
		if not b:
			continue
		lines = b.splitlines()
		has_msgid = any(line.startswith("msgid") for line in lines)
		if not has_msgid:
			continue
		# Header entry in gettext POT has msgid "" followed by Project-Id-Version in msgstr
		if any(line.strip() == 'msgid ""' for line in lines) and any(
			"Project-Id-Version:" in line for line in lines
		):
			continue

		total += 1
		has_comment = any(line.startswith("#.") for line in lines)
		if not has_comment:
			locs = [line[2:].strip() for line in lines if line.startswith("#:")]
			msgid_parts = []
			in_msgid = False
			for line in lines:
				if line.startswith("msgid "):
					in_msgid = True
					msgid_parts.append(line[6:].strip().strip('"'))
				elif in_msgid and line.startswith('"'):
					msgid_parts.append(line.strip().strip('"'))
				elif line.startswith("msgstr") or line.startswith("msgid_plural"):
					in_msgid = False
			msgid_text = "".join(msgid_parts)
			missing.append({"locations": locs, "msgid": msgid_text})

	return total, missing


def validate_pot_file(pot_path: str) -> int:
	try:
		with open(pot_path, "r", encoding="utf-8") as f:
			content = f.read()
	except Exception as err:
		sys.stderr.write(f"\n[ERROR] Unable to read POT file {pot_path}: {err}\n")
		return 1

	total, missing = find_missing_comments(content)
	if missing:
		sys.stderr.write(
			f"\n[ERROR] Found {len(missing)} translatable string(s) missing translator comments in {pot_path}:\n\n"
		)
		for item in missing:
			loc_str = ", ".join(item["locations"]) if item["locations"] else "unknown location"
			sys.stderr.write(f'  * {loc_str}:\n    "{item["msgid"]}"\n')
		sys.stderr.write(
			"\nPlease place '# Translators: <context explanation>' directly above each translatable string.\n\n"
		)
		return 1

	print(f"Validation successful: all {total} translatable strings in {pot_path} have translator comments.")
	return 0


def validate_pot_action(target, source, env):
	pot_path = str(target[0])
	return validate_pot_file(pot_path)


if __name__ == "__main__":
	target_pot = sys.argv[1] if len(sys.argv) > 1 else "VisionAssistant.pot"
	sys.exit(validate_pot_file(target_pot))
