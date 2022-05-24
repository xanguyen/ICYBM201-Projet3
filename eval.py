import argparse
import pathlib
import joblib

import train
import load_data as ld
import rules


parser = argparse.ArgumentParser(description="Dataset evaluation")
parser.add_argument("--dataset", required=True, type=pathlib.Path)
parser.add_argument("--trained_model", type=pathlib.Path)
parser.add_argument("--output", required=True, type=pathlib.Path)


def evaluate_dataset(model, output_file):

    #the following ligne should change with get_eval_dataset
    (requests, answers) = ld.get_training_dataset_for(0)
    X_eval = []

    #compute the features of the dataset
    for host in requests["hosts"]:
        evaluating_values = []
        evaluating_values.append(rules.average_dot_num_in_domain(requests["name"][host]))
        evaluating_values.append(rules.average_number_num_in_domain(requests["name"][host]))
        evaluating_values.append(rules.average_number_of_special_char_in_domain(requests["name"][host]))
        evaluating_values.append(rules.num_request(requests["qtype"][host]))
        evaluating_values.append(rules.get_dominant_qtype(requests["qtype"][host]))

        evaluating_values.append(rules.first_last_window(requests["query_timestamp"][host]))

        print(evaluating_values)
        X_eval.append(evaluating_values)

    #evaluate hosts using the model
    Y_eval = model.predict(X_eval)

    #write in output_file the suspicious hosts
    f = open(output_file, "w")
    for (evaluation, host) in (Y_eval, requests["hosts"]):
        if evaluation == 0: #bot
            f.write(host)
    f.close()


if __name__ == "__main__":

    args = parser.parse_args()
    
    #load datasets
    ld.load_training("bots.pcap", "webclients.pcap")

    if args.trained_model != None:
        #to load the classifier 
        RF_classifier = joblib.load(args.trained_model)
        evaluate_dataset(RF_classifier, args.output)

    else:
        print("please provide a trained_model")
        #RF_classifier = train.train_the_model(None)
