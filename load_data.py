"""
tcpdump query format :

timestamp 	  	|IPtype | from.port		   | to.port 				|queryID rdflag| qtype | name 			  | (query length)
13:24:21.778551 | IP 	|unamur032.55417 > |one.one.one.one.domain: |7107+ 		   |A? 	   |xhamster18.desi.  |(33)

"""
bots_query_type = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict()}
bots_answer_type = None

human_query_type = {"hosts": [], "query_timestamp":dict(), "qtype":dict(), "name":dict(), "len":dict()}
human_answer_type = None

def load(bots_file, webclients_file):
	bots_query_type["hosts"] = ["unamur021", "unamur032"]

	bots_query_type["query_timestamp"]["unamur021"] = ["13:22:44.546969", "13:23:43.649185", "13:23:46.905715", "13:24:03.501097", 
		"13:24:17.537724", "13:25:08.609675", "13:25:58.688820", "13:26:41.738336", "13:27:04.786223", "13:27:37.844408"]

	bots_query_type["query_timestamp"]["unamur032"] = ["13:22:45.573082", "13:23:14.647512", "13:24:01.734220", "13:24:21.778551",
		"13:24:32.816987", "13:25:48.341773", "13:26:55.375177", "13:27:50.457504", "13:28:20.756824"]

	bots_query_type["qtype"]["unamur021"] = ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A"]
	bots_query_type["qtype"]["unamur032"] = ["A", "A", "A", "A", "A", "A", "A", "A", "A"]

	bots_query_type["name"]["unamur021"] = ["kumparan.com.", "oschina.net.", "inven.co.kr.", "videocampaign.co.", "patreon.com.",
		"chaturbate.com.", "lenovo.com.", "animixplay.to.", "google.de.", "asurascans.com."]

	bots_query_type["name"]["unamur032"] = ["fast.com.", "thepaper.cn.", "india.com.", "xhamster18.desi.", "dytt8.net.", "fedex.com.",
		"cnnindonesia.com.", "sina.cn.", "arca.live."]

	bots_query_type["len"]["unamur021"] = ["30", "29", "29", "34", "29", "32", "28", "31", "27", "32"]
	bots_query_type["len"]["unamur032"] = ["26", "29", "27", "33", "27", "27", "34", "25", "27"]

def get_data_set_for(target):
	if target == 0: #bot
		return (bots_query_type, bots_answer_type)
	elif  target == 1: #human
		return (human_query_type, human_answer_type)
	else:
		return (None, None)

"""
for host in bots_query_type["hosts"]:
	for dic in bots_query_type:
		if type(bots_query_type[dic]) == type(dict()):
			print(len(bots_query_type[dic][host]))
"""
#TODO : bots_answer_type, human_query_type, human_answer_type  (bots = from bots.pcap, human = from webclients.pcap)
