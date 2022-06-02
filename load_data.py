import copy
"""
tcpdump query format :

timestamp 	  	|IPtype | from.port		   | to.port 				|queryID rdflag| qtype | name 			  | (query length)
13:24:21.778551 | IP 	|unamur032.55417 > |one.one.one.one.domain: |7107+ 		   |A? 	   |xhamster18.desi.  |(33)

"""
bots_query_type = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict(), "queryID":dict()}
bots_answer_type = {"queryID":dict(), "answer_list":dict(), "flags":dict()} 

human_query_type = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict(), "queryID":dict()}
human_answer_type = {"queryID":dict(), "answer_list":dict(), "flags":dict()}

hybrid_query = None
hybrid_answer = None


def load_training(bots_file, webclients_file):

	bot_f = open(bots_file, 'r')
	bot_lines = bot_f.readlines()
	
	for line in bot_lines:
		l_tab = line.split(" ")
		if "Flags" in l_tab:		#to change (temporary bandage)
			continue
		
		if "unamur" in l_tab[2]: #this is a query
			the_host = l_tab[2].split('.')[0]
			if the_host not in bots_query_type["hosts"]:
				bots_query_type["hosts"].append(the_host)
				
				bots_query_type["query_timestamp"][the_host] = [l_tab[0]]
				bots_query_type["qtype"][the_host] = [l_tab[6].split('?')[0]]
				bots_query_type["name"][the_host] = [l_tab[7]]
				bots_query_type["len"][the_host] = [l_tab[-1].split('(')[1].split(')')[0]] #that's ugly :(
				bots_query_type["queryID"][the_host] = [l_tab[5].split('+')[0]]
				
			else:
				bots_query_type["query_timestamp"][the_host].append(l_tab[0])
				bots_query_type["qtype"][the_host].append(l_tab[6].split('?')[0])
				bots_query_type["name"][the_host].append(l_tab[7])
				bots_query_type["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
				bots_query_type["queryID"][the_host].append(l_tab[5].split('+')[0])
			
		else : #this is the answer to a previous query
			the_host = l_tab[4].split('.')[0]
			
			(answer_list, flags) = get_answer_list(l_tab[6:])
			
			if the_host not in bots_answer_type["queryID"].keys():
				bots_answer_type["queryID"][the_host] = [l_tab[5]]
				bots_answer_type["answer_list"][the_host] = [answer_list]
				bots_answer_type["flags"][the_host] = [flags]
					
			else:
				bots_answer_type["queryID"][the_host].append(l_tab[5])
				bots_answer_type["answer_list"][the_host].append(answer_list)
				bots_answer_type["flags"][the_host].append(flags)
				
	global hybrid_query, hybrid_answer
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
				human_query_type["queryID"][the_host] = [l_tab[5].split('+')[0]]
				
			else:
				human_query_type["query_timestamp"][the_host].append(l_tab[0])
				human_query_type["qtype"][the_host].append(l_tab[6].split('?')[0])
				human_query_type["name"][the_host].append(l_tab[7])
				human_query_type["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
				human_query_type["queryID"][the_host].append(l_tab[5].split('+')[0])
				
			if the_host in hybrid_query["hosts"]:
				hybrid_query["query_timestamp"][the_host].append(l_tab[0])
				hybrid_query["qtype"][the_host].append(l_tab[6].split('?')[0])
				hybrid_query["name"][the_host].append(l_tab[7])
				hybrid_query["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
				hybrid_query["queryID"][the_host].append(l_tab[5].split('+')[0])
			
		else : #this is the answer to a previous query
			the_host = l_tab[4].split('.')[0]
			
			(answer_list, flags) = get_answer_list(l_tab[6:])
			
			if the_host not in human_answer_type["queryID"].keys():
				human_answer_type["queryID"][the_host] = [l_tab[5]]
				human_answer_type["answer_list"][the_host] = [answer_list]
				human_answer_type["flags"][the_host] = [flags]
					
			else:
				human_answer_type["queryID"][the_host].append(l_tab[5])
				human_answer_type["answer_list"][the_host].append(answer_list)
				human_answer_type["flags"][the_host].append(flags)
				
			if the_host in hybrid_answer["queryID"].keys():
				hybrid_answer["queryID"][the_host].append(l_tab[5])
				hybrid_answer["answer_list"][the_host].append(answer_list)
				hybrid_answer["flags"][the_host].append(flags)
			

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
			zipped = sorted(zip(
					hybrid_query["query_timestamp"][host], 
					hybrid_query["qtype"][host], 
					hybrid_query["name"][host], 
					hybrid_query["len"][host], 
					hybrid_query["queryID"][host],
					))
			
			timestamps, qtype, name, lengths, queryID = zip(*zipped)
		
			hybrid_query["query_timestamp"][host] = timestamps
			hybrid_query["qtype"][host] = qtype
			hybrid_query["name"][host] = name
			hybrid_query["len"][host] = lengths
			hybrid_query["queryID"][host] = queryID
		
		return (hybrid_query, hybrid_answer)
	else:
		return (None, None)


def get_eval_dataset(eval_file):
	eval_query = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict(), "queryID":dict()}
	eval_answers = {"queryID":dict(), "answer_list":dict(), "flags":dict()}

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
				eval_query["queryID"][the_host] = [l_tab[5].split('+')[0]]
				
			else:
				eval_query["query_timestamp"][the_host].append(l_tab[0])
				eval_query["qtype"][the_host].append(l_tab[6].split('?')[0])
				eval_query["name"][the_host].append(l_tab[7])
				eval_query["len"][the_host].append(l_tab[-1].split('(')[1].split(')')[0])
				eval_query["queryID"][the_host].append(l_tab[5].split('+')[0])
			
		else : #this is the answer to a previous query
			the_host = l_tab[4].split('.')[0]
			
			(answer_list, flags) = get_answer_list(l_tab[6:])
			
			if the_host not in eval_answers["queryID"].keys():
				eval_answers["queryID"][the_host] = [l_tab[5]]
				eval_answers["answer_list"][the_host] = [answer_list]
				eval_answers["flags"][the_host] = [flags]
			else:
				eval_answers["queryID"][the_host].append(l_tab[5])
				eval_answers["answer_list"][the_host].append(answer_list)
				eval_answers["flags"][the_host].append(flags)

	return (eval_query, eval_answers)


def get_answer_list(l_tab):
	#example : 5/0/0 A 104.19.141.69, A 104.19.143.69, A 104.19.142.69, A 104.19.128.70, A 104.19.129.70 (108)
	if "NXDomain" in l_tab or "ServFail" in l_tab or "NXDomain*" in l_tab:
		return ([], l_tab[1])
	else:
		return (l_tab[1:-1], l_tab[0])
		
		
		
		
		
