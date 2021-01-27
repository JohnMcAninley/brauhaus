import os
import json


SETTINGS_DIR = "../.."
FILE_EXTENSION = ".json"


def read(module, setting=None):
	filepath = os.path.join(SETTINGS_DIR, module + FILE_EXTENSION)
	with open(filepath, 'r') as f:
		config = json.load(f)
	return config[setting] if setting else config


def defaults():
	# TODO
	pass


def update(module, setting, value):
	filepath = os.path.join(SETTINGS_DIR, module + FILE_EXTENSION)
	with open(filepath, 'r') as f:
		config = json.load(f)
	config[setting] = value
	with open(filepath, 'w') as f:
		json.dump(f, config)

# TODO Nested setting update

def append():
	# TODO
	pass
