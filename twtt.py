#!/usr/bin/python
import sys
import re
# I think we also need to include the wika stuff here

# Global variables

'''
	MAIN - Runs the program.
'''
def main(fname):
	get_lines(fname)
#	get_tokens()

'''
'''
def get_lines(fname):
# condition which have to be met
	print("run get_line\n")
	#try:
	fptr = open(fname, 'r')
	for line in fptr:
		# This function removes the @ and # 
		#mod_line = remove_unwanted(line)
		mod_line = replace_ascii(mod_line)
		print(mod_line + "\n")
	#except:
		#print("Could not read file.")
	#	print("Something with wrong"), sys.exc_info()[0]
	#finally:
	#	print("clean up")
		# Clean up stuff

def remove_unwanted(line):
	# Removes @ sign from usernames
	pattern = r'(@<.*?tweet-url username.*?>(.*?)<.*?>)'
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), i.group(2))

	# Removes # from hash-tags
	pattern = r'(<.*?class="tweet-url hashtag".*?>#(.*?)<.*?>)'
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), i.group(2))

	# Removes http, www and other links
	pattern = r'(<.*?>.*?<.*?>)'
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), '')

	return line

def find_end_of_sentence(line):
	#w.(space)w.
	#you also have to do this for ! and ?
	#return re.sub(r'<(.*?)>', '', line, re.M|re.I)
	#There is a problem here, it will not keep the content in the middle
	#of the html tags
	#matchObj = re.match( r'(.*)', line, re.M|re.I)

'''
html codes
You should replace the codes with these symboles
'''
def replace_ascii(line):
	dict = {'&amp;':'&',
	'&quot;':'"',
	'&frasl;':'/',
	'&lt;':'<',
	'&gt;':'>',
	'&lsquo;':'\'',
	'&rsquo;':'\'',
	'&sbquo;':',',
	'&ldquo;':'"',
	'&rdquo;':'"'
	}
	for i in dict.keys():

	return line

def remove_html_www(line):
	return re.sub(r'(^["www"|"html"](.*))', '', line, re.M|re.I)

if __name__ == "__main__":
	main("/Users/g1izzyw/Documents/CSC401/A1/TwtClassification/tweets/test")