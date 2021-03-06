import json
import os


class config():
	"""Not meant to be instanced.
	   Use, for example: jf.config.directory
	"""
	# Init
	__config_path = "config.json"
	if not os.path.isfile(__config_path):
		__data = {
			"journal directory": "./entries",
			"font": {
				"family": "consolas",
				"label size": 10,
				"content size": 11
			}
		}
		with open(__config_path, "w") as f:
			json.dump(__data, f, ensure_ascii=True, indent=4)

	with open(__config_path, "r") as f:
		__data = json.load(f)

	_font = __data["font"]
	_font_family = _font["family"].strip()
	_font_labelsize = _font["label size"]
	_font_contentsize = _font["content size"]

	# Public vars
	directory = __data["journal directory"].strip()
	font_label = f"{_font_family} {_font_labelsize}"
	font_content = f"{_font_family} {_font_contentsize}"

	# Setup
	if not os.path.isdir(directory):
		os.mkdir(directory)
