import numpy as np

# returns the average number of dots in domain names queried by a host 
def average_dot_num_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if c == '.':
				count += 1

	return round(count/len(domain_list), 1)

# returns the average number of numerical characters in domain names queried by a host 
def average_number_num_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if c.isdigit():
				count += 1

	return round(count/len(domain_list), 1)

# returns the average number of special characters in domain names queried by a host 
def average_number_of_special_char_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if not c.isalnum():
				count += 1

	return round(count/len(domain_list), 1)

# returns the number of queries done by a host
def num_request(requests):
	return len(requests)
	
# returns the average query length of a host
def get_average_query_len(len_list):
	count = 0
	for l in len_list:
		count += int(l)
		
	return round(count/len(len_list), 1)

# returns the qtype (A, AAAA, CNAME, ...) that is dominant in the list qtype_list (depending on its use, it can either be the most often queried by a host,
# or the most often found in query answers)
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

# returns the amount of milliseconds between the first and the last query of a host
def first_last_window(timestamps):
	first = timestamps[0].split(":")
	last = timestamps[-1].split(":")

	first_in_microsec = int((int(first[0]) * 3600 + int(first[1]) * 60 + float(first[2])) * 1000) 
	last_in_microsec = int((int(last[0]) * 3600 + int(last[1]) * 60 + float(last[2])) * 1000)


	return last_in_microsec - first_in_microsec
	
# returns the average number of answers queried by a host 
def average_query_num_answers(ret_val_list):
	count = 0
	for answer_list in ret_val_list:
		count += len(answer_list)
	
	return round(count/len(ret_val_list), 1)
	
	





