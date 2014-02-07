import sys
import re

# Globals
number_of_rlines = -1
class_names = {}
# class name is constructed so that the classes are the keys and their corresponding files
# files are its values (which are stored in a list)
imported_features = []
other_features = ["upper_case", "avg_len_token", "avg_len_sentence", "num_sentence"]

master_output = []
# The order in which features will be attached are:
# fp_pronoun, sp_pronoun, tp_pronoun, coordinat_conj, past_tense_verbs,
# future_tense_verbs, commas, colons, dash, parentheses, ellipses,
# common_nouns, proper_nouns, adverbs, wh-words, modern_slang,
# upper_case, avg_len_token, avg_len_sentence, num_sentence

def main():
	output_f = parse_args(sys.argv[1:])
	get_features("features")
	get_lines()
	write_output(output_f)

	# Next we want to get all the features

def write_output(fname):
	print fname
	try:
		fw = open(fname, 'w')
	except:
		sys.stderr.write("Error while writing to file!\n")
		sys.exit()

	fw.write("@RELATION TWEET \n\n")

	for feature in imported_features:
		fw.write("@ATTRIBUTE " + feature[0] + " NUMERIC\n")

	for feature in other_features:
		fw.write("@ATTRIBUTE " + feature + " NUMERIC\n")

	fw.write("@ATTRIBUTE class {")
	cn = class_names.keys()
	for i in range(len(cn)):
		if i != len(cn) - 1:
			fw.write(cn[i] + ",")
		else:
			fw.write(cn[i])
	fw.write("}\n\n")

	fw.write("@DATA\n")

	for tmp_lst in master_output:
		for i in range(len(tmp_lst)):
			if i != 20:
				fw.write(tmp_lst[i] + ",")
			else:
				fw.write(tmp_lst[i])
		fw.write("\n")

def process_tweet(tweet_info):

	# This value will be calculated by the process_tweet function
	# as it is calculating all the values for imported_features.
	total_token_len = 0
	number_of_tokens = 0

	upper_case = 0
	tmp_output_data = []
	counter = 0

	for token in tweet_info:
		tmp_tk = re.split(r"/", token)

		if re.match(r"[A-Z][A-Z]+", tmp_tk[0]):
			upper_case = upper_case + 1

		if not re.match(r"[\W]+", tmp_tk[0]):
			#calculates everything needed to calculate average token  length
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
		tmp_output_data.append(str(counter))

	tmp_output_data.append(str(upper_case))
	# this is the average token length
	tmp_output_data.append(str(total_token_len/number_of_tokens))

	return tmp_output_data

def get_lines():
	#if number_of_rlines == -1:
	for cn in class_names.keys():
		list_of_files = class_names[cn]
		for f in list_of_files:
			try:
				fr = open(f, 'r')
			except:
				sys.stderr.write("Error while reading file: " + f + "\n")
				continue
			
			tweet_count = 0
			# Keeps track of the tweets processed.

			num_sentence = 0
			# A simple counter as we move from one sentence to the next
			# in a tweet.

			sentence_len = 0
			# avg_len_sentence will be calculated by adding up all the
			# numbers in sentence_len_list and diving that number by the
			# num_sentence value.

			tweet_info = []
			# Will store all the tokens and their tags for each tweet and
			# will be passed into process_tweet.

			for line in fr:
				if line.strip() != '|':
					m_list = re.split(r" ", line)
					m_list.remove("\n")
					
					num_sentence = num_sentence + 1
					sentence_len = sentence_len + len(m_list)
					
					tweet_info = tweet_info + m_list					
				else:
					tmp_output_data = process_tweet(tweet_info)
					# This will return the average length of tokens
					# retreve al the information and store it somewhere.
					
					# This is where we want to add all the information

					# This is the average sentece length
					tmp_output_data.append(str(sentence_len/num_sentence))
					# This is the number of sentences per tweet
					tmp_output_data.append(str(num_sentence))
					# This is the class name being attached
					tmp_output_data.append(cn)

					# This is the final output to the arff file
					master_output.append(tmp_output_data)

					num_sentence = 0
					sentence_len = 0
					tweet_info = []

					tweet_count = tweet_count + 1
					if tweet_count == number_of_rlines:
						# This is for when the number of tweets to read
						# is specified.
						break

def get_features(fname):
	try:
		fr = open(fname, 'r')
	except:
		sys.stderr.write("Error while reading file: " + fname + "\n")
		sys.exit();

	for line in fr:
		tmp = eval(line)
		imported_features.append([tmp[0], tmp[1], tmp[2:]])
			#tmp 1 has the feature name
			# tmp 0 has if its a word tag or both
			# tmo 2 and onwards has all the tags associated with it
	#print imported_features

def parse_args(args):
	if len(args) > 1:
		output_f = args[len(args) - 1]

		m_one = re.search(r"-(\d+)", args[0])
		i = 1
		if m_one:
			number_of_rlines = m_one.group(1)
			i = 2
		
		if i >= len(args):
			sys.stderr.write("Not enough parameters provided!\n")

		for j in range(0, len(args) - 1):
			m_two = re.split(r":", args[j])
			if len(m_two) == 1:
				m_three = re.search(r"(\w+).twt", m_two[0])
				if m_three:
					class_names[m_three.group(1)] = [m_two[0]]
			else:
				# If we get here its the case that m_two = [pop, ""]
				m_four = re.split(r"\+", m_two[1])
				if len(m_four) > 0:
					class_names[m_two[0]] = m_four
		return output_f
	else:
		sys.stderr.write("Not enough parameters provided!\n")

#[x for x in list1 if x in list2]
if __name__ == "__main__":
	main()