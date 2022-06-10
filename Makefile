
train:
	python3 train.py --webclients webclients.pcap --bots bots.pcap --output output.joblib

eval:
	python3 eval.py --dataset eval1.pcap --trained_model output.joblib --output output

lib_dl:
	pip3 install -r requirements.txt
