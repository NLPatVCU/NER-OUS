#!/usr/bin/python3

import sys
import os
import subprocess
import configparser
import getopt
import datetime
from random import sample

import numpy as np

import agent
import helpers
from classes import SentenceStructure, Annotation, BatchContainer
from preprocess import preprocess

def check_config_file(config):
    """
    Checks configuration file for sanity. Will exit if it is not correct.

    :param config: A configuration instance from configparser to check.
    :return: Nothing.
    """
    if not 'MAX_SENTENCE_LENGTH' in config:
        print("Missing MAX_SENTENCE_LENGTH in config.ini.")
        sys.exit(0)
        
    if not 'USE_SEMANTIC_TYPES' in config:
        print("Missing USE_SEMANTIC_TYPES in config.ini.")
        sys.exit(0)
        
    elif config['USE_SEMANTIC_TYPES'] == '1':
        if not 'SEMANTIC_ANNOTATION_FILE_PATH' in config:
            print("Missing SEMANTIC_ANNOTATION_FILE_PATH in config.ini.")
            sys.exit(0)
            
        if not 'OVERRIDE_SEMANTIC_ANNOTATIONS' in config:
            print("Missing OVERRIDE_SEMANTIC_ANNOTATIONS in config.ini.")
            sys.exit(0)
            
        if not 'METAMAP_PATH' in config:
            print("Missing METAMAP_PATH in config.ini.")
            sys.exit(0)
        
    if not 'EMBEDDING_SIZE' in config:
        print("Missing EMBEDDING_SIZE in config.ini")
        sys.exit(0)

    if not 'EMBEDDING_FILE' in config:
        print("Missing EMBEDDING_FILE in config.ini")
        sys.exit(0)

    if not 'ANNOTATION_FILE_PATH' in config:
        print("Missing ANNOTATION_FILE_PATH in config.ini")
        sys.exit(0)

    if not 'RAW_FILE_PATH' in config:
        print("Missing RAW_FILE_PATH in config.ini")
        sys.exit(0)

    if not 'BUCKETS' in config:
        print("Missing BUCKETS in config.ini")
        sys.exit(0)

    if not 'EPOCHS' in config:
        print("Missing EPOCHS in config.ini")
        sys.exit(0)

    if not 'CLASSES' in config:
        print("Missing CLASSES in config.ini")
        sys.exit(0)

def build_config_file(file_path):
    #Parse config file and set up configuration classes.
    config_file = configparser.ConfigParser()
    config_file.read_file(open(file_path))
    config_dict = config_file['Main']

    check_config_file(config_dict)
    
    config = {'CONFIGURATION': config_dict}
 
    feature_map = {"IS_NUM" : 0,
                   "IS_DATE" : 1,
                   "IS_TIME" : 2}
    if config['CONFIGURATION']['USE_SEMANTIC_TYPES'] == '1':
        feature_map['PROBLEM_ST'] = 3
        feature_map["TEST_ST"] = 4
        feature_map["TREATMENT_ST"] = 5
                                   
    config['FEATURE_MAP'] = feature_map
    config['CLASS_LIST'] = config['CONFIGURATION']['CLASSES'].split(',')
    
    config['CLASS_MAP'] = {}
    config['CLASS_MAP'][''] = 0
    for i, el in enumerate(config['CLASS_LIST']):
        config['CLASS_MAP'][el.lower()] = i+1

    config['NUM_FEATURES'] = int(config['CONFIGURATION']['EMBEDDING_SIZE']) + len(feature_map)
    
    return config

