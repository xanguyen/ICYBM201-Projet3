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


def evaluate_dataset(model, dataset, output_file):

    #the following ligne should change with get_eval_dataset
    (requests, answers) = ld.get_eval_dataset(dataset)
    X_eval = []

    #compute the features of the dataset
    for host in requests["hosts"]:
        evaluating_values = []
        
        evaluating_values.append(rules.average_dot_num_in_domain(requests["name"][host]))
        evaluating_values.append(rules.average_number_num_in_domain(requests["name"][host]))
        evaluating_values.append(rules.average_number_of_special_char_in_domain(requests["name"][host]))
        
        #evaluating_values.append(rules.num_request(requests["qtype"][host]))
        evaluating_values.append(rules.get_qtype_pourcentage(requests["qtype"][host], 'A'))
        evaluating_values.append(rules.get_qtype_pourcentage(requests["qtype"][host], 'AAAA'))
        evaluating_values.append(rules.get_qtype_pourcentage(requests["qtype"][host], 'CNAME'))
                
        evaluating_values.extend(rules.get_min_average_max_query_len(requests["len"][host]))
	
        evaluating_values.append(rules.min_time_btween_3_queries_window(requests["query_timestamp"][host]))
        evaluating_values.append(rules.first_last_window(requests["query_timestamp"][host]))

        #training_values.append(rules.average_query_num_answers(answers["ret_val"][host]))
        
        X_eval.append(evaluating_values)
        
        print(evaluating_values)

    #evaluate hosts using the model
    Y_eval = model.predict(X_eval)
    
    
    probas = model.predict_proba(X_eval)
    print(probas)
    
    
    #write in output_file the suspicious hosts
    k = 0
    f = open(output_file, "w")
    for evaluation in Y_eval:
        if evaluation == 0: #bot
            f.write(requests["hosts"][k] + '\n')
        elif evaluation == 2 :
        	print(requests["hosts"][k])
            
        k += 1
        
    f.close()


if __name__ == "__main__":

    args = parser.parse_args()

    if args.trained_model != None:
        #to load the classifier 
        RF_classifier = joblib.load(args.trained_model)
        evaluate_dataset(RF_classifier, args.dataset, args.output)

    else:
        print("please provide a trained_model")
        #RF_classifier = train.train_the_model(None)
