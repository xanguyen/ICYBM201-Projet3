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
	
# returns the [min, average, max] query length of a host
def get_min_average_max_query_len(len_list):
	the_min = len_list[0]
	the_max = len_list[0]
	count = 0
	for l in len_list:
		count += int(l)
		
	return [the_min, round(count/len(len_list), 1), the_max]

# returns the pourcentage of qtype (A, AAAA, CNAME, ...) in the list qtype_list (depending on its use, it can either be queried by a host, or found in query answers)
def get_qtype_pourcentage(qtype_list, qtype_asked):
	count = 0
	for qtype in qtype_list:
		if qtype == qtype_asked:
			count += 1

	return round(count/len(qtype_list), 2)

# returns the amount of milliseconds between the first and the last query of a host
def first_last_window(timestamps):
	first = timestamps[0].split(":")
	last = timestamps[-1].split(":")

	first_in_microsec = int((int(first[0]) * 3600 + int(first[1]) * 60 + float(first[2])) * 1000) 
	last_in_microsec = int((int(last[0]) * 3600 + int(last[1]) * 60 + float(last[2])) * 1000)


	return last_in_microsec - first_in_microsec

#returns the minimum time in milliseconds between 3 queries window of a host
def min_time_btween_3_queries_window(timestamps):
	min_time = -1
	for i in range(2, len(timestamps)):
		first = timestamps[i-2].split(":")
		last = timestamps[i].split(":")
		
		first_in_microsec = int((int(first[0]) * 3600 + int(first[1]) * 60 + float(first[2])) * 1000) 
		last_in_microsec = int((int(last[0]) * 3600 + int(last[1]) * 60 + float(last[2])) * 1000)

		if (min_time > (last_in_microsec - first_in_microsec) or min_time == -1):
			min_time = last_in_microsec - first_in_microsec

	return min_time
	
# returns the average number of answers queried by a host 
def average_query_num_answers(ret_val_list):
	count = 0
	for answer_list in ret_val_list:
		count += len(answer_list)
	
	return round(count/len(ret_val_list), 1)
	
	





