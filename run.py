#!/usr/bin/python3

import sys
import os
import subprocess
import configparser
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

        
def main():
    """
    Main function of the application. Call -h or --help for command line inputs.
    """
    mode, outputDirectory, modelFile = None, None, None
    """
    #Process command line entries.
    opts, args = getopt.getopt(sys.argv[1:], 'm:i:o:d:a:h',["mode=","output=","model=","help"])
    for opt, arg, in opts:
        if opt in ("-m","--mode"):
            mode = arg
        elif opt in ("-o","--output"):
            outputDirectory = arg
        elif opt in ("-d","--model"):
            modelFile = arg
        elif opt in ("-h","--help"):
            printHelp()
            return
        
    #Verify if needed command line entries are present.
    if mode == None:
        print("You must specify a mode to use with -m or --mode. Options are train, eval, and annotate.")
        print("train creates a model file, eval evaluates annotated text using a model, and annotate creates an annotation file using a model.")
        return
        
    elif mode == "eval" and modelFile == None:
        print("You must specify a model to use for evaluation using -d or --model.")
        
    if outputDirectory == None:
        print("You must specify a directory for output files with -o or --output.")
        return
        """
    #Parse config file and set up configuration classes.
    config_file = configparser.ConfigParser()
    config_file.read_file(open('config.ini'))
    config_dict = config_file['Main']

    check_config_file(config_dict)
    
    config = {'CONFIGURATION': config_dict}
 
    feature_map = {"PUNC_OTHER" : 0,
                   "PUNC_COMMA" : 1,
                   "PUNC_PERIOD" : 2,
                   "IS_NUM" : 3,
                   "IS_DATE" : 4}
                                   
    config['FEATURE_MAP'] = feature_map
    config['CLASS_LIST'] = config['CONFIGURATION']['CLASSES'].split(',')
    config['NUM_FEATURES'] = int(config['CONFIGURATION']['EMBEDDING_SIZE']) + len(feature_map)

    #Iterate files and generate feature vectors.
    file_sentence_dict = create_annotated_sentence_structures(config['CONFIGURATION']['ANNOTATION_FILE_PATH'], config['CONFIGURATION']['RAW_FILE_PATH'])
    add_modified_sentence_array(file_sentence_dict)
    helpers.build_semantic_type_annotations(config)
    tx, ty, ts, tm = generate_embeddings(file_sentence_dict, config)
    train_batch_container = BatchContainer(tx, ty, ts, tm)

    #Train the network.
    train_network(train_batch_container, file_sentence_dict, config)

   
def printHelp():
    """
    Prints out the command line help information.
    """ 
    print("Options:")
    print("-m/--mode [train,eval,annotate] : Specify the mode of the system.")
    print("-o/--output DIR : Specify the output directory to write to.")
    print("-d/--model FILE : Specify a model to use when running in eval mode.")
    
    return

