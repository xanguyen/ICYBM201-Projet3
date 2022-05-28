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

# returns the pourcentage of qtype (A, AAAA, CNAME, ...) in the QUERY list qtype_list 
def get_query_qtype_pourcentage(qtype_list, qtype_asked):
	count = 0
	for qtype in qtype_list:
		if qtype == qtype_asked:
			count += 1

	return round(count/len(qtype_list), 2)
	
# returns the pourcentage of qtype (A, AAAA, CNAME, ...) in the ANSWER list answer_list 
def get_answer_qtype_pourcentage(answer_list, qtype_asked):
	count = 0
	num_tot = 0
	for answers in answer_list:
		if len(answers) == 0:
			num_tot += 1
			continue
		
		for answer in answers:
			if answer == qtype_asked:
				count += 1
			num_tot += 1
	
	if num_tot == 0:
		num_tot = 1
	return round(count/num_tot, 2)

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
	
# returns the max number of answers queried by a host 
def max_num_answers(flag_list):
	the_max = int(flag_list[0].split('/')[0])
	for flag in flag_list:
		num_ans = int(flag.split('/')[0])
		if the_max < num_ans:
			the_max = num_ans
	
	return the_max
	
	





