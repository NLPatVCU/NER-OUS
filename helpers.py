import os, re
from copy import copy

from medacy.pipeline_components.metamap.metamap import MetaMap

#Constant Lists
#MetaMap semantic types corresponding to medical problems
problem_list = [
'amph', #Amphibian
'famg', #Family Group
'ffas', #Fully Formed Anatomical Structure
'orgm', #Organism
'humn', #Human
'rnlw', #Regulation or Law
'nusq', #Nucleotide Sequence
'eehu', #Environmental Effect of Humans
'sosy', #Sign or Symptom
'patf', #Pathologic Function
'dsyn', #Disease or Syndrome
'inpo', #Injury or Poisoning
'bact', #Bacterium
'gora', #Governmental or Regulatory Activity
'grpa', #Group Attribute
'anab', #Anatomical Abnormality
'neop', #Neoplastic Process
'cgab', #Congenital Abnormality
]

#MetaMap semantic types corresponding to medical tests
test_list = [
'mbrt', #Molecular Biology Research Technique
'lbpr', #Laboratory Procedure
'diap', #Diagnostic Procedure
]

#MetaMap semantic types corresponding to medical treatments
treatment_list = [
'clnd', #Clinical Drug
'drdd', #Drug Delivery Device
'edac', #Educational Activity
'shro', #Self-help or Relief Organization
'amas', #Amino Acid Sequence
'antb', #Antibiotic
'mcha', #Machine Activity
'lang', #Language
'horm', #Hormone
]

def stripped_filename(filename): 
    return os.path.splitext(filename)[0]
    
def build_metamap_semantic_dictionary(medacy_instance, in_file):
    metamap_dict = medacy_instance.map_file(in_file)
    metamap_terms = medacy_instance.extract_mapped_terms(metamap_dict)
    metamap_annotations = medacy_instance.mapped_terms_to_spacy_ann(metamap_terms)
    
    return metamap_annotations

def build_word_dictionary(in_file):
    index_dict = {}
    line_index_counter = 0
    sentence_counter = 1
    word_counter = 0

    #For each line, extract the words and their start locations.
    line = in_file.readline().rstrip('\r\n')

    while line:
        #Find all locations of whitespace.
        spaces = [m.start() for m in re.finditer(' ', line)]
        #If we have whitespace, process the words.
        if len(spaces):
            word_start = -1
            if not spaces[0] == 0:
                word_start = 0
            for i in range(0, len(spaces)):
                if not word_start == -1:
                    #[start_index, text, sentence #, word #, problem st, test st, treatment st]
                    word_info = [word_start + line_index_counter, line[word_start:spaces[i]], sentence_counter, word_counter, 0, 0, 0]
                    index_dict[word_start + line_index_counter] = copy(word_info)
                    word_counter += 1
                    word_start = -1
                if i == (len(spaces)-1):
                    if not spaces[i] == (len(line)-1):
                        word_info = [(spaces[i]+1) + line_index_counter, line[(spaces[i]+1):], sentence_counter, word_counter, 0, 0, 0]
                        index_dict[(spaces[i]+1) + line_index_counter] = copy(word_info)
                else:
                    if not spaces[i] == (spaces[i+1] - 1):
                        word_start = spaces[i] + 1
        #No whitespace, so if there is text, just add it as a word.
        else:
            if len(line):
                word_info = [line_index_counter, line, sentence_counter, 0, 0, 0, 0]
                index_dict[line_index_counter] = copy(word_info)
                
        #Increment and loop
        line_index_counter = in_file.tell()
        sentence_counter += 1
        word_counter = 0
        line = in_file.readline().rstrip('\r\n')
        
    return index_dict


def build_semantic_type_annotations(config):
    #TODO(Jeff): Fill out function information.
    medacy_metamap_component = MetaMap(metamap_path=config['METAMAP_PATH'])
    input_directory = config['RAW_FILE_PATH']
    output_directory = config['SEMANTIC_ANNOTATION_FILE_PATH']

    # cd into test file directory
    cwd = os.getcwd()
    os.chdir(input_directory)    
    
    #Iterate over documents in the raw_file_path directory
    for document in os.listdir():
        out_file_path = os.path.join(cwd, output_directory, stripped_filename(document) + ".st")
        if not os.path.exists(out_file_path) or config['OVERRIDE_SEMANTIC_ANNOTATIONS'] == "1":
            metamap_annotations = build_metamap_semantic_dictionary(medacy_metamap_component, document)
            
            in_file = open(document, 'r')
            index_dict = build_word_dictionary(in_file)
            in_file.close()
            
            #Sort the index_dict for easy traversal.
            key_list = sorted(index_dict.keys())
            
            for v in metamap_annotations["entities"].values():
                mark_location = -1
                if v[2] in problem_list:
                    mark_location = 4
                elif v[2] in test_list:
                    mark_location = 5
                elif v[2] in treatment_list:
                    mark_location = 6

                if mark_location > -1:
                    try:
                        start_index = key_list.index(v[0])
                        while key_list[start_index] < v[1]:
                            index_dict[key_list[start_index]][mark_location] = 1
                            start_index += 1
                            if start_index >= len(key_list):
                                break
                    except ValueError:
                        print("Found a non-existant index. Continuing.")
                            
            out_file = open(out_file_path, 'w')
            for v in index_dict.values():
                if v[4] or v[5] or v[6]:
                    out_buff = [str(v[2]), str(v[3]), str(v[4]), str(v[5]), str(v[6])] 
                    out_file.write(','.join(out_buff) + '\n')
            out_file.close()

    #Return to original path
    os.chdir(cwd)