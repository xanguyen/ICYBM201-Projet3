
train:
	python3 train.py --webclients webclients.pcap --bots bots.pcap --output output.joblib

eval:
	python3 eval.py --dataset eval2.pcap --trained_model output.joblib --output output

lib_dl:
	pip3 install -r requirements.txt
