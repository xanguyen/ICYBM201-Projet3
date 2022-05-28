import copy
"""
tcpdump query format :

timestamp 	  	|IPtype | from.port		   | to.port 				|queryID rdflag| qtype | name 			  | (query length)
13:24:21.778551 | IP 	|unamur032.55417 > |one.one.one.one.domain: |7107+ 		   |A? 	   |xhamster18.desi.  |(33)

"""
bots_query_type = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict()}
bots_answer_type = None

human_query_type = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict()}
human_answer_type = None

hybrid_query = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict()}
hybrid_answer = None


def load_training(bots_file, webclients_file):

	bot_f = open(bots_file, 'r')
	bot_lines = bot_f.readlines()
	
	for line in bot_lines:
		l_tab = line.split(" ")
		
		if "unamur" in l_tab[2]: #this is a query
			the_host = l_tab[2].split('.')[0]
			if the_host not in bots_query_type["hosts"]:
				bots_query_type["hosts"].append(the_host)
				
				bots_query_type["query_timestamp"][the_host] = [l_tab[0]]
				bots_query_type["qtype"][the_host] = [l_tab[6].split('?')[0]]
				bots_query_type["name"][the_host] = [l_tab[7]]
				bots_query_type["len"][the_host] = [l_tab[-1].split('(')[1].split(')')[0]] #that's ugly :(
				
			else:
				bots_query_type["query_timestamp"][the_host].append(l_tab[0])
				bots_query_type["qtype"][the_host].append(l_tab[6].split('?')[0])
				bots_query_type["name"][the_host].append(l_tab[7])
				bots_query_type["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
			
		else : #this is the answer to a previous query
			pass
			#TODO
			
	global hybrid_query
	hybrid_query = copy.deepcopy(bots_query_type)
	hybrid_answer = copy.deepcopy(bots_answer_type)
	
	webc_f = open(webclients_file, 'r')
	webc_lines = webc_f.readlines()
	
	for line in webc_lines:
		l_tab = line.split(" ")
		if "Flags" in l_tab:		#to change (temporary bandage)
			continue
		
		if "unamur" in l_tab[2]: #this is a query
			the_host = l_tab[2].split('.')[0]
			if the_host not in human_query_type["hosts"]:
				human_query_type["hosts"].append(the_host)
				
				human_query_type["query_timestamp"][the_host] = [l_tab[0]]
				human_query_type["qtype"][the_host] = [l_tab[6].split('?')[0]]
				human_query_type["name"][the_host] = [l_tab[7]]
				human_query_type["len"][the_host] = [l_tab[-1].split('(')[1].split(')')[0]] #that's ugly :(
				
			else:
				human_query_type["query_timestamp"][the_host].append(l_tab[0])
				human_query_type["qtype"][the_host].append(l_tab[6].split('?')[0])
				human_query_type["name"][the_host].append(l_tab[7])
				human_query_type["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
				
			if the_host in hybrid_query["hosts"]:
				hybrid_query["query_timestamp"][the_host].append(l_tab[0])
				hybrid_query["qtype"][the_host].append(l_tab[6].split('?')[0])
				hybrid_query["name"][the_host].append(l_tab[7])
				hybrid_query["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
			
		else : #this is the answer to a previous query
			pass
			#TODO
			

def get_training_dataset_for(target):
	if target == 0: #bot
		return (bots_query_type, bots_answer_type)
	elif  target == 1: #human
		return (human_query_type, human_answer_type)
	elif target == 2: #hybrid
		for host in hybrid_query["hosts"]:
			"""
			if len(hybrid_query["qtype"][host]) > 2 * len(bots_query_type["qtype"][host]):
				l = 2 * len(bots_query_type["qtype"][host])
				zipped = sorted(zip(hybrid_query["query_timestamp"][host][:l], hybrid_query["qtype"][host][:l], hybrid_query["name"][host][:l], hybrid_query["len"][host][:l]))
			"""
			zipped = sorted(zip(hybrid_query["query_timestamp"][host], hybrid_query["qtype"][host], hybrid_query["name"][host], hybrid_query["len"][host]))
			
			timestamps, qtype, name, lengths = zip(*zipped)
		
			hybrid_query["query_timestamp"][host] = timestamps
			hybrid_query["qtype"][host] = qtype
			hybrid_query["name"][host] = name
			hybrid_query["len"][host] = lengths
		
		return (hybrid_query, hybrid_answer)
	else:
		return (None, None)


def get_eval_dataset(eval_file):
	eval_query = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict()}
	eval_answers = None

	eval_f = open(eval_file, 'r')
	eval_lines = eval_f.readlines()
	
	for line in eval_lines:
		l_tab = line.split(" ")
		if "Flags" in l_tab:		#to change (temporary bandage)
			continue
		
		if "unamur" in l_tab[2]: #this is a query
			the_host = l_tab[2].split('.')[0]
			if the_host not in eval_query["hosts"]:
				eval_query["hosts"].append(the_host)
				
				eval_query["query_timestamp"][the_host] = [l_tab[0]]
				eval_query["qtype"][the_host] = [l_tab[6].split('?')[0]]
				eval_query["name"][the_host] = [l_tab[7]]
				eval_query["len"][the_host] = [l_tab[-1].split('(')[1].split(')')[0]] #that's ugly :(
				
			else:
				eval_query["query_timestamp"][the_host].append(l_tab[0])
				eval_query["qtype"][the_host].append(l_tab[6].split('?')[0])
				eval_query["name"][the_host].append(l_tab[7])
				eval_query["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
			
		else : #this is the answer to a previous query
			pass
			#TODO

	return (eval_query, eval_answers)

#TODO : bots_answer_type, human_query_type, human_answer_type  (bots = from bots.pcap, human = from webclients.pcap)
