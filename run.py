#!/usr/bin/python3
"""
run.py
Scope: The entrance point for our program.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import sys, getopt, os, subprocess
from classes import SentenceStructure, Annotation

#TODO(Jeff) Revamp this file based on run_test.py

#Author: Jeffrey Smith
def main():
    """
    Main function of the application. Call -h or --help for command line inputs.
    """
    mode, inputDirectory, annotationsDirectory, outputDirectory, modelFile = None, None, None, None, None
    
    #Process command line entries.
    opts, args = getopt.getopt(sys.argv[1:], 'm:i:o:d:a:h',["mode=","input=","output=","model=","annotations=","help"])
    for opt, arg, in opts:
        if opt in ("-m","--mode"):
            mode = arg
        elif opt in ("-i","--input"):
            inputDirectory = arg
        elif opt in ("-o","--output"):
            outputDirectory = arg
        elif opt in ("-d","--model"):
            modelFile = arg
        elif opt in ("-a","--annotations"):
            annotationsDirectory = arg
        elif opt in ("-h","--help"):
            printHelp()
            return
        
    #Verify if needed command line entries are present.
    if mode == None:
        print("You must specify a mode to use with -m or --mode. Options are train, test, and eval.")
        return
    elif mode == "eval" and modelFile == None:
        print("You must specify a model to use for evaluation using -d or --model.")
        
    if inputDirectory == None:
        print("You must specify a directory with input files with -i or --input.")
        return

    if annotationsDirectory == None:
        print("You must specify a directory with annotation files with -a or --annotations.")
        return
        
    if outputDirectory == None:
        print("You must specify a directory for output files with -o or --output.")
        return

#Author: Jeffrey Smith      
def printHelp():
    """
    Prints out the command line help information.
    """ 
    print("Options:")
    print("-m/--mode [test,train,eval] : Specify the mode of the system.")
    print("-i/--input DIR : Specify the input directory to read from.")
    print("-a/--annotations DIR : Specify the annotations directory to read from.")
    print("-o/--output DIR : Specify the output directory to write to.")
    print("-d/--model FILE : Specify a model to use when running in eval mode.")
    
    return


#Author: Evan French
"""
Iterates through all documents in the directory specified in the params and creates a SentenceStructure object for each sentence. 
Return value is a dictionary keyed on document name with lists of SentenceStructure objects as values.
"""
def CreateSentenceStructures(raw_file_path):
    """
    Create SentenceStructures from raw documents
    
    :param raw_file_path: Path to directory where raw documents are located
    :return: Dictionary of lists of SentenceStructure objects keyed on document name stripped of extension
    """

    #Create a dictionary of documents
    docDictionary = {}

    # cd into test file directory
    cwd = os.getcwd()
    os.chdir(raw_file_path)

    #Iterate over documents in the raw_file_path directory
    for document in os.listdir():

        #Instantiate a list to hold a SentenceStructure for each sentence(line) in the document
        docSentenceStructureList = []

        #Open the document
        doc = open(document, "r")

        #Iterate over sentences in the document
        for sentence in doc.readlines():

            #Create a SentenceStructure obj
            ss = SentenceStructure(sentence)

            #Add SentenceStructure obj to the list
            docSentenceStructureList.append(ss)        

        #Strip the extension from the file to get the document name
        docName = os.path.splitext(document)[0]

        #Add the SentenceStructureList to the dictionary
        docDictionary[docName] = docSentenceStructureList

        #Close the document
        doc.close()
        
    #Return to original path
    os.chdir(cwd)
    
    #Return the dictionary
    return docDictionary

#Author: Evan French
def CreateAnnotatedSentenceStructures(ann_file_path, raw_file_path):
    """
    Create SentenceStructures from raw documents and annotate them
    
    :param ann_file_path: Path to directory where annotation documents are located
    :param raw_file_path: Path to directory where raw documents are located
    :return: Dictionary of lists of annotated SentenceStructure objects keyed on document name stripped of extension
    """
    #create annotation dictionary
    annDict = CreateAnnotationDictionary(ann_file_path)

    #create sentence structure dictionary
    ssDict = CreateSentenceStructures(raw_file_path)

    #Iterate over documents
    for key, value in ssDict.items():
        docAnnotations = annDict[key]
        docSentenceStructures = ssDict[key]

        #Annotate each sentence
        for index, ss in enumerate(docSentenceStructures):
            #Annotations only for this sentence
            annotations = [ann for ann in annDict[key] if ann.line == index + 1]

            #Updated SentenceStructure
            ss = AnnotateSentenceStructure(ss, annotations)

    #Return the updated ssDict
    return ssDict

#Author: Evan French
def AnnotateSentenceStructure(ss, annotations):
    """
    Annotates SentenceStructure object
    
    :param ss: SentenceStructure object
    :param annotions: list of annotations for the sentence
    :return: Annotated SentenceStructure object
    """

    #Iterate over distinct annotations for a sentence
    for m in annotations:
        for j in range(m.startWord, m.endWord + 2):
            if j == m.startWord:
                ss.originalSentenceArray[j][1] = m.label + ':Start'
            elif j == m.endWord + 1:
                ss.originalSentenceArray[j][1] = m.label + ':End'
            else:
                ss.originalSentenceArray[j][1] = m.label
    return ss

#Author: Evan French
"""
Iterates through all annotation documents in the directory specified and creates a dictionary keyed on file name 
(without extension) with a list Annotation objects as the value
"""
def CreateAnnotationDictionary(annotation_file_path):
    """
    Create Annotations from raw documents
    
    :param annotation_file_path: Path to directory where annotation documents are located
    :return: Dictionary of lists of Annotation objects keyed on document name stripped of extension
    """
    
    #Create a dictionary of documents
    docDictionary = {}

    # cd into annotation file directory
    cwd = os.getcwd()
    os.chdir(annotation_file_path)

    #Iterate over documents in the annotation_file_path directory
    for document in os.listdir():

        #Instantiate a list to hold Annotations for each document
        annotationList = []

        #Open the document
        doc = open(document, "r")

        #Iterate over lines in the document
        for line in doc.readlines():

            #Create an Annotation obj
            an = Annotation(line)

            #Add Annotation obj to the list
            annotationList.append(an)        

        #Strip the extension from the file to get the document name
        docName = os.path.splitext(document)[0]

        #Add the AnnotationList to the dictionary
        docDictionary[docName] = annotationList

        #Close the document
        doc.close()
        
    #Return to the original directory
    os.chdir(cwd)

    #Return the dictionary
    return docDictionary

if __name__ == "__main__":
    main()