def train_network(train_batch_container, file_sentence_dict, config, supplemental_batch=None):
    """
    Trains a neural network model. If one is not given, creates one.

    :param train_batch_container: A BatchContainer object containing the data to be trained.
    :param file_sentence_dict: Map containing SentenceStructures of all files in memory. Used for generating analysis.
    :param config: A configuration instance from configparser.
    :param supplemental_batch: A BatchContainer object containing optional data to be transfer learned. Defaults to None.
    :return: Nothing.
    """
    buckets = int(config['CONFIGURATION']['BUCKETS'])
    epochs = int(config['CONFIGURATION']['EPOCHS'])

    #Setup Buckets for 10 fold cross validation
    batch_x, batch_y, seq_len, batch_to_file_map = kfold_bucket_generator(train_batch_container.bx, train_batch_container.by, train_batch_container.bs, buckets)

    #TODO(Jeff) Clean up supplemental_batch information.
    if supplemental_batch:
        sup_batch_x, sup_batch_y, sup_seq_len, _ = kfold_bucket_generator(supplemental_batch.bx, supplemental_batch.by, supplemental_batch.bs, 10)

    #Create and train the model for kFoldCrossValidation
    confusion_matrix_list = []
    sentence_lenience_list = []

    for k in range(0, buckets):
        trainer = agent.Agent(config['NUM_FEATURES'], 4, int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']))

        #Train supplemental for j epochs.
        if supplemental_batch:
            for j in range(0, epochs):
                for l in range(0, 10):
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
        cf = trainer.eval(batch_x[k], batch_y[k], seq_len[k])
        confusion_matrix_list.append(cf)

        print(cf)

        file = open("./outCF", 'a')
        outstr = np.array2string(cf)
        file.write(outstr)
        file.write("\n")
        file.close()

        cf_ = trainer.eval_with_structure(batch_x[k], batch_y[k], seq_len[k], k, train_batch_container.mapping, batch_to_file_map, file_sentence_dict)
        sentence_lenience_list.append(cf_)
        file = open("./outCFS", 'a')
        outstr = np.array2string(cf_)
        file.write(outstr)
        file.write("\n")
        file.close()

        trainer.clean_up()

    #Run analysis generation.
    #TODO(Jeff) Create separate function for analysis generation.

    #Start with Majority Sense Baseline
    class_count = len(confusion_matrix_list[0])
    majority_sense_data = np.zeros((1, class_count), dtype=np.int32)

    for i in confusion_matrix_list:
        for j in range(0, class_count):
            for k in range(0, class_count):
                majority_sense_data[0, k] += i[j, k]

    class_none_micro_precision = 1.0 * majority_sense_data[0, 0] / np.sum(majority_sense_data[0, :])
    class_none_micro_recall = 1.0
    class_none_micro_f1_score = 2 * (class_none_micro_precision/(class_none_micro_precision+1.0))

    class_none_macro_precision = class_none_micro_precision/class_count
    class_none_macro_recall = 1.0/class_count
    class_none_macro_f1_score = class_none_micro_f1_score/class_count

    #Now for all the individual buckets.
    precision_micro_list = np.zeros((class_count, len(confusion_matrix_list)), dtype=np.float32)
    recall_micro_list = np.zeros((class_count, len(confusion_matrix_list)), dtype=np.float32)
    f1_micro_list = np.zeros((class_count, len(confusion_matrix_list)), dtype=np.float32)
    precision_macro_list = []
    recall_macro_list = []
    f1_macro_list = []

    #TODO(Jeff) Convert to enumerate.
    for i in range(0, len(confusion_matrix_list)):
        for j in range(0, class_count):
            precision_micro_list[j, i] = 1.0 * confusion_matrix_list[i][j, j] / np.sum(confusion_matrix_list[i][j, :])
            recall_micro_list[j, i] = 1.0 * confusion_matrix_list[i][j, j] / np.sum(confusion_matrix_list[i][:, j])
            f1_micro_list[j, i] = 2.0 * ((precision_micro_list[j, i] * recall_micro_list[j, i]) / (precision_micro_list[j, i] + recall_micro_list[j, i]))

        precision_macro_list.append((np.sum(precision_micro_list[:, i])/class_count))
        recall_macro_list.append((np.sum(recall_micro_list[:, i])/class_count))
        f1_macro_list.append((np.sum(f1_micro_list[:, i])/class_count))

    #Process Sentence Lenience Lists
    total_sentence_lenience = np.zeros((class_count, 3), dtype=np.int32)

    for i in sentence_lenience_list:
        total_sentence_lenience[:, :] += i[:, :]

    #Write Information to file
    file = open("./analysis.txt", 'a')

    file.write("===Majority Sense Baseline===\n")
    file.write("Micro Precision: \t" + str(class_none_micro_precision) + "\n")
    file.write("Micro Recall: \t" + str(class_none_micro_recall) + "\n")
    file.write("Micro F1: \t" + str(class_none_micro_f1_score) + "\n")
    file.write("Macro Precision: \t" + str(class_none_macro_precision) + "\n")
    file.write("Macro Recall: \t" + str(class_none_macro_recall) + "\n")
    file.write("Macro F1: \t" + str(class_none_macro_f1_score) + "\n\n")

    file.write("===Summary===\n\n")

    file.write("=Macro=\n")
    file.write("Macro F1 Total Average: \t" + str(sum(f1_macro_list)/buckets) + "\n")
    file.write("Macro F1 Minimum: \t" + str(min(f1_macro_list)) + "\n")
    file.write("Macro F1 Maximum: \t" + str(max(f1_macro_list)) + "\n\n")

    file.write("=Sentence Level=\n")
    file.write("CLASS \tSTRICT \tLENIENT \tMISS \tS% \tL%\n")
    for i in range(0, class_count):
        file.write(str(config['CLASS_LIST']) +
                   " \t" + str(total_sentence_lenience[i, 0]) + " \t" + str(total_sentence_lenience[i, 1]) + " \t" + str(total_sentence_lenience[i, 2]) +
                   str(total_sentence_lenience[i, 0]/np.sum(total_sentence_lenience[i, :])) + "\t" + str(np.sum(total_sentence_lenience[i, 0:2])/np.sum(total_sentence_lenience[i, :])) + "\n")
    file.write("\n")

    for i in range(0, class_count):
        file.write("=" + str(config['CLASS_LIST']) + "=\n")
        file.write("Micro Precision Average: \t" + str(np.sum(precision_micro_list[i, :])/buckets) + "\n")
        file.write("Micro Recall Average: \t" + str(np.sum(recall_micro_list[i, :])/buckets) + "\n")
        file.write("Micro F1 Average: \t" + str(np.sum(f1_micro_list[i, :])/buckets) + "\n")
        file.write("\n")

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
            #TODO(Jeff) Add a debug flag for verbose outputs like this.
            print(k_)
            f = open('./_arff/' + k_, 'w+')
            sentence_counter = 0

            #TODO(Jeff) Change this later, only static for the interm. Should match number of features.
            f.write("201\n")

            #x: list of sentences
            for x in file_sentence_dict[k_]:
                f.write("START\n")
                t_array = np.zeros((int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH']), config['NUM_FEATURES']), dtype=np.float32)
                c_array = np.zeros((int(config['CONFIGURATION']['MAX_SENTENCE_LENGTH'])), dtype=np.float32)

                for z in range(0, len(x.modified_sentence_array)):
                    p.stdin.write(x.modified_sentence_array[z][0] + "\n")
                    p.stdin.flush()

                    class_ = 0

                    #TODO(Jeff) This shouldn't be class specific. Make generic.
                    if not "End" in x.original_sentence_array[z][1]:
                        if "problem" in x.original_sentence_array[z][1]:
                            class_ = 1
                        elif "test" in x.original_sentence_array[z][1]:
                            class_ = 2
                        elif "treatment" in x.original_sentence_array[z][1]:
                            class_ = 3

                    while not p.poll():
                        t = p.stdout.readline()

                        if "UNDEF" in t:
                            f.write(("0.0 " * int(config['CONFIGURATION']['EMBEDDING_SIZE'])) + str(class_) + "\n")
                            undefined.append(x.modified_sentence_array[z][0])
                            break
                        elif len(t) > 2:
                            #Temp Generate Embeddings
                            t_split = t.split()
                            t_array[z][0:int(config['CONFIGURATION']['EMBEDDING_SIZE'])] = t_split[1:int(config['CONFIGURATION']['EMBEDDING_SIZE'])+1]
                            c_array[z] = class_

                            f.write(t + " " + str(class_) + "\n")
                            break
                        else:
                            print(t)

                    #Generate Extra Features
                    if x.modified_sentence_array[z][0] == ":":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_OTHER"]] = 1.0
                    elif x.modified_sentence_array[z][0] == ";":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_OTHER"]] = 1.0
                    elif x.modified_sentence_array[z][0] == ",":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_COMMA"]] = 1.0
                    elif x.modified_sentence_array[z][0] == ".":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_PERIOD"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "[" or x.modified_sentence_array[z][0] == "]" or x.modified_sentence_array[z][0] == "(" or x.modified_sentence_array[z][0] == ")":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_OTHER"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "&quot;":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_OTHER"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "'" or x.modified_sentence_array[z][0] == "'s":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["PUNC_OTHER"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "num":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["IS_NUM"]] = 1.0
                    elif x.modified_sentence_array[z][0] == "date":
                        t_array[z][int(config['CONFIGURATION']['EMBEDDING_SIZE']) + config['FEATURE_MAP']["IS_DATE"]] = 1.0

                #Add embeddings to our arrays.
                embedding_list.append(t_array)
                class_list.append(c_array)
                seq_list.append(len(x.modified_sentence_array))

                #Add this index back to the mapping.
                mapping.append([k_, sentence_counter])
                sentence_counter += 1

            f.close()
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
    #TODO(Jeff) Eventually remove debug features from parent pipeline.
    #Write words to file that were undefined in embedding list.
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

def create_sentence_structures(raw_file_path):
    """
    Iterates through all documents in the directory specified in the params and creates a SentenceStructure object for each sentence.

    :param raw_file_path: Path to directory where raw documents are located
    :return: Dictionary of lists of SentenceStructure objects keyed on document name stripped of extension
    """
    #Create a dictionary of documents
    doc_dictionary = {}

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
                ss.modified_sentence = doc_text_processed_split[counter]

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
    return doc_dictionary

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
    ss_dict = create_sentence_structures(raw_file_path)

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
    return ss_dict

def annotate_sentence_structure(ss, annotations):
    """
    Annotates SentenceStructure object

    :param ss: SentenceStructure object
    :param annotions: list of annotations for the sentence
    :return: Annotated SentenceStructure object
    """
    #Iterate over distinct annotations for a sentence
    for m in annotations:
        for j in range(m.start_word, m.end_word + 2):
            if j == m.start_word:
                ss.original_sentence_array[j][1] = m.label + ':Start'
            elif j == m.end_word + 1:
                ss.original_sentence_array[j][1] = m.label + ':End'
            else:
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

if __name__ == "__main__":
    main()
