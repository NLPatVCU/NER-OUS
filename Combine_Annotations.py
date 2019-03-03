#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
This is a function that takes in annoation files from 3 folders removes overlapping
and duplicate annotations and returns a annotation file with supporting text file. Each time you run this funtion
all files contined within the folders created by this function will be deleted and then new files 
will be loaded. Save any prior runs somewhere else if needed. 
Bill Cramer
3-1-2019

treatmentFolder = folder where treatment annotations are stored
testFolder = folder where test annotations are stored
problemFolder = folder where problem annotations are stored
txtDir = folder where text files that match the annotations files are stored
outputDir = the directory where you want the output folder containing the output subfolders/files

"""
import re
import csv
import pandas as pd
import os
from shutil import copyfile
from datetime import datetime
import traceback

treatmentFolder = 'C:/Users/bat/Downloads/what5/treatmentFolder/'
testFolder = 'C:/Users/bat/Downloads/what5/testFolder/'
problemFolder = 'C:/Users/bat/Downloads/what5/problemFolder/'
txtDir = 'C:/Users/bat/Downloads/what5/postProcessedTXTFiles/'
outputDir = 'C:/Users/bat/Downloads/what5/'

# treatmentFolder = 'C:/Users/wccramer/Desktop/Downloads/what5/treatmentFolder/'
# testFolder = 'C:/Users/wccramer/Desktop/Downloads/what5/testFolder/'
# problemFolder = 'C:/Users/wccramer/Desktop/Downloads/what5/problemFolder/'
# txtDir = 'C:/Users/wccramer/Desktop/Downloads/what5/postProcessedTXTFiles/'
# outputDir = 'C:/Users/wccramer/Desktop/Downloads/what5/'



def combineAnnotations(treatmentFolder,testFolder,problemFolder,txtDir,outputDir):
    
    '''
    This area creates the output folder structure
    '''
    
    #function to create new sub output directory for final training files 
    finalOutputSubDirectory = 'finalTraining/'
    if os.path.exists(outputDir+finalOutputSubDirectory):
        for the_file in os.listdir(outputDir+finalOutputSubDirectory):
            file_path = os.path.join(outputDir+finalOutputSubDirectory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e) 
    else:
        os.makedirs(outputDir+finalOutputSubDirectory)

    finalOutputDir = outputDir+finalOutputSubDirectory


    #function to create new sub output directory for final processed annotations files 
    postFilteredAnnoSubDirectory = 'postfilteredAnnoFiles/'
    if os.path.exists(finalOutputDir+postFilteredAnnoSubDirectory):
        for the_file in os.listdir(finalOutputDir+postFilteredAnnoSubDirectory):
            file_path = os.path.join(finalOutputDir+postFilteredAnnoSubDirectory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e) 
    else:
        os.makedirs(finalOutputDir+postFilteredAnnoSubDirectory)         
    finalAnnoFiles = finalOutputDir+postFilteredAnnoSubDirectory   

    #function to create new sub output directory for txt files matching the final processed annoations files
    matchingtxtSubDirectory = 'matchingTXTFiles/'
    if os.path.exists(finalOutputDir+matchingtxtSubDirectory):
        for the_file in os.listdir(finalOutputDir+matchingtxtSubDirectory):
            file_path = os.path.join(finalOutputDir+matchingtxtSubDirectory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e) 
    else:
        os.makedirs(finalOutputDir+matchingtxtSubDirectory)          
    finalTxtFiles = finalOutputDir+matchingtxtSubDirectory    

    
    
    '''
    This area collects the files from each annoation folder  
    '''
    numberOfProblemFiles = []
    for problemFile in os.listdir(problemFolder):

        #captaure the input text files' name only without the file type ending
        nameOnly = re.sub(r'\.con','',str(problemFile))
        numberOfProblemFiles.append(nameOnly)
    
    numberOfTestFiles = []    
    for testFiles in os.listdir(testFolder):
        
        #captaure the input text files' name only without the file type ending
        nameTestOnly = re.sub(r'\.con','',str(testFiles))
        numberOfTestFiles.append(nameTestOnly)
    
    numberOfTreatmentFiles = []
    for treatmentFiles in os.listdir(treatmentFolder):
        #captaure the input text files' name only without the file type ending
        nameTreatmentOnly = re.sub(r'\.con','',str(treatmentFiles))
        numberOfTreatmentFiles.append(nameTreatmentOnly)
    
    #error checking for number of files in each folder above to make sure the len of the files match in each folder
    checkLoop = [1]
    for checkIt in checkLoop:
        if len(numberOfTreatmentFiles) != len(numberOfTestFiles) or len(numberOfTestFiles) != len(numberOfProblemFiles):
            print("something is wrong with the numbers of files in target/treatment/test")
            break
        else:
            #if no errors, open each annotation file
            completedList = []
            for theFiles in numberOfProblemFiles:
                with open(problemFolder+theFiles+'.con') as daProblemFile:#eachFile
                    with open(testFolder+theFiles+'.con') as daTestFile:
                        with open(treatmentFolder+theFiles+'.con') as daTreatmentFile:
                            #print('starting file: ',theFiles)
                            try:
                                #create empty list to hold function results 
                                #get the row number and each line to identify the span number for each comma
                                #create dataframe to hold results
                                #print(theFiles)
                                #helper function to process the input file and spit out a data for a dataFrame
                                completedList.append(theFiles)
                                completedTotal = str(len(completedList)) 
                                totalFiles = str(len(numberOfProblemFiles))
                                def spitOutaDF(inputFile):

                                    data2 = []

                                    finalDF = pd.DataFrame()

                                    for i,l in enumerate(inputFile):
                                        #print(eachFile)
                                        #print(i,l)
                                        commaSpans = []
                                        commaStarts = []
                                        commaEnds = []
                                        commaGroups = []

                                        targetComma = '\"'
                                        commaCompile = re.compile(targetComma)
                                        findComma = commaCompile.finditer(l)
                                        for spans in findComma:
                                            commaSpans.append(spans)
                                            #print(spans)

                                    #pull the span info and append to the approprate list
                                        for items in commaSpans:
                                            spanStarts = items.start()
                                            spansEnds = items.end()
                                            spansGroups = items.group()
                                            commaStarts.append(spanStarts)
                                            commaEnds.append(spansEnds)
                                            commaGroups.append(spansGroups)
                                        #print(commaEnds)

                                    #get the locations of the phrases between the commas and store in lists
                                        phraseStarts = commaStarts[0::4]
                                        phraseEnds = commaEnds[1::4]
                                        phraseStarting = []
                                        phraseEnding = []
                                        phraseList = []
                                        combined = []
                                        #filter for getting pharse start/ends
                                        #pull the phrases out the put in a list
                                        for phStarts in phraseStarts:
                                            phraseStarting.append((phStarts+1))
                                        for phEnds in phraseEnds:
                                            phraseEnding.append((phEnds-1))
                                        phraseResults = map(lambda x, y: l[x:y],phraseStarting,phraseEnding)
                                        phraseRAppend = list(phraseResults)
                                        phraseList.append(phraseRAppend[0])


                                    #pull the classes out and put in a list
                                        classesStarts = commaStarts[2::4]
                                        classesEnds = commaEnds[3::4]
                                        classStart = []
                                        classEnd = []
                                        classList = []
                                        for classStarts in classesStarts:
                                            classStart.append((classStarts+1))
                                        for classEnds in classesEnds:
                                            classEnd.append((classEnds-1))
                                        classResults = map(lambda m, n: l[m:n],classStart,classEnd)
                                        classRAppend = list(classResults)
                                        classList.append(classRAppend[0])

                                        #pull the numbers/positions from each line
                                        numberSpans = []
                                        numberStarts = []
                                        numberEnds = []
                                        numberGroups = []
                                        numberSpanz = []

                                        targetNumber = '\d+\:\d+'
                                        numberCompile = re.compile(targetNumber)
                                        findNumber = numberCompile.finditer(l)
                                        for spanz in findNumber:
                                            numberSpans.append(spanz)
                                        #pull the span info and append to the approprate list
                                        for itemz in numberSpans:
                                            numberStartz = itemz.start()
                                            numberEndz = itemz.end()
                                            numberGroupz = itemz.group()
                                            numberSpanc = itemz.span()
                                            numberSpanz.append(numberSpanc)
                                            numberStarts.append(numberStartz)
                                            numberEnds.append(numberEndz)
                                            numberGroups.append(numberGroupz)


                                        row = []
                                        rowz = []
                                        indexNumbers = []
                                        indexStart = []
                                        indexEnd = []
                                        df = pd.DataFrame()
                                        for rows in numberSpanz:
                                            cut = l[rows[0]:rows[1]]
                                            rowNumber = re.sub(r'\:\d+','',cut)
                                            row.append(int(rowNumber))
                                            indexNums = re.sub(r'\d+\:','',cut)
                                            indexNumbers.append(int(indexNums))
                                            indexToNumbers = int(indexNums)
                                            #print(indexNums)
                                            #indexStart.append(indexToNumbers[0])
                                            #indexEnd.append(indexToNumbers[1])

                                        rowz.append(row[0])
                                        indexStart.append(indexNumbers[0])
                                        indexEnd.append(indexNumbers[1])

                                        #print(indexNumbers)

                                        data = {'row':rowz[0],'startIndex':indexStart[0],'endIndex':indexEnd[0],'class':classList[0],'phrase':phraseList[0]}

                                        data2.append(data)

        #                             noEmptyData = []
        #                             for dropEmpty in data2:
        #                                 if len(dropEmpty)>0:
        #                                     noEmptyData.append(dropEmpty)
        #                                 else:
        #                                     pass
                                    return(data2)

                                testData = spitOutaDF(daTestFile)
                                treatmentData = spitOutaDF(daTreatmentFile)
                                problemData = spitOutaDF(daProblemFile)
                                #print(testData)
                                #create dataframe from the data list
                                df = pd.DataFrame(testData)  
                                df = df.append(treatmentData)
                                df = df.append(problemData)
                                #print(df)




                                #print(df)    
                                #create a df that uses the df above to return a df that has unique rows
                                uniqueDF = df.groupby('row').filter(lambda x: len(x) == 1).reset_index(drop=True)
                                #sort the rows by acending starting with the startIndex then by endIndex and reset the indexes
                                uniqueDF = uniqueDF[['startIndex','endIndex','row','class','phrase']].sort_values(by=['startIndex','endIndex']).reset_index(drop=True)

                                #create a df that uses the df above to return a df that without unique rows
                                nonUniqueDF = df.groupby('row').filter(lambda x: len(x) > 1).reset_index(drop=True)
                                #sort the values of the df by start then end
                                nonUniqueDF = nonUniqueDF[['startIndex','endIndex','row','class','phrase']].sort_values(by=['startIndex','endIndex']).reset_index(drop=True)
                                #create a grouping by the row numbers 
                                groupNonUniqueDF = nonUniqueDF.groupby('row')
                                # create a loop to process the grouped df
                                completeFinal = pd.DataFrame()
                                dfNonOverlays = pd.DataFrame(uniqueDF)

                                #this is where the good stuff happens 
                                for uniqueRow, dFrame in groupNonUniqueDF:
                                    dfHoldDF = dFrame
                                    #create columns that will indicate if tokens overlay and if classes are the same in rows above and below

                                    dfHoldDF = dfHoldDF.reset_index(drop=True)

                                    while len(dfHoldDF) > 0:
                                        # this function looks at each row and determins if the next row matches the conditions or not
                                        dfHoldDF['tokenOverlayDown'] = (dfHoldDF['startIndex'] <= dfHoldDF['startIndex'].shift(periods=-1))&(dfHoldDF['endIndex'] >= dfHoldDF['startIndex'].shift(periods=-1)) 
                                        dfHoldDF['classOverayDown'] = (dfHoldDF['class'] == dfHoldDF['class'].shift(periods=-1))
                                        # sort the columns 
                                        dfHoldDF = dfHoldDF[['startIndex','endIndex','row','class','phrase','tokenOverlayDown','classOverayDown']].reset_index(drop=True)

                                        if len(dfHoldDF) == 1:
                                            if dfHoldDF['class'].iloc[0] == 'toss':
                                                dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0])

                                            else:
                                                dfNonOverlays = dfNonOverlays.append(dfHoldDF.iloc[0])
                                                dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0])


                                        elif len(dfHoldDF) > 1:
                                            if dfHoldDF['tokenOverlayDown'].iloc[0] == True:
                                                #get the highest end token number from row 0 in postion 0 and 2nd highest from row 1 in postion 1 in a list 
                                                bigestEndNumber = sorted([dfHoldDF['endIndex'].iloc[0],dfHoldDF['endIndex'].iloc[1]],reverse=True)

                                                #get the start and end tokens for our target phrase 
                                                phraseStartTokenNumber = dfHoldDF['startIndex'].iloc[0]
                                                phraseEndTokenNumber = bigestEndNumber[0]

                                                #create a list of the words in the first row
                                                firstPhrase = dfHoldDF['phrase'].iloc[0].split()

                                                #create an empty list to hold the range vaules "indexes" for the first row phrase
                                                firstPhraseList = []

                                                #get the range values for the first row phrase and return it to the list above
                                                for firstPhraseRange in range(dfHoldDF['startIndex'].iloc[0],(dfHoldDF['endIndex'].iloc[0]+1)):
                                                    firstPhraseList.append(firstPhraseRange)

                                                #create a list using the 2nd row words
                                                secondPhrase = dfHoldDF['phrase'].iloc[1].split()

                                                #create an empty list to hold the range values for the indexes of the 2nd row words
                                                secondPhraseList = []

                                                #get the range values for the 2nd row phrase and return it to the list above
                                                for secondPhraseRange in range(dfHoldDF['startIndex'].iloc[1],(dfHoldDF['endIndex'].iloc[1]+1)):
                                                    secondPhraseList.append(secondPhraseRange)

                                                #create dict from the lists
                                                firstDict = dict(zip(firstPhraseList,firstPhrase))
                                                secondDict = dict(zip(secondPhraseList,secondPhrase))
                                                thirdDict = firstDict.update(secondDict)

                                                #create set using the indexes from the two rows
                                                setIt = sorted(list(set(firstPhraseList+secondPhraseList)))

                                                #use this set above to return the words 
                                                finalPhraseList = [firstDict[y_] for y_ in setIt]
                                                finalPhrase = ' '.join(finalPhraseList)


                                                # determine the class relation between the 0 and 1 rows F conflict T they are the same
                                                if dfHoldDF['classOverayDown'].iloc[0] == False:

                                                    dfHoldDF.loc[-1] = [dfHoldDF['startIndex'].iloc[0],bigestEndNumber[0],dfHoldDF['row'].iloc[0],'toss',finalPhrase,dfHoldDF['tokenOverlayDown'].iloc[1],dfHoldDF['classOverayDown'].iloc[1]]
                                                    dfHoldDF = dfHoldDF.drop(columns=['tokenOverlayDown','classOverayDown'])
                                                    dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0:2])
                                                    dfHoldDF.index = dfHoldDF.index + 1  
                                                    dfHoldDF = dfHoldDF.sort_index()

                                                elif dfHoldDF['class'].iloc[0] == 'toss':
                                                    dfHoldDF.loc[-1] = [dfHoldDF['startIndex'].iloc[0],bigestEndNumber[0],dfHoldDF['row'].iloc[0],'toss',finalPhrase,dfHoldDF['tokenOverlayDown'].iloc[1],dfHoldDF['classOverayDown'].iloc[1]]
                                                    dfHoldDF = dfHoldDF.drop(columns=['tokenOverlayDown','classOverayDown'])
                                                    dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0:2])
                                                    dfHoldDF.index = dfHoldDF.index + 1  
                                                    dfHoldDF = dfHoldDF.sort_index()


                                                else:
                                                    dfHoldDF.loc[-1] = [dfHoldDF['startIndex'].iloc[0],bigestEndNumber[0],dfHoldDF['row'].iloc[0],dfHoldDF['class'].iloc[0],finalPhrase,dfHoldDF['tokenOverlayDown'].iloc[1],dfHoldDF['classOverayDown'].iloc[1]]
                                                    dfHoldDF = dfHoldDF.drop(columns=['tokenOverlayDown','classOverayDown'])
                                                    dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0:2])
                                                    dfHoldDF.index = dfHoldDF.index + 1
                                                    dfHoldDF = dfHoldDF.sort_index()


                                            elif dfHoldDF['tokenOverlayDown'].iloc[0] == False:

                                                if dfHoldDF['class'].iloc[0] == 'toss':
                                                    dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0]) 

                                                else:
                                                    dfNonOverlays = dfNonOverlays.append(dfHoldDF.iloc[0])
                                                    dfHoldDF = dfHoldDF.drop(dfHoldDF.index[0])
                                            else:
                                                pass


                                        else:
                                            pass

                                ''' 
                                check to see if the DF that outputs our final post processed results actually exhists.
                                If it does not then make sure the text file does not end up in our final output folder.
                                '''


                                if len(dfNonOverlays) > 0:
                                    dfNonOverlays['endIndex'] = dfNonOverlays['endIndex'].astype(int)
                                    #onOverlays['endIndex'] = dfNonOverlays['endIndex'].astype(str)
                                    dfNonOverlays['startIndex'] = dfNonOverlays['startIndex'].astype(int)
                                    #dfNonOverlays['startIndex'] = dfNonOverlays['startIndex'].astype(str)
                                    dfNonOverlays['row'] = dfNonOverlays['row'].astype(int)
                                    #dfNonOverlays['row'] = dfNonOverlays['row'].astype(str)
                                    dfNonOverlays = dfNonOverlays[['startIndex','endIndex','row','class','phrase']]
                                    # this is the funciton that builds the output annotation file

                                    coutz = 0
                                    phraseListing = []
                                    for finalPost in dfNonOverlays.itertuples():  
                                        #print('finalpost: ', finalPost)
                                        #print('finalpost: ', finalPost[5])
                                        #print('finalpost type: ', type(finalPost[1]))
                                        phraz = str(finalPost[5])
                                        #print ('phrase is: ',phraz)
                                        #print('phrase type: ', type(phraz))
                                        rawz = str(finalPost[3])
                                        #print('row: ',rawz)
                                        #print('row: ',type(rawz))
                                        stazT = str(finalPost[1])
                                        #print('start: ', stazT)
                                        #print('start: ', type(stazT))
                                        enDz = str(finalPost[2])
                                        #print('end: ',enDz)
                                        #print('end: ',type(enDz))
                                        claz = str(finalPost[4])
                                        #print('class: ',claz)
                                        #print('class: ',type(claz))

                                        annoPhrase = 'c="'+phraz+'" '+rawz+':'+stazT+' '+rawz+':'+enDz+'||t='+'"'+claz+'"'
                                        #print('annophrase: ',annoPhrase)
                                        phraseListing.append(annoPhrase)
                                        annoFileName = theFiles+'.con'
                                        #print('fileName: ', annoFileName)
                        #                 with open((finalAnnoFiles+annoFileName), 'a') as annoFileBuild:
                        #                     annoFileBuild.write(annoPhrase+"\n")
                                        annoFileBuild = open((finalAnnoFiles+annoFileName), 'a')
                                        #print(annoFileBuild)
                                        annoFileBuild.write(annoPhrase)
                                        annoFileBuild.write("\n")
                                        annoFileBuild.close()

                                        #copy the matching text file to the new output directory
                                        matchingTxtFile = nameOnly+'.txt'
                                        copyfile(txtDir+matchingTxtFile,finalTxtFiles+matchingTxtFile)
                                else:
                                    pass
                                #create and output complete work to the log file 
                                completed = open((finalOutputDir+'completedLog.txt'), 'a')
                                now = datetime.now()
                                completed.write(theFiles+'\n')
                                completed.write('total number of completed files is '+completedTotal+' out of '+totalFiles+'\n')
                                completed.write(str(now)+'\n\n')
                                completed.close()
                                #print('total number of completed files is ',completedTotal,' out of ',totalFiles)

                            except Exception:
                                with open(finalOutputDir+'probemfiles.txt', 'a') as dropSpot:
                                    now = datetime.now()
                                    dropSpot.write(theFiles)
                                    dropSpot.write("\n")
                                    dropSpot.write(str(now)+'\n')
                                    dropSpot.write('total number of completed files is '+completedTotal+' out of '+totalFiles+'\n')
                                    traceback.print_exc(file=dropSpot)
                                    dropSpot.write("\n\n\n")
                                continue

combineAnnotations(treatmentFolder,testFolder,problemFolder,txtDir,outputDir)

