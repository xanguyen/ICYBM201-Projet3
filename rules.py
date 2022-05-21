def dot_num_in_domain(domain):
	count = 0
	for c in domain:
		if c == '.':
			count += 1

	return count

def number_num_in_domain(domain):
	count = 0
	for c in domain:
		if c.isdigit():
			count += 1

	return count 
	"""
	if count == 0:
		return 0
	elif count < 10:
		return 1
	else:
		return 2
	"""

def number_of_special_char_in_domain(domain):
	count = 0
	for c in domain:
		if not c.isalnum():
			count += 1

	return count 

def num_request(requests):
	return len(requests)
