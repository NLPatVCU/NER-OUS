"""
classes.py
Scope: Defines the major classes used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import re
from copy import copy
import spacy

strip_map = set([':', ';', ',', '.', '[', '(', ']', ')', '-', '?', '&quot;', '&apos;', '&apos;s', '/', '#', '=', '+', '*', '%'])
nlp = spacy.load('en_core_web_sm')

#TODO(Jeff) Replace with preprocessing later.
def process_token(token):
    token = re.sub(r'[\.-]', '', token)
    token = re.sub(r'^-?[\d]+[%\+]?$', '__num__', token)
    token = re.sub(r'^[0-1]\d?/\d?\d(/\d\d)?(\d\d)?$', '__date__', token)
    token = re.sub(r'^\d?\d:\d\d(:\d\d)?$', '__time__', token)
    return token

#Author: Jeffrey Smith
class SentenceStructure:
    """
    SentenceStructure represents a sentence taken from an input file. It splits the string based on whitespace and adds an END tag.
    """

    def __init__(self, in_string, label=None):
        """
        Constructor for SentenceStructure.

        :param in_string: The string that this object will represent.
        :param label: A label that will be automatically applied to all words in the sentence. Defaults to None.
        :return: Nothing.
        :var original_sentence: Copy of the original string.
        :var original_sentence_array: An array of [string,string] tuples. The first string is a token, and the second is a holder for tags.
        """
        self.original_sentence = in_string
        self.original_sentence_array = []
        self.modified_sentence = None
        self.modified_sentence_array = None

        #Split the string by whitespace and add it to the array.
        for x in in_string.split():
            if not label:
                token = [x, ""]
            else:
                token = [x, label]
            self.original_sentence_array.append(token)

    def generate_modified_sentence_array(self, allow_stripping=False):
        """
        modified_sentence_array creator for SentenceStructure.

        :return: Nothing.
        :var modified_sentence_array: An array of [string,string,int] tuples. The first string is a token, and the second is a holder for tags. The int represents the position in the original string.
        """
        self.modified_sentence_array = []

        #Split the string by whitespace and add it to the array.
        counter = 0

        for x in self.modified_sentence.split():
            token = [x, '', counter]
            counter += 1
            if not allow_stripping or not x in strip_map:
                #TODO(Jeff) Replace with preprocessing later.
                token[0] = process_token(token[0])
                self.modified_sentence_array.append(token)

    def rebuild_modified_sentence_array_tags(self):
        #Modifiy special characters
        m = 0
        dep = []
        head = []
        doc = nlp(self.original_sentence)
        for token in doc:
            dep.append(token.dep_)
            head.append(token.head.text)            
        
        while m < len(self.modified_sentence_array):
            #Check if the character in this position is a special character. If so, process
            if self.modified_sentence_array[m][0] == ',':
                if m > 0 and m < len(self.modified_sentence_array)-1 and self.modified_sentence_array[m-1][1] == self.modified_sentence_array[m+1][1]:
                    self.modified_sentence_array[m][1] = self.modified_sentence_array[m-1][1]
            elif self.modified_sentence_array[m][0] == '/':
                if m > 0 and m < len(self.modified_sentence_array)-1 and self.modified_sentence_array[m-1][1] == self.modified_sentence_array[m+1][1]:
                    self.modified_sentence_array[m][1] = self.modified_sentence_array[m-1][1]                    
            elif self.modified_sentence_array[m][0] == '[' or self.modified_sentence_array[m][0] == '(':
                if m < len(self.modified_sentence_array)-1 and not self.modified_sentence_array[m+1][1] == '':
                    self.modified_sentence_array[m][1] = self.modified_sentence_array[m+1][1]                      
            elif self.modified_sentence_array[m][0] == ')' or self.modified_sentence_array[m][0] == ')' or self.modified_sentence_array[m] == '&apos;s':
                if m > 0 and not self.modified_sentence_array[m-1][1] == '':
                    self.modified_sentence_array[m][1] = self.modified_sentence_array[m-1][1]    
            elif self.modified_sentence_array[m][0] == '&quot;' and not self.modified_sentence_array[m][1]:
                quot_loc = -1
                for p in range(m+1, len(self.modified_sentence_array)):
                    if self.modified_sentence_array[p][0] == '&quot;':
                        quot_loc = p
                        break
                if quot_loc > -1:
                    self.modified_sentence_array[m][1] = self.modified_sentence_array[m+1][1]
                    self.modified_sentence_array[quot_loc][1] = self.modified_sentence_array[m+1][1]
                    
            #elif self.modified_sentence_array[m][0] == 'a' or self.modified_sentence_array[m][0] == 'an' or self.modified_sentence_array[m][0] == 'his' or self.modified_sentence_array[m][0] == 'her' or self.modified_sentence_array[m][0] == 'the' or self.modified_sentence_array[m][0] == 'this':
                #if m+1 < len(self.modified_sentence_array):
                    #self.modified_sentence_array[m][1] = self.modified_sentence_array[m+1][1]
                    
            #elif dep[m] == 'cc' or dep[m] == 'det' or dep[m] == 'nummod' or dep[m] == 'poss' or dep[m] == 'prep':
             #   for x in range(0, len(self.original_sentence_array)):
              #      if self.original_sentence_array[x][0] == head[m]:
               #         self.modified_sentence_array[m][1] = self.modified_sentence_array[x][1]
                #        break
                    
            m += 1

    def rebuild_modified_sentence_array(self):
        for x in range(0, len(self.original_sentence_array)):
            if x >= len(self.modified_sentence_array) or self.modified_sentence_array[x][2] > x:
                #Missing Value in array. Add it back in.
                val = [self.original_sentence_array[x][0], '', x]
                self.modified_sentence_array.insert(x, copy(val))
        self.rebuild_modified_sentence_array_tags()
                
                

#Author: Jeffrey Smith
class BatchContainer:
    """
    BatchContainer represents a container for running network batches through Tensorflow
    """
    def __init__(self, bx, by, bs, mapping=None):
        """
        Constructor for BatchContainer.

        :param bx: List of x values to batch.
        :param by: List of y values to batch.
        :param bs: List of sentence lengths to batch.
        :param mapping: A map that connects indices of the batches to the original files and strings. Defaults to None if not needed.
        :return: Nothing.
        :var bx: List of x values to batch.
        :var by: List of y values to batch.
        :var bs: List of sentence lengths to batch.
        :var mapping: A map that connects indices of the batches to the original files and strings.
        """
        self.bx = bx
        self.by = by
        self.bs = bs
        self.mapping = mapping

#Author: Evan French
class Annotation:
    """
    Annotation represents a line from the annotation file.
    """
    def __init__(self, in_string):
        """
        Constructor for Annotation.

        :param in_string: The string that this object will represent.
        :return: Nothing.
        :var concept: String representing concept (i.e. "the sickness").
        :var label: Classification label (i.e. "problem").
        :var line: Line number on which the concept appears.
        :var start_word: Index of first word in the concept.
        :var end_word: Index of the word after the concept ends.
        """

        #Clean up in_string into segments we can use
        parse = re.sub(r'c="', '', in_string)
        concept = re.sub(r'" \d+:\d+.*$', '', parse)
        after_concept = re.sub(r'c=".*" ', '', in_string)
        segments = after_concept.replace(':', ' ').replace('||t=', ' ').replace('"', '').split()

        #Define Annotation properties
        self.concept = concept.strip()
        self.line = int(segments[0])
        self.start_word = int(segments[1])
        self.end_word = int(segments[3])
        self.label = segments[4]
