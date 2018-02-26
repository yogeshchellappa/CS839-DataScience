import glob
import os
import sys

def main(path):
	os.chdir(path)
	
	files = glob.glob("*.txt")
	count = 0
	
	for i in files:
		fp = open(i, 'r')
		count += fp.read().count("<")
		fp.close()
	
	print("Number of reviews in " + path + ": " + str(len(files)))
	print("Number of mentions in " + path + ": " + str(count))


if len(sys.argv) < 2:
	print("Usage:\npython metrics <Path to Folder(set B or Set I or Set J)>")
	sys.exit(0)
else:
	main(sys.argv[1])