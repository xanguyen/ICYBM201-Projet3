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
        
        evaluating_values.extend(rules.min_average_max_dot_num_in_domain(requests["name"][host]))
        evaluating_values.extend(rules.min_average_max_number_num_in_domain(requests["name"][host]))
        #evaluating_values.extend(rules.min_average_max_number_of_special_char_in_domain(requests["name"][host]))
        evaluating_values.extend(rules.min_average_max_number_of_punctuation_char_in_domain(requests["name"][host]))
        evaluating_values.append(rules.most_queried_domain_prop(requests["name"][host]))

        evaluating_values.append(rules.num_request(requests["qtype"][host]))
        evaluating_values.append(rules.get_query_qtype_pourcentage(requests["qtype"][host], 'A'))
        evaluating_values.append(rules.get_query_qtype_pourcentage(requests["qtype"][host], 'AAAA'))
        evaluating_values.append(rules.get_query_qtype_pourcentage(requests["qtype"][host], 'CNAME'))
        
        evaluating_values.append(rules.get_answer_qtype_pourcentage(answers["answer_list"][host], 'A'))
        evaluating_values.append(rules.get_answer_qtype_pourcentage(answers["answer_list"][host], 'AAAA'))
        #evaluating_values.append(rules.get_answer_qtype_pourcentage(answers["answer_list"][host], 'CNAME'))
                
        evaluating_values.extend(rules.get_min_average_max_query_len(requests["len"][host]))
	
        evaluating_values.append(rules.min_time_btween_3_queries_window(requests["query_timestamp"][host]))
        evaluating_values.append(rules.first_last_window(requests["query_timestamp"][host]))

        evaluating_values.append(rules.max_num_answers(answers["flags"][host]))
        evaluating_values.append(rules.no_answer_num(answers["flags"][host]))

        evaluating_values.append(rules.has_asnwer_to_all_queries(len(requests["qtype"][host]), len(answers["flags"][host])))
        evaluating_values.append(rules.different_answers_for_domain(
                requests["name"][host], 
                requests["queryID"][host], 
                requests["qtype"][host],
                answers["answer_list"][host], 
                answers["queryID"][host]))
        
        X_eval.append(evaluating_values)
        
        #print(evaluating_values)

    #evaluate hosts using the model
    Y_eval = model.predict(X_eval)
    
    
    probas = model.predict_proba(X_eval)
    #print(probas)
    
    the_sum = 0.0
    to_be_flagged = ["unamur05", "unamur031", "unamur02", "unamur015", "unamur15", "unamur128", "unamur115", "unamur111", "unamur24", "unamur236", "unamur232", "unamur233"]
    for i in range(len(probas)):
    	if requests["hosts"][i] in to_be_flagged:
    		print(requests["hosts"][i] + " : " + str(probas[i]))
    		the_sum += probas[i][2]
    
    print('the sum : ' + str(the_sum))
    #write in output_file the suspicious hosts
    k = 0
    f = open(output_file, "w")
    for evaluation in Y_eval:
        if evaluation == 0: #bot
            f.write(requests["hosts"][k] + '\n')
        elif probas[k][0] + probas[k][2] > probas[k][1] :
            print("flagged : "  + requests["hosts"][k])
            
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
