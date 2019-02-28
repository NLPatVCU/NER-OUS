import os
import re
from copy import copy

from medacy.pipeline_components.metamap.metamap import MetaMap

#Constant Lists
#MetaMap semantic types corresponding to medical problems
problem_list = [
'grpa', #Group Attribute
'amph', #Amphibian
'mobd', #Mental or Behavioral Dysfunction
'inpo', #Injury or Poisoning
'lang', #Language
'dsyn', #Disease or Syndrome
'sosy', #Sign or Symptom
'aggp', #Age Group
'evnt', #Event
'bhvr', #Behavior
'cgab', #Congenital Abnormality
'rept', #Reptile
'patf', #Pathologic Function
'chem', #Chemical
'neop', #Neoplastic Process
'acab' #Acquired Abnormality
]

#MetaMap semantic types corresponding to medical tests
test_list = [
'edac', #Educational Activity
'amas', #Amino Acid Sequence
'mbrt', #Molecular Biology Research Technique
'irda', #Indicator, Reagent, or Diagnostic Aid
'ffas', #Fully Formed Anatomical Structure
'enty', #Entity
'elii', #Element, Ion, or Isotope
'ocdi', #Occupation or Discipline
'lbpr', #Laboratory Procedure
'nnon', #Nucleic Acid, Nucleoside, or Nucleotide
'comd', #Cell or Molecular Dysfunction
'resa', #Research Activity
'bacs', #Biologically Active Substance
'lbtr', #Laboratory or Test Result
'vita', #Vitamin
'diap' #Diagnostic Procedure
]

#MetaMap semantic types corresponding to medical treatments
treatment_list = [
'drdd', #Drug Delivery Device
'orgt', #Organization
'bodm', #Biomedical or Dental Material
'mcha', #Machine Activity
'food', #Food
'tisu', #Tissue
'hcpp', #Human-caused Phenomenon or Process
'topp', #Therapeutic or Preventive Procedure
'antb', #Antibiotic
'genf', #Genetic Function
'medd', #Medical Device
'bdsu' #Body Substance
]

def stripped_filename(filename): 
    """
    Quickly strip extension from a filename.
    
    :param filename: Filename to remove extension from.
    :return: Stripped filename.
    """
    return os.path.splitext(filename)[0]
    
def build_metamap_semantic_dictionary(medacy_metamap_component, in_file_path):
    """
    Uses an instance of Medacy MetaMap to build a dictionary of semantic objects and map them in SpaCy ANN format.
    
    :param medacy_metamap_component: Initialized Medacy MetaMap component to use.
    :param in_file_path: Path of the file to build the semantic dictionary for.
    :return: Metamap annotation dictionary in SpaCy ANN format.
    """
    metamap_dict = medacy_metamap_component.map_file(in_file_path)
    metamap_terms = medacy_metamap_component.extract_mapped_terms(metamap_dict)
    if metamap_terms:
        metamap_annotations = medacy_metamap_component.mapped_terms_to_spacy_ann(metamap_terms)
        return metamap_annotations
    else:
        return None
    
    

def build_word_dictionary(in_file):
    """
    Builds a dictionary of words indexed by starting position in a document. For mapping ANN annotations to CON format.
    [start_index, text, sentence #, word #, problem st, test st, treatment st]
    
    :param in_file: Open file to be read and mapped.
    :return: Dictionary of words indexed by starting position. 
    """
    index_dict = {}
    line_index_counter = 0
    sentence_counter = 1
    word_counter = 0

    #For each line, extract the words and their start locations.
    line = in_file.readline()

    while line:
        line = line.rstrip('\r\n')
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

def write_semantic_annotations_to_file(index_dict, out_file_path):
    """
    Writes semantic annotations to file for easy retrieval. CSV format. Indicies below.
    sentence #, word #, problem st, test st, treatment st
    
    :param index_dict: Processed dictionary of words and annotations to write to file.
    :param out_file_path: Path to write to.
    :return: None
    """
    out_file = open(out_file_path, 'w')
    for v in index_dict.values():
        if v[4] or v[5] or v[6]:
            out_buff = [str(v[2]), str(v[3]), str(v[4]), str(v[5]), str(v[6])] 
            out_file.write(','.join(out_buff) + '\n')
    out_file.close()

def build_single_semantic_type_annotations(config, in_file_path, medacy_metamap_component=None):
    """
    Builds a dictionary of words indexed by starting position in a document and adds metamap annotations. 
    This function does not write to file.
    [start_index, text, sentence #, word #, problem st, test st, treatment st]
    
    :param config: Configuration file to utilize. 
    :param in_file_path: Path to file to be read and mapped.
    :param medacy_metamap_component: Optinal open instance of a Medacy MetaMap component. If not provided, will open one.
    :return: Dictionary of words indexed by starting position in a document and metamap annotations. 
    """
    if not medacy_metamap_component:
        medacy_metamap_component = MetaMap(metamap_path=config['CONFIGURATION']['METAMAP_PATH'])
    metamap_annotations = build_metamap_semantic_dictionary(medacy_metamap_component, in_file_path)
    
    if not metamap_annotations:
        return None

    in_file = open(in_file_path, 'r')
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
    return index_dict
    
    
def build_semantic_type_annotations(config):
    """
    For a directory, builds a dictionary of words indexed by starting position in a document and adds metamap annotations then converts and writes to file. 
    CSV format. Indicies below.
    sentence #, word #, problem st, test st, treatment st
    
    :param config: Configuration file to utilize. 
    :return: None
    """
    medacy_metamap_component = MetaMap(metamap_path=config['CONFIGURATION']['METAMAP_PATH'])
    input_directory = config['CONFIGURATION']['RAW_FILE_PATH']
    output_directory = config['CONFIGURATION']['SEMANTIC_ANNOTATION_FILE_PATH']

    # cd into test file directory
    cwd = os.getcwd()
    os.chdir(input_directory)    
    
    #Iterate over documents in the raw_file_path directory
    for document in os.listdir():
        out_file_path = os.path.join(cwd, output_directory, stripped_filename(document) + ".st")
        if not os.path.exists(out_file_path) or config['CONFIGURATION']['OVERRIDE_SEMANTIC_ANNOTATIONS'] == "1":
            index_dict = build_single_semantic_type_annotations(config, document, medacy_metamap_component)
            if index_dict:
                write_semantic_annotations_to_file(index_dict, out_file_path)

    #Return to original path
    os.chdir(cwd)
