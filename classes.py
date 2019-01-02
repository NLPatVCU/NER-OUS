"""
classes.py
Scope: Defines the major classes used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import re

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

        #Add an end tag to the end of the array.
        if not label:
            self.original_sentence_array.append(["END", ""])
        else:
            self.original_sentence_array[0][1] = label + ":Start"
            self.original_sentence_array.append(["END", label + ":End"])

    def generate_modified_sentence_array(self):
        """
        modified_sentence_array creator for SentenceStructure.

        :return: Nothing.
        :var modified_sentence_array: An array of [string,string,int] tuples. The first string is a token, and the second is a holder for tags. The int represents the position in the original string.
        """
        self.modified_sentence_array = []

        #Split the string by whitespace and add it to the array.
        counter = 0

        for x in self.modified_sentence.split():
            token = [x, "", counter]
            self.modified_sentence_array.append(token)
            counter += 1
        self.modified_sentence_array.append(["END", ""])

        assert(len(self.original_sentence_array) == len(self.modified_sentence_array)), "Assertion failed, sentences don't match. Original Sentence: " + self.original_sentence +" Modified Sentence: " + self.modified_sentence

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
