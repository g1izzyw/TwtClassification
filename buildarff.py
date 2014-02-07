import sys
import re

# Globals
number_of_lines = -1
class_names = {}
features = []

def main():
	parse_args(sys.argv[1:])
	get_features("features")
	get_lines()

	# Next we want to get all the features

def write_output():
	try:
		fw = open(fname, 'w')
		fw.write(output)
	except:
		sys.stderr.write("Error while writing to file!\n")

def get_lines():
	if number_of_lines == -1:
		for cn in class_names.keys():
			list_of_files = class_names[cn]
			for f in list_of_files:
				try:
					fr = open(f, 'r')
				except:
					sys.stderr.write("Error while reading file: " + f + "\n")
					sys.exit();
				
				for line in fr:
					output_list = [cn]
					if line.strip() != '|':
						
						m_list = re.split(r" ", line)
						print m_list

						for feature in features:


		# Then we are going to do the whole file
	#else:
		# Then we are going to do the number of lines
	return 1

def get_features(fname):
	try:
		fr = open(fname, 'r')
	except:
		sys.stderr.write("Error while reading file: " + fname + "\n")
		sys.exit();

	for line in fr:
		tmp = eval(line)
		tmp_tpl = (tmp[1], {tmp[0]:tmp[2:]})
		features.append(tmp_tpl)

def parse_args(args):
	if len(args) > 1:
		output_f = args[len(args) - 1]

		m_one = re.search(r"-(\d+)", args[0])
		i = 1
		if m_one:
			number_of_lines = m_one.group(1)
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
	else:
		sys.stderr.write("Not enough parameters provided!\n")

#[x for x in list1 if x in list2]
if __name__ == "__main__":
	main()