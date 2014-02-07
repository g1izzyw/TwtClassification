import sys
import re
import NLPlib

# Globals
tagger = NLPlib.NLPlib()

'''
	MAIN - Runs the program.
	- Parses the input parameters.
	- Parses the innput_f file.
	- Writes appropriate output to output_f file.
'''
def main():
	# Parse parameters
	try:
		input_f = sys.argv[1]
		output_f = sys.argv[2]
	except:
		sys.stderr.write("Correct number of parameters not provided!\n")

	# Parse input_f
	output = parse_file(input_f)
	# Write to output_f
	write_to_file(output_f, output)
'''
	Writes the output to file fname. The output is generated
	by the function parse_file - according to A1 handout.
'''
def write_to_file(fname, output):
	try:
		fw = open(fname, 'w')
		fw.write(output)
	except:
		sys.stderr.write("Error while writing to file!\n")

'''
	Parses the input file fname according to the specifications on
	the A1 handout.
'''
def parse_file(fname):
	output = ""
	
	try:
		fr = open(fname, 'r')
	except:
		sys.stderr.write("Error while reading input file!\n")
		sys.exit();

	for line in fr:
		# This function removes the @ and # and all html links 
		mod_line = remove_unwanted(line)
		# This function replaces all the html codes with symboles 
		mod_line = replace_ascii(mod_line)
		# This function seperates sentences in tweets
		mod_line = find_end_of_sentence(mod_line)
		# This function handels ellipsis
		mod_line = find_ellipsis(mod_line)
		# This function seperates single punctuation
		mod_line = sep_punctuation(mod_line)
		# Tags the tokens with NLPlib
		mod_line = tag_tokens(mod_line)
		
		output = output + mod_line + "\n|\n"

	return output

'''
	This function does the following:
	- Removes @ and #
	- Removes all html links
'''
def remove_unwanted(line):
	# Removes @ sign from usernames
	pattern = r"(@<.*?tweet-url username.*?>(.*?)<.*?>)"
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), i.group(2))

	# Removes # from hash-tags
	pattern = r"(<.*?tweet-url hashtag.*?>#(.*?)<.*?>)"
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), i.group(2))

	# Removes http, www and other links
	pattern = r"(<.*?>.*?<.*?>)"
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), '')

	return line

'''
	Adds spaces infront and behind of all ellipsis.
	I consider ellipsis to be any punctuation from the list: [., ?, !]
	which is repeated more than once in a row.
'''
def find_ellipsis(line):
	pattern = r"((\w+)(\s?)(!+|\?+|\.\.+))"
	m = re.finditer(pattern, line)
	for i in m:
		line = line.replace(i.group(1), i.group(2) + ' ' + i.group(4) + ' ')
	
	return line

'''
	Tags the tokens with tags using NLPlib.
'''
def tag_tokens(line):
	token_list = re.split(r" +", line.strip())
	tags = tagger.tag(token_list)

	new_line = ""
	for i in range(len(tags)):
		if token_list[i] != "\n":
			new_line = new_line + token_list[i] + "/" + tags[i] + " "
		else:
			new_line = new_line + "\n"
	return new_line

'''
	Parses each tweet and attempts to split the tweet into
	proper sentences. Splits into sentences if one of the for
	following characters occure: [., ?, !]
'''
def find_end_of_sentence(line):
	pattern = r"((\w+)\s?\.\s?)((\w+\.)?)+"
	m = re.finditer(pattern, line)
	# This is to handle the . case
	for i in m:
		if i.group(3).count('.') == 0:
			if not (i.group(1).lower() in open('/u/cs401/Wordlists/pn_abbrev.english').read().lower() or i.group(1).lower() in open('/u/cs401/Wordlists/abbrev.english').read().lower()):
				# Two above checks are to see if it is an abbreviation
				# THIS MIGHT FAIL IF THE ABBREV FILES ARE NOT FOUND!
				if not bool(re.compile('\d').search(i.group(1))):
					# Adove check is to see if it a decimal number

					# NOTE: I do not check for cases where the period is
					# within " ", since this case is not difficult to handle
					# becuase of the randomness/correctness of sentece structure
					# and tweets
					line = line.replace(i.group(1), i.group(2) + ' . \n')

	pattern = r'(\w+\s?\?+)(\s?)'
	m = re.finditer(pattern, line)
	# This is to handle the ? case
	for i in m:
		line = line.replace(i.group(1) + i.group(2), i.group(1) + ' \n')

	pattern = r'(\w+\s?!+)(\s?)'
	m = re.finditer(pattern, line)
	# This is to handle the ! case
	for i in m:
		line = line.replace(i.group(1) + i.group(2), i.group(1) + ' \n')

	return line

'''
	Seperates punctuation by putting a space infront and behind each
	single punctuation character. The cases of [., ?, !] are taken
	care of elsewhere and are not included in this function.
'''
def sep_punctuation(line):
	pattern = r"((\w+)(\s?)([\W]))(\s?)"
	m = re.finditer(pattern, line)
	for i in m:
		# It is a special case for ' - because of possessive and
		# abbreviation cases
		if i.group(4) == '\'':
			line = line.replace(i.group(1), i.group(2) + ' ' + i.group(4))
		elif i.group(4) != ' ' and i.group(4) != '.' and i.group(4) != '?' and i.group(4) != '!':
			line = line.replace(i.group(4), ' ' + i.group(4) + ' ')

	return line

'''
	Replaces all html codes within the tweets with the appropriate
	symboles. The only symboles which are changed are listed in the
	dictionary inside the function + '&'.
'''
def replace_ascii(line):
	dict = {
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

	line  = re.sub(r'&amp;', '&', line)
	for i in dict.keys():
		line = re.sub(r''+ i +'', dict[i], line)

	return line

if __name__ == "__main__":
	main()