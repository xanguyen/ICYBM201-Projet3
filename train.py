import argparse
import pathlib
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

import rules
import load_data as ld


parser = argparse.ArgumentParser(description="Optional classifier training")
parser.add_argument("--webclients", required=True, type=pathlib.Path)
parser.add_argument("--bots", required=True, type=pathlib.Path)
parser.add_argument("--output", required=True, type=pathlib.Path)

def train_the_model(savefile):
    #declaring variables
    X_train = []
    Y_train = []
    bot = 0
    human = 1
    bot_and_human = 2

    #create/fill the training set

    for target in [bot, human, bot_and_human]:
        (requests, answers) = ld.get_training_dataset_for(target)
        
        for host in requests["hosts"]:
            training_values = []
            
            training_values.extend(rules.min_average_max_dot_num_in_domain(requests["name"][host]))
            training_values.extend(rules.min_average_max_number_num_in_domain(requests["name"][host]))
            #training_values.extend(rules.min_average_max_number_of_special_char_in_domain(requests["name"][host]))
            training_values.extend(rules.min_average_max_number_of_punctuation_char_in_domain(requests["name"][host]))
            training_values.append(rules.most_queried_domain_prop(requests["name"][host]))
            
            training_values.append(rules.num_request(requests["qtype"][host]))
            training_values.append(rules.get_query_qtype_pourcentage(requests["qtype"][host], 'A'))
            training_values.append(rules.get_query_qtype_pourcentage(requests["qtype"][host], 'AAAA'))
            #training_values.append(rules.get_query_qtype_pourcentage(requests["qtype"][host], 'CNAME'))
            
            
            training_values.append(rules.get_answer_qtype_pourcentage(answers["answer_list"][host], 'A'))
            training_values.append(rules.get_answer_qtype_pourcentage(answers["answer_list"][host], 'AAAA'))
            training_values.append(rules.get_answer_qtype_pourcentage(answers["answer_list"][host], 'CNAME'))
            
            training_values.extend(rules.get_min_average_max_query_len(requests["len"][host]))
            
            training_values.append(rules.min_time_btween_3_queries_window(requests["query_timestamp"][host]))
            training_values.append(rules.first_last_window(requests["query_timestamp"][host]))
            
            training_values.append(rules.max_num_answers(answers["flags"][host]))
            training_values.append(rules.no_answer_num(answers["flags"][host]))

            training_values.append(rules.has_asnwer_to_all_queries(len(requests["qtype"][host]), len(answers["flags"][host])))
            training_values.append(rules.different_answers_for_domain(
                requests["name"][host], 
                requests["queryID"][host], 
                requests["qtype"][host],
                answers["answer_list"][host], 
                answers["queryID"][host]))

            X_train.append(training_values)
            Y_train.append(target)
            
            #print(training_values)

    #create and train/fit the classifier
    classifier = RandomForestClassifier()
    classifier.fit(X_train, Y_train)

    print(classifier.feature_importances_)

    #save the trained classifier if savefile != None, else return the classifier (for eval.py)
    if savefile != None:
        joblib.dump(classifier, savefile)
    else:
        return classifier


    
if __name__ == "__main__":

    args = parser.parse_args()
    ld.load_training(args.bots, args.webclients)

    train_the_model(args.output)
