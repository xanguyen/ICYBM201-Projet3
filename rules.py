import numpy as np
import string

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
def max_number_of_special_char_in_domain(domain_list):
	max_num = 0
	
	for domain in domain_list:
		count = 0
		for c in domain:
			if not c.isalnum() and not c in string.punctuation:
				count += 1

		if count > max_num:
			max_num = count

	return max_num

# returns the average number of punctuation characters in domain names queried by a host 
def average_number_of_punctuation_char_in_domain(domain_list):
	count = 0
	for domain in domain_list:
		for c in domain:
			if c in string.punctuation:
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

# returns 1 if the amount of seconds between the first and the last query of a host is less than 1500
#		  0 therwise
def first_last_window(timestamps):
	first = timestamps[0].split(":")
	last = timestamps[-1].split(":")

	first_in_sec = int(int(first[0]) * 3600 + int(first[1]) * 60 + float(first[2]))
	last_in_sec = int(int(last[0]) * 3600 + int(last[1]) * 60 + float(last[2]))


	if (last_in_sec - first_in_sec) < 1500:
		return 1
	else:
		return 0

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

# returns 1 if the number of query with no answers / total answers > 0.15
#		  0 otherwise
def no_answer_num(flag_list):
	count = 0
	for flag in flag_list:
		if flag[0] == '0':
			count += 1

	if count/len(flag_list) > 0.15:
		return 1
	else:
		return 0
	
# returns the most queried domain proportion (compared to the total queries) of a host
def most_queried_domain_prop(domain_list):
	max_num = 0

	for domain1 in domain_list:
		count = 0
		for domain2 in domain_list:
			if domain1 == domain2:
				count += 1
		if count > max_num:
			max_num = count

	return round(count/len(domain_list), 4)