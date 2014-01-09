#!/usr/bin/python
import sys
import re
# I think we also need to include the wika stuff here

# Global variables
lines = []
tokens = []

'''
	MAIN - Runs the program.
'''
def main(fname):
	get_lines(fname)
#	get_tokens()

'''
	Input 
'''
'''
	- All html tags have to be removed
	- HTML character codes are replaced with ASCII equivilants

	- All token begining with "html" and "www" are removed
	- First chrater in twitter use name are removed + hashtags
	- Each sentence within a tweet is on its own line
	- Multiple punctuation is not split
	- Each tweet is seperated by "|"
'''
def get_lines(fname):
# condition which have to be met
	print("run get_lines")
	#try:
	fptr = open(fname, 'r')
	for line in fptr:
		modLine = remove_html(line)
		# I think this should be done last
		#modLine = replace_ascii(modLine)
		modLine = remove_html_www(modLine)
		modLine = remove_at_hashtag(modLine)
		modLine = 
		#modLine = remove_chr_usr_name(modLine)
		print modLine
	#except:
		#print("Could not read file.")
	#	print("Something with wrong"), sys.exc_info()[0]
	#finally:
	#	print("clean up")
		# Clean up stuff

def remove_html(line):
	return re.sub(r'<(.*?)>', '', line, re.M|re.I)
	#There is a problem here, it will not keep the content in the middle
	#of the html tags
	#matchObj = re.match( r'(.*)', line, re.M|re.I)

'''
html codes
space &#32
! &#33
" &#34
# &#35
$ &#36
% &#37
& &#38
' &#39
( &#40
) &#41
* &#42
+ &#43
, &#44
- &#45
. &#46
/
:
;
<
=
>
?
@
[
\
]
^
_
`
{
|
}
~
'''
def replace_ascii(line):

	return line

def remove_html_www(line):
	return re.sub(r'(^["www"|"html"](.*))', '', line, re.M|re.I)

def remove_chr_usr_name(line):
	return line


if __name__ == "__main__":
	main("/Users/g1izzyw/Desktop/A1/tweets/cnn")