def main():
    """
    Main function of the application. Call -h or --help for command line inputs.
    """
    mode, output_directory, model_file = None, None, None
    
    #Process command line entries.
    opts, args = getopt.getopt(sys.argv[1:], 'm:i:o:d:a:h',["mode=","output=","model=","help"])
    for opt, arg, in opts:
        if opt in ("-m","--mode"):
            mode = arg
        elif opt in ("-o","--output"):
            output_directory = arg
        elif opt in ("-d","--model"):
            model_file = arg
        elif opt in ("-h","--help"):
            print_help()
            return
        
    #Verify if needed command line entries are present.
    if mode == None:
        print("You must specify a mode to use with -m or --mode. Options are train, eval, annotate, and analysis.")
        print("train creates a model file, eval evaluates annotated text using a model, annotate creates an annotation file using a model, and analysis runs k-fold cross validation using a training set.")
        return
        
    elif mode == "eval" and model_file == None:
        print("You must specify a model to use for evaluation using -d or --model.")
        return
        
    elif mode == 'annotate':
        if output_directory == None:
            print("You must specify a directory for output files with -o or --output.")
            return
        elif model_file == None:
            print("You must specify a model to use for evaluation using -d or --model.")
            return        

    #Parse config file and set up configuration classes.
    config = build_config_file('config.ini')
    
    if config['CONFIGURATION']['USE_SEMANTIC_TYPES'] == '1':
        helpers.build_semantic_type_annotations(config)
        
    if output_directory:
        config['CONFIGURATION']['OUTPUT_DIR'] = output_directory

    if mode == "annotate":
        file_sentence_dict, max_sentence_length = create_sentence_structures(config['CONFIGURATION']['RAW_FILE_PATH'])
        add_modified_sentence_array(file_sentence_dict)
        
        if max_sentence_length > int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']):
            config['CONFIGURATION']['MAX_SENTENCE_LENGTH'] = str(max_sentence_length)
        
        tx, ty, ts, tm = generate_embeddings(file_sentence_dict, config)
        train_batch_container = BatchContainer(tx, ty, ts, tm)
        
        annotate_network_model(train_batch_container, file_sentence_dict, config, model_file)
        
    else:
        #Iterate files and generate feature vectors.
        file_sentence_dict, max_sentence_length = create_annotated_sentence_structures(config['CONFIGURATION']['ANNOTATION_FILE_PATH'], config['CONFIGURATION']['RAW_FILE_PATH'])
        add_modified_sentence_array(file_sentence_dict)
        
        if max_sentence_length > int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']):
            config['CONFIGURATION']['MAX_SENTENCE_LENGTH'] = str(max_sentence_length)
            
        tx, ty, ts, tm = generate_embeddings(file_sentence_dict, config)
        train_batch_container = BatchContainer(tx, ty, ts, tm)
        if mode == "analysis":
            #Train the network with k-fold cross validation and report analysis.
            train_network_analysis(train_batch_container, file_sentence_dict, config)
        elif mode == "train":
            #Build a model file for exporting.
            train_network_model(train_batch_container, config)
        elif mode == "eval":
            evaluate_network_model(train_batch_container, file_sentence_dict, config, model_file)
        
    
def print_help():
    """
    Prints out the command line help information.
    """ 
    print("Options:")
    print("-m/--mode [train,eval,annotate,analysis] : Specify the mode of the system.")
    print("-o/--output DIR : Specify the output directory to write to.")
    print("-d/--model FILE : Specify a model to use when running in eval mode.")
    
    return

