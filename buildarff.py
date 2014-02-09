import sys
import re

# Globals
master_output = []
class_names = {}
# Classes are the keys and their corresponding files
# are its values (which are stored in a list).
imported_features = []
other_features = ["upper_case", "avg_len_token", "avg_len_sentence", "num_sentence"]
# The order in which features will be attached are:
# fp_pronoun, sp_pronoun, tp_pronoun, coordinat_conj, past_tense_verbs,
# future_tense_verbs, commas, colons, dash, parentheses, ellipses,
# common_nouns, proper_nouns, adverbs, wh-words, modern_slang,
# upper_case, avg_len_token, avg_len_sentence, num_sentence

'''
	MAIN - Runs the program.
	- Parses parameters
	- Gather features
	- Parses tweet files for f
'''
def main():
	output_file, number_of_twt = parse_args(sys.argv[1:])
	get_features("features")
	parse_features(number_of_twt)
	write_output(output_file)

'''
	Actually writes the output_file arff file, using
	master_output. Both feature globals and the class_names
	are also used.
'''
def write_output(fname):
	# globals used
	global class_names
	global master_output
	global imported_features
	global other_features

	try:
		fw = open(fname, 'w')
	except:
		sys.stderr.write("Error while writing to file!\n")
		sys.exit()

	fw.write("@RELATION TWEET \n\n")

	for feature in imported_features:
		fw.write("@ATTRIBUTE " + feature[0] + "\t\tNUMERIC\n")

	for feature in other_features:
		fw.write("@ATTRIBUTE " + feature + "\t\tNUMERIC\n")

	fw.write("@ATTRIBUTE class\t\t{")
	cn = class_names.keys()
	for i in range(len(cn)):
		if i != len(cn) - 1:
			fw.write(cn[i] + ", ")
		else:
			fw.write(cn[i])
	fw.write("}\n\n")

	fw.write("@DATA\n")

	for tmp_lst in master_output:
		for i in range(len(tmp_lst)):
			if i != 20:
				fw.write(tmp_lst[i] + ", ")
			else:
				fw.write(tmp_lst[i])
		fw.write("\n")

'''
	Calculates the number of features for each tweet. As well as
	the upper_case feature and the avg_len_token featre. Returns
	all this data in the a list.
'''
def process_tweet(tweet_info):
	# The length of all tokens in the tweet
	total_token_len = 0
	# The number of tokens in the tweet
	number_of_tokens = 0
	# Number of capitalized words
	upper_case = 0

	tmp_output_data = []
	counter = 0

	for token in tweet_info:
		tmp_tk = re.split(r"/", token)

		if re.match(r"[A-Z][A-Z]+", tmp_tk[0]):
			# upper_case calculation
			upper_case = upper_case + 1

		if not re.match(r"[\W]+", tmp_tk[0]):
			# avg_len_token calculation
			number_of_tokens = number_of_tokens + 1
			total_token_len = total_token_len + len(token[0])

	for i in range(len(imported_features)):
		counter = 0
		for token in tweet_info:
			tmp_tk = re.split(r"/", token)

			if imported_features[i][1] == "words":
				if tmp_tk[0].lower() in imported_features[i][2]:
					counter = counter + 1
			elif imported_features[i][1] == "tags":
				if tmp_tk[1] in imported_features[i][2]:
					counter = counter + 1
		# Appends imported_features to the master_output
		tmp_output_data.append(str(counter))

	# Appends other_features to the master_output
	tmp_output_data.append(str(upper_case))
	if number_of_tokens != 0:
                tmp_output_data.append(str(total_token_len/number_of_tokens))
        else:
                tmp_output_data.append("0")

	return tmp_output_data

'''
	Parses the appropriate tweet files for feature according to 
	class_names, and then construcs a master_output of all the
	features.
'''
def parse_features(number_of_twt):
	global class_names
	global master_output

	for cn in class_names.keys():
		list_of_files = class_names[cn]
		for f in list_of_files:
			try:
				fr = open(f, 'r')
			except:
				sys.stderr.write("Error while reading file: " + f + "\n")
				continue
			
			# Keeps track how the number of tweets
			tweet_count = 0
			# Keeps track of the number of sentences
			num_sentence = 0
			# Keeps track of the length of the tweet
			twt_len = 0
			# The tokens/tags for each tweet
			tweet_info = []

			for line in fr:
				if line.strip() != '|':
					m_list = re.split(r" ", line)
					m_list.remove("\n")
					
					# Update feature information
					num_sentence = num_sentence + 1
					twt_len = twt_len + len(m_list)
					tweet_info = tweet_info + m_list					
				else:
					tmp_output_data = process_tweet(tweet_info)

					# Appends other_features to the master_output
					if num_sentence != 0:
						tmp_output_data.append(str(twt_len/num_sentence))
						# Calculate avg_len_sentence
					else:
						tmp_output_data.append("0")
					tmp_output_data.append(str(num_sentence))
					tmp_output_data.append(cn)

					# This is the final output to the arff file
					master_output.append(tmp_output_data)

					num_sentence = 0
					sentence_len = 0
					tweet_info = []

					tweet_count = tweet_count + 1
					if str(tweet_count) == str(number_of_twt):
						# This is for when the number of tweets to read
						# is specified.
						break

'''
	Reads in all features and all words and according tags for 
	those features. imported_features will store all this information and 
	will be used to 
'''
def get_features(fname):
	try:
		fr = open(fname, 'r')
	except:
		sys.stderr.write("Error while reading file: " + fname + "\n")
		sys.exit();

	for line in fr:
		tmp = eval(line)
		global imported_features # global used
		imported_features.append([tmp[0], tmp[1], tmp[2:]])
		# The format of imported_features is as follows:
		# tmp[0] - feature name
		# tmp[1] - type of the feature - words / tags
		# tmp[2:] - how to identify the feature

'''
	Parses the argument list and extracts the following:
	- Number of tweets per file, to be read
	- Classes and theiry associated files - global class_names
	- Output file, where the arff file will be written
'''
def parse_args(args):
	number = 0
	if len(args) > 1:
		output_file = args[len(args) - 1]
		
		m_one = re.search(r"-(\d+)", args[0])
		param_num = 1
		if m_one:
			# Specification of a certain set of tweets
			number = m_one.group(1)
			param_num = 2
		
		if param_num >= len(args):
			sys.stderr.write("Not enough parameters provided!\n")

		global class_names # global used
		for i in range(len(args)):
			m_two = re.split(r":", args[i])
			if len(m_two) == 1:
				# This is for the case: file1.twt
				m_three = re.search(r"(\w+).twt", m_two[0])
				if m_three:
					class_names[m_three.group(1)] = [m_two[0]]
			else:
				# This is for the case: class:file1.twt+file2.twt
				m_four = re.split(r"\+", m_two[1])
				if len(m_four) > 0:
					class_names[m_two[0]] = m_four

		return (output_file, number)
	else:
		sys.stderr.write("Not enough parameters provided!\n")

if __name__ == "__main__":
	main()