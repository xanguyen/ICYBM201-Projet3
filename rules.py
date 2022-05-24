import numpy as np

def average_dot_num_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if c == '.':
				count += 1

	return count/len(domain_list)

def average_number_num_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if c.isdigit():
				count += 1

	return count/len(domain_list)

def average_number_of_special_char_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if not c.isalnum():
				count += 1

	return count/len(domain_list)

def num_request(requests):
	return len(requests)

def get_dominant_qtype(qtype_list):
	counter_dict = {}
	for qtype in qtype_list:
		if qtype in counter_dict.keys():
			counter_dict[qtype] += 1
		else:
			counter_dict[qtype] = 0

	the_max = max(counter_dict, key=counter_dict.get)
	ret_val = 0
	for c in the_max:
		ret_val = ret_val + ord(c)

	return ret_val


def first_last_window(timestamps):
	first = timestamps[0].split(":")
	last = timestamps[-1].split(":")

	first_in_microsec = int((int(first[0]) * 3600 + int(first[1]) * 60 + float(first[2])) * 1000000) 
	last_in_microsec = int((int(last[0]) * 3600 + int(last[1]) * 60 + float(last[2])) * 1000000)


	return last_in_microsec - first_in_microsec