def annotate_network_model(train_batch_container, file_sentence_dict, config, model_file):
    buckets = int(config['CONFIGURATION']['BUCKETS'])
    trainer = agent.Agent(config['NUM_FEATURES'], len(config['CLASS_LIST'])+1, int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']))
    trainer.load_model(model_file)
    
    batch_x, batch_y, seq_len, batch_to_file_map = kfold_bucket_generator(train_batch_container.bx, train_batch_container.by, train_batch_container.bs, buckets)
    for i in range(0, buckets):
        trainer.build_annotations(batch_x[i], seq_len[i], train_batch_container.mapping, batch_to_file_map, file_sentence_dict, i, config)
    
    write_annotations(file_sentence_dict, config['CONFIGURATION']['OUTPUT_DIR'])
    
def evaluate_network_model(train_batch_container, file_sentence_dict, config, model_file):
    trainer = agent.Agent(config['NUM_FEATURES'], len(config['CLASS_LIST'])+1, int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']))
    trainer.load_model(model_file)
    
    batch_x, batch_y, seq_len, batch_to_file_map = kfold_bucket_generator(train_batch_container.bx, train_batch_container.by, train_batch_container.bs, 1)
    
    cm = [trainer.eval_token_level(batch_x[0], batch_y[0], seq_len[0])]
    pm = [trainer.eval_phrase_level(batch_x[0], seq_len[0], 0, train_batch_container.mapping, batch_to_file_map, file_sentence_dict, config)]

    post_correction_confusion_matrix = trainer.eval_token_level_from_dict(file_sentence_dict, config)
    
    #Run analysis generation.
    generate_analysis_file(cm, post_correction_confusion_matrix, pm, config)
    
def train_network_model(train_batch_container, config):
    """
    Trains a neural network model and saves it.

    :param train_batch_container: A BatchContainer object containing the data to be trained.
    :param config: A configuration instance from configparser.
    :return: Nothing.
    """
    epochs = int(config['CONFIGURATION']['EPOCHS'])
    buckets = int(config['CONFIGURATION']['BUCKETS'])
    trainer = agent.Agent(config['NUM_FEATURES'], len(config['CLASS_LIST'])+1, int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']))
    
    batch_x, batch_y, seq_len, batch_to_file_map = kfold_bucket_generator(train_batch_container.bx, train_batch_container.by, train_batch_container.bs, buckets)
    for k in range(0,epochs):
        loss = 0
        for i in range(0, buckets):
            loss += trainer.train(batch_x[i], batch_y[i], seq_len[i])
        print("Loss for Epoch " + str(k) + " is " + str(loss) + ".")
  
    trainer.save_model("./mimic_model/model.ckpt")    

def train_network_analysis(train_batch_container, file_sentence_dict, config, supplemental_batch=None):
    """
    Trains a neural network model and reports analysis usking k-fold cross validation.

    :param train_batch_container: A BatchContainer object containing the data to be trained.
    :param file_sentence_dict: Map containing SentenceStructures of all files in memory. Used for generating analysis.
    :param config: A configuration instance from configparser.
    :param supplemental_batch: A BatchContainer object containing optional data to be transfer learned. Defaults to None.
    :return: Nothing.
    """
    buckets = int(config['CONFIGURATION']['BUCKETS'])
    epochs = int(config['CONFIGURATION']['EPOCHS'])

    #Setup Buckets for k fold cross validation
    batch_x, batch_y, seq_len, batch_to_file_map = kfold_bucket_generator(train_batch_container.bx, train_batch_container.by, train_batch_container.bs, buckets)
        
    #TODO(Jeff) Clean up supplemental_batch information.
    if supplemental_batch:
        sup_batch_x, sup_batch_y, sup_seq_len, _ = kfold_bucket_generator(supplemental_batch.bx, supplemental_batch.by, supplemental_batch.bs, epochs)

    #Create and train the model for kFoldCrossValidation
    pre_correction_confusion_matrix_list = []
    phrase_matrix_list = []
    post_correction_confusion_matrix = None
    
    if buckets > 1:
        for k in range(0, buckets):
            trainer = agent.Agent(config['NUM_FEATURES'], len(config['CLASS_LIST'])+1, int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']))

            #Train supplemental for j epochs.
            if supplemental_batch:
                for j in range(0, epochs):
                    for l in range(0, epochs):
                        trainer.train(sup_batch_x[l], sup_batch_y[l], sup_seq_len[l])

            #Train normal for j epochs.
            for j in range(0, epochs):
                loss = 0

                #Train each bucket where l != current K
                for l in range(0, buckets):
                    if l == k:
                        continue
                    loss += trainer.train(batch_x[l], batch_y[l], seq_len[l])

                print("Loss for Epoch " + str(j) + " is " + str(loss) + ".")

            #Evaluate after training and store debugging files.
            cm = trainer.eval_token_level(batch_x[k], batch_y[k], seq_len[k])
            pre_correction_confusion_matrix_list.append(cm)

            file = open("./outCF", 'a')
            outstr = np.array2string(cm)
            file.write(outstr)
            file.write("\n")
            file.close()

            pm = trainer.eval_phrase_level(batch_x[k], seq_len[k], k, train_batch_container.mapping, batch_to_file_map, file_sentence_dict, config)
            phrase_matrix_list.append(pm)
            file = open("./outCFS", 'a')
            outstr = np.array2string(pm)
            file.write(outstr)
            file.write("\n")
            file.close()

            trainer.clean_up()
    else:
        trainer = agent.Agent(config['NUM_FEATURES'], len(config['CLASS_LIST'])+1, int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']))
        
        #Train supplemental for j epochs.
        if supplemental_batch:
            for j in range(0, epochs):
                trainer.train(sup_batch_x[0], sup_batch_y[0], sup_seq_len[0])
                    
        #Train normal for j epochs.
        for j in range(0, epochs):
            loss = trainer.train(batch_x[0], batch_y[0], seq_len[0])
            print("Loss for Epoch " + str(j) + " is " + str(loss) + ".")
        

    post_correction_confusion_matrix = agent.eval_token_level_from_dict(file_sentence_dict, config)
    
    #Run analysis generation.
    generate_analysis_file(pre_correction_confusion_matrix_list, post_correction_confusion_matrix, phrase_matrix_list, config)
    
def generate_analysis_file(pre_correction_confusion_matrix_list, post_correction_confusion_matrix, phrase_matrix_list, config):
    class_count = len(config['CLASS_LIST'])+1
    
    #Start with Majority Sense Baseline
    majority_sense_data = np.zeros((1, class_count), dtype=np.int32)
    for i in pre_correction_confusion_matrix_list:
        for j in range(0, class_count):
            for k in range(0, class_count):
                majority_sense_data[0, k] += i[j, k]   

    class_none_micro_precision = 1.0 * majority_sense_data[0, 0] / np.sum(majority_sense_data[0, :])
    class_none_micro_recall = 1.0
    class_none_micro_f1_score = 2 * (class_none_micro_precision/(class_none_micro_precision+1.0))

    class_none_macro_precision = class_none_micro_precision/class_count
    class_none_macro_recall = 1.0/class_count
    class_none_macro_f1_score = class_none_micro_f1_score/class_count   

    #Token Level Analysis
    pre_correction_confusion_matrix = np.zeros((class_count, class_count), dtype=np.int32)
    precision_micro_list = np.zeros((class_count, len(pre_correction_confusion_matrix_list)), dtype=np.float32)
    recall_micro_list = np.zeros((class_count, len(pre_correction_confusion_matrix_list)), dtype=np.float32)
    f1_micro_list = np.zeros((class_count, len(pre_correction_confusion_matrix_list)), dtype=np.float32)
    precision_macro_list = []
    recall_macro_list = []
    f1_macro_list = []    
    
    for i, cm in enumerate(pre_correction_confusion_matrix_list):
        for j in range(0, class_count):
            for k in range(0, class_count):
                pre_correction_confusion_matrix[j, k] += cm[j, k]
            precision_micro_list[j, i] = 1.0 * cm[j, j] / np.sum(cm[j, :])
            recall_micro_list[j, i] = 1.0 * cm[j, j] / np.sum(cm[:, j])
            f1_micro_list[j, i] = 2.0 * ((precision_micro_list[j, i] * recall_micro_list[j, i]) / (precision_micro_list[j, i] + recall_micro_list[j, i]))
            
        precision_macro_list.append((np.sum(precision_micro_list[:, i])/class_count))
        recall_macro_list.append((np.sum(recall_micro_list[:, i])/class_count))
        f1_macro_list.append((np.sum(f1_micro_list[:, i])/class_count))
        
    correction_difference_confusion_matrix = np.zeros((class_count, class_count), dtype=np.int32)
    for j in range(0, class_count):
        for k in range(0, class_count):
            correction_difference_confusion_matrix[j, k] = post_correction_confusion_matrix[j, k] - pre_correction_confusion_matrix[j, k]
        
    #Phrase Level Analysis
    strict_phrase_precision_micro_list = np.zeros((class_count-1, len(phrase_matrix_list)), dtype=np.float32)
    strict_phrase_recall_micro_list = np.zeros((class_count-1, len(phrase_matrix_list)), dtype=np.float32)
    strict_phrase_f1_micro_list = np.zeros((class_count-1, len(phrase_matrix_list)), dtype=np.float32)
    lenient_phrase_precision_micro_list = np.zeros((class_count-1, len(phrase_matrix_list)), dtype=np.float32)
    lenient_phrase_recall_micro_list = np.zeros((class_count-1, len(phrase_matrix_list)), dtype=np.float32)
    lenient_phrase_f1_micro_list = np.zeros((class_count-1, len(phrase_matrix_list)), dtype=np.float32)
    
    for i, cm in enumerate(phrase_matrix_list):
        for j in range(1, class_count):
            strict_phrase_precision_micro_list[j-1, i] = cm[j,0] / (cm[j,0] + cm[j,1] + cm[j,3])
            strict_phrase_recall_micro_list[j-1, i] = cm[j,0] / (cm[j,0] + cm[j,1] + cm[j,2])
            strict_phrase_f1_micro_list[j-1, i] = 2.0 * ((strict_phrase_precision_micro_list[j-1, i] * strict_phrase_recall_micro_list[j-1, i]) / (strict_phrase_precision_micro_list[j-1, i] + strict_phrase_recall_micro_list[j-1, i]))
            lenient_phrase_precision_micro_list[j-1, i] = (cm[j,0] + cm[j,1])  / (cm[j,0] + cm[j,1] + cm[j,3])
            lenient_phrase_recall_micro_list[j-1, i] = (cm[j,0] + cm[j,1]) / (cm[j,0] + cm[j,1] + cm[j,2])
            lenient_phrase_f1_micro_list[j-1, i] = 2.0 * ((lenient_phrase_precision_micro_list[j-1, i] * lenient_phrase_recall_micro_list[j-1, i]) / (lenient_phrase_precision_micro_list[j-1, i] + lenient_phrase_recall_micro_list[j-1, i]))                
            
    #Write Information to file
    file = open("./analysis.txt", 'a')
    file.write(str(datetime.datetime.now()) + '\n\n')
 
    file.write("===Majority Sense Baseline===\n")
    file.write("Micro Precision: \t" + str(class_none_micro_precision) + "\n")
    file.write("Micro Recall: \t" + str(class_none_micro_recall) + "\n")
    file.write("Micro F1: \t" + str(class_none_micro_f1_score) + "\n")
    file.write("Macro Precision: \t" + str(class_none_macro_precision) + "\n")
    file.write("Macro Recall: \t" + str(class_none_macro_recall) + "\n")
    file.write("Macro F1: \t" + str(class_none_macro_f1_score) + "\n\n")
    
    file.write("===Summary===\n\n")
     
    file.write("=Phrase Level=\n")
    file.write("CLASS \tSF1 \tLF1\n")
    for i in range(0, class_count-1):
        file.write(str(config['CLASS_LIST'][i]) + ' \t' + 
                       str(np.sum(strict_phrase_f1_micro_list[i,:])/len(phrase_matrix_list)) + ' \t' +
                       str(np.sum(lenient_phrase_f1_micro_list[i,:])/len(phrase_matrix_list)) + '\n')
    file.write("\n")
    
    file.write("=Token Level=\n")
    
    file.write("=Macro=\n")
    file.write("Macro F1 Total Average: \t" + str(sum(f1_macro_list)/len(pre_correction_confusion_matrix_list)) + "\n")
    file.write("Macro F1 Minimum: \t" + str(min(f1_macro_list)) + "\n")
    file.write("Macro F1 Maximum: \t" + str(max(f1_macro_list)) + "\n\n")
    
    file.write("=Micro=\n")
    for i in range(0, class_count):
        if not i:
            file.write("=none=\n")
        else:
            file.write("=" + str(config['CLASS_LIST'][i-1]) + "=\n")
            
        file.write("Micro Precision Average: \t" + str(np.sum(precision_micro_list[i, :])/len(pre_correction_confusion_matrix_list)) + "\n")
        file.write("Micro Recall Average: \t" + str(np.sum(recall_micro_list[i, :])/len(pre_correction_confusion_matrix_list)) + "\n")
        file.write("Micro F1 Average: \t" + str(np.sum(f1_micro_list[i, :])/len(pre_correction_confusion_matrix_list)) + "\n")
        file.write("\n")
    file.write("\n")
    
    file.write("=Confusion Matrix Difference=\n")
    for j in range(0, class_count):
        for k in range(0, class_count):
            file.write(str(correction_difference_confusion_matrix[j, k]) + ' ')
        file.write('\n')
    file.close()

def kfold_bucket_generator(batch_x, batch_y, seq_len, k):
    """
    Takes a batch and shuffles it, then creates k subbatches of each.

    :param batch_x: A list of values to bucket.
    :param batch_y: A list of values to bucket.
    :param seq_len: A list of sequences associated with the values.
    :param k: Number of buckets to split.
    :return: bucketed x, bucketed y, bucketed seq_len, bucket->file mapping.
    """
    indicies = sample(range(0, len(batch_x)), len(batch_x))

    nbatch_x, nbatch_y, nseq_len = [], [], []
    batch_to_file_mapping = []

    #Create K Buckets
    for i in range(0, k):
        m = int(len(indicies) / (k-i))

        x, y, z, map_ = [], [], [], []

        for n in range(0, m):
            index = indicies.pop(0)
            x.append(batch_x[index])
            y.append(batch_y[index])
            z.append(seq_len[index])
            map_.append(index)

        nbatch_x.append(x)
        nbatch_y.append(y)
        nseq_len.append(z)
        batch_to_file_mapping.append(map_)

    return nbatch_x, nbatch_y, nseq_len, batch_to_file_mapping

def generate_embeddings(file_sentence_dict, config):
    """
    Generates embeddings vectors for all included sentences.

    :param file_sentence_dict: A map containing SentenceStructures to generate embeddings for.
    :param config: A configuration file from configparser.
    :return: A list of embeddings representing X, list of classes Y, list of sequences, vector->file mapping
    """
    if not os.path.isdir('./_arff'):
        os.mkdir('_arff')

    #Launch perl pipe
    args = ['perl', './w2v.pl', config['CONFIGURATION']['EMBEDDING_FILE']]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    outs, errs = [], []

    #Wait until perl is done loading file.
    loaded = False
    while not p.poll():
        t = p.stdout.readline()
        if "READY" in t:
            loaded = True
            break
        elif "FAILED" in t:
            break
        elif "EXIT" in t:
            break

    if not loaded:
        print("Perl module did not load correctly. Dying.")
        sys.exit(-1)

    print("Perl loaded correctly.")

    #Generate embedding file for each thingy.
    embedding_list = []
    class_list = []
    seq_list = []
    mapping = [] #A map to tie things back together.

    undefined = []

    try:
        k = file_sentence_dict.keys()
        for k_ in k:
            #Debug
            if "DEBUG" in config['CONFIGURATION']:
                print(k_)
            embedding_list_file = []
            #f = open('./_arff/' + k_, 'w+')
            sentence_counter = 0

            #Number of features
            #f.write(str(config['NUM_FEATURES']) + '\n')

            #x: list of sentences
            for x in file_sentence_dict[k_]:
                #f.write("START\n")
                t_array = np.zeros((int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']), config['NUM_FEATURES']), dtype=np.float32)
                c_array = np.zeros((int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH'])), dtype=np.float32)

                for z in range(0, len(x.modified_sentence_array)):
                    p.stdin.write(x.modified_sentence_array[z][0] + "\n")
                    p.stdin.flush()

                    class_ = 0
                    if x.original_sentence_array[x.modified_sentence_array[z][2]][1] in config['CLASS_MAP']:
                        class_ = config['CLASS_MAP'][x.original_sentence_array[z][1]]

                    while not p.poll():
                        t = p.stdout.readline()

                        if "UNDEF" in t:
                            #f.write(("0.0 " * int(config['CONFIGURATION']['EMBEDDING_SIZE'])) + str(class_) + "\n")
                            undefined.append(x.modified_sentence_array[z][0])
                            break
                        elif len(t) > 2:
                            #Temp Generate Embeddings
                            t_split = t.split()
                            t_array[z][0:int(config['CONFIGURATION']['EMBEDDING_SIZE'])] = t_split[1:int(config['CONFIGURATION']['EMBEDDING_SIZE'])+1]
                            c_array[z] = class_

                            #f.write(t + " " + str(class_) + "\n")
                            break
                        else:
                            print(t)

                    #Generate Extra Features
                    if x.modified_sentence_array[z][0] == "__num__":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["IS_NUM"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "__date__":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["IS_DATE"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "__time__":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["IS_TIME"]] = 1.0

                #Add embeddings to our arrays.
                embedding_list_file.append(t_array)
                class_list.append(c_array)
                seq_list.append(len(x.modified_sentence_array))

                #Add this index back to the mapping.
                mapping.append([k_, sentence_counter])
                sentence_counter += 1

            #f.close()
            
            #Add Semantic Embeddings
            if config['CONFIGURATION']['USE_SEMANTIC_TYPES'] == '1':
                sem_loc = os.path.join(config['CONFIGURATION']['SEMANTIC_ANNOTATION_FILE_PATH'], k_ + '.st')
                if os.path.isfile(sem_loc):
                    add_semantic_features(config, sem_loc, embedding_list_file)

            #Add Document Embeddings to List
            embedding_list.extend(embedding_list_file)
            
    except Exception as e:
        print("Failed to properly generate word embeddings. Dying.")
        print(repr(e))
        p.terminate()
        sys.exit(-1)

    finally:
        p.stdin.write("EXIT\n")
        p.stdin.flush()

    p.terminate()

    #Debug
    #Write words to file that were undefined in embedding list.
    if "DEBUG" in config['CONFIGURATION']:
        xF = open('undef.txt', 'a')
        for x in undefined:
            xF.write(x)
            xF.write("\n")
        xF.close()

    return embedding_list, class_list, seq_list, mapping

def add_modified_sentence_array(file_sentence_dict):
    """
    Takes a dictionary of SentenceStructures and generates preprocessed arrays for them.

    :param file_sentence_dict:  A map containing SentenceStructures to generate modified sentences for.
    :return: Nothing.
    """
    #Get each list of SentenceStructures from map.
    v = file_sentence_dict.values()

    for x in v:
        for y in x:
            y.generate_modified_sentence_array()
            
def add_semantic_features(config, semantic_annotation_file_path, feature_vector):
    #Open File
    smf = open(semantic_annotation_file_path, 'r')
    smf_line = smf.readline()
    
    #Parse Lines
    while smf_line:
        smf_line_split = smf_line.split(',')
        smf_line_split = [int(i) for i in smf_line_split]
        smf_sentence = smf_line_split[0]-1
        smf_word = smf_line_split[1]
        
        if len(smf_line_split) == 5:
            smf_line_split = [int(i) for i in smf_line_split]
            smf_index = config['FEATURE_MAP']['PROBLEM_ST']
            feature_vector[smf_sentence][smf_word][smf_index:smf_index+3] = smf_line_split[2:]
        else:
            print("Invalid line found in semantic annotation file. Continuing.")
        smf_line = smf.readline()

def create_sentence_structures(raw_file_path):
    """
    Iterates through all documents in the directory specified in the params and creates a SentenceStructure object for each sentence.

    :param raw_file_path: Path to directory where raw documents are located
    :return: Dictionary of lists of SentenceStructure objects keyed on document name stripped of extension
    """
    #Create a dictionary of documents
    doc_dictionary = {}
    max_sentence_length = 0

    # cd into test file directory
    cwd = os.getcwd()
    os.chdir(raw_file_path)

    #Iterate over documents in the raw_file_path directory
    for document in os.listdir():

        #Instantiate a list to hold a SentenceStructure for each sentence(line) in the document
        doc_sentence_structure_list = []

        #Open the document
        doc = open(document, "r")

        doc_text = doc.read()
        doc_text_processed = preprocess(doc_text)
        doc_text_processed_split = doc_text_processed.splitlines()

        doc.close()

        doc = open(document, "r")
        try:
            #Iterate over sentences in the document
            counter = 0
            for sentence in doc.readlines():
                #Create a SentenceStructure obj
                ss = SentenceStructure(sentence)
                lower_sentence = sentence.lower()
                ss.modified_sentence = lower_sentence
                #TODO(Jeff) Readd Preprocessed text.
                #ss.modified_sentence = doc_text_processed_split[counter]
                
                if len(ss.original_sentence_array) > max_sentence_length:
                    max_sentence_length = len(ss.original_sentence_array)

                #Add SentenceStructure obj to the list
                doc_sentence_structure_list.append(ss)

                counter += 1
        except:
            print("ERR. " + str(document))
            sys.exit(0)

        assert(len(doc_sentence_structure_list) == len(doc_text_processed_split)), "Assertion Failed, array lengths don't match. " + str(len(doc_sentence_structure_list)) + " " + str(len(doc_text_processed_split))

        #Strip the extension from the file to get the document name
        doc_name = os.path.splitext(document)[0]

        #Add the SentenceStructureList to the dictionary
        doc_dictionary[doc_name] = doc_sentence_structure_list

        #Close the document
        doc.close()

    #Return to original path
    os.chdir(cwd)

    #Return the dictionary
    return doc_dictionary, max_sentence_length

def create_annotated_sentence_structures(ann_file_path, raw_file_path):
    """
    Create SentenceStructures from raw documents and annotate them

    :param ann_file_path: Path to directory where annotation documents are located
    :param raw_file_path: Path to directory where raw documents are located
    :return: Dictionary of lists of annotated SentenceStructure objects keyed on document name stripped of extension
    """
    #create annotation dictionary
    ann_dict = create_annotation_dictionary(ann_file_path)

    #create sentence structure dictionary
    ss_dict, max_sentence_length = create_sentence_structures(raw_file_path)

    #Iterate over documents
    for key, value in ss_dict.items():
        #TODO(Jeff) Ask Evan about this unused variable.
        doc_annotations = ann_dict[key]
        doc_sentence_structures = ss_dict[key]

        #Annotate each sentence
        for index, ss in enumerate(doc_sentence_structures):
            #Annotations only for this sentence
            annotations = [ann for ann in ann_dict[key] if ann.line == index + 1]

            #Updated SentenceStructure
            ss = annotate_sentence_structure(ss, annotations)

    #Return the updated ss_dict
    return ss_dict, max_sentence_length

def annotate_sentence_structure(ss, annotations):
    """
    Annotates SentenceStructure object

    :param ss: SentenceStructure object
    :param annotions: list of annotations for the sentence
    :return: Annotated SentenceStructure object
    """
    #Iterate over distinct annotations for a sentence
    for m in annotations:
        for j in range(m.start_word, m.end_word + 1):
            ss.original_sentence_array[j][1] = m.label

    return ss

def create_annotation_dictionary(annotation_file_path):
    """
    Iterates through all annotation documents in the directory specified and creates a dictionary keyed on file name (without extension) with a list Annotation objects as the value

    :param annotation_file_path: Path to directory where annotation documents are located
    :return: Dictionary of lists of Annotation objects keyed on document name stripped of extension
    """
    #Create a dictionary of documents
    doc_dictionary = {}

    # cd into annotation file directory
    cwd = os.getcwd()
    os.chdir(annotation_file_path)

    #Iterate over documents in the annotation_file_path directory
    for document in os.listdir():

        #Instantiate a list to hold Annotations for each document
        annotation_list = []

        #Open the document
        doc = open(document, "r")

        #Iterate over lines in the document
        for line in doc.readlines():

            #Create an Annotation obj
            an = Annotation(line)

            #Add Annotation obj to the list
            annotation_list.append(an)

        #Strip the extension from the file to get the document name
        doc_name = os.path.splitext(document)[0]

        #Add the annotation_list to the dictionary
        doc_dictionary[doc_name] = annotation_list

        #Close the document
        doc.close()

    #Return to the original directory
    os.chdir(cwd)

    #Return the dictionary
    return doc_dictionary

def create_supplemental_sentence_structures(supp_file_path):
    """
    Create SentenceStructures from supplemental documents

    :param supp_file_path: Path to directory where supplemental documents are located
    :return: Dictionary of lists of SentenceStructure objects keyed on document name stripped of extension
    """
    #Create a dictionary of documents
    doc_dictionary = {}

    # cd into test file directory
    cwd = os.getcwd()
    os.chdir(supp_file_path)

    #Iterate over documents in the supp_file_path directory
    for document in os.listdir():

        #Instantiate a list to hold a SentenceStructure for each sentence(line) in the document
        doc_sentence_structure_list = []

        #Open the document
        doc = open(document, "r")

        doc_text = doc.read()
        doc_text_processed = preprocess(doc_text)
        doc_text_processed_split = doc_text_processed.splitlines()

        doc.close()

        doc = open(document, "r")

        #Strip the extension from the file to get the document name
        doc_name = os.path.splitext(document)[0]

        #Iterate over sentences in the document
        counter = 0
        for sentence in doc.readlines():
            #Create a SentenceStructure obj
            ss = SentenceStructure(sentence, doc_name)
            ss.modified_sentence = doc_text_processed_split[counter]

            #Add SentenceStructure obj to the list
            doc_sentence_structure_list.append(ss)
            counter += 1

        #Add the SentenceStructureList to the dictionary
        doc_dictionary[doc_name] = doc_sentence_structure_list

        #Close the document
        doc.close()

    #Return to original path
    os.chdir(cwd)

    #Return the dictionary
    return doc_dictionary

def write_annotations(sentence_dict, output_location):
    # cd into test file directory
    cwd = os.getcwd()
    
    if not os.path.isdir(output_location):
        os.mkdir(output_location)
    os.chdir(output_location)    
    
    for k in sentence_dict.keys():
        sentence_counter = 1
        k_file = open(k + '.con', 'w')
        
        for v in sentence_dict[k]:
            #Get the next annotation
            start, end, tag = agent.get_annotation(v.modified_sentence_array, 0)
            while not start == None:
                #Build output string.
                out_words = []
                for i in range(start, end+1):
                    out_words.append(v.original_sentence_array[i][0])
                    
                out_string = 'c="' + ' '.join(out_words) + '" ' + str(sentence_counter) + ':' + str(start) + ' ' + str(sentence_counter) + ':' + str(end) + '||t="' + tag + '"\n'
                k_file.write(out_string)
                
                start, end, tag = agent.get_annotation(v.modified_sentence_array, end+1)
            
            sentence_counter += 1
        
    os.chdir(cwd)

if __name__ == "__main__":
    main()
