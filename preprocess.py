#!/usr/bin/env python
# coding: utf-8

# In[2]:



"""

preprocess.py
Authors: Bill Cramer
Scope:
Takes in a file path that contains text documents and converts the text in each file
by converting all dates to a singular DATE and all numbers to a singular NUM. 
Returns an object of the post processed text file.
The funcation counts the number of lines and counts the number of tokens perline. 
If the output does not equal the input prints the name of the problem file along with
error difference in the len of the number of rows and also prints a dataframe containing 
the problem rows and counts of tokens per row. The error post-processed text file is also printed.
 

"""

import os, shutil
from os import listdir
from os.path import isfile, join
import pandas as pd
from os import listdir
from os.path import isfile
from io import StringIO
import numpy as np
import itertools
import re
from itertools import permutations
from operator import setitem




def preprocess(ogString):
    
    newString = ogString
    
    newString = newString.lower()
    
    newString = re.sub(r"\n",' \n ', newString)

    #### listing of symbols that seperate dates including spaces 
    dateSeparators = ['\-\s|\/\s|\.\s|\,\s|\s']

    #### listing of symbols that seperate dates without spaces
    dateSeparatorsNoSpace = ['\-|\/|\.|\,']

    #### listing of ways to represent days of the week     
    daysOfWeek = ['monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|mo|tue|tues|tu|wed|we|thur|thurs|th|thu|fri|fr|sat|sa|sun|su|\d\d|\d']

    #### listing of ways to represent months
    monthList = ['january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sept|oct|nov|dec|\d\d|\d']

    #### listing of ways to represent a year
    yearFormat = ['\d\d\d\d|\d\d']

    #### listing of ordinals for days of the week 
    dayOfWeekOrdinalIndicator = ['th|st|nd|rd|']


    #### listing of our date lists 
    dateFormat = [(yearFormat[0]), (daysOfWeek[0]), (monthList[0])]

    #### set counter to start at 4 as the max tokens for a date format example: wednesday, nov 21st 1982
    counter = 4

    #### use a while loop that stops at 2 tokens for a date format to iterate
    while counter > 1:
        #### use a cartesian product to loop through all combinations of our date formats 
        combo = itertools.product(dateFormat, repeat=counter)
        #### for loop to process the cartesian product loop
        for tt in combo:
            #### need to make 2 copies of the cartesian product list one for with spaces and one w/o
            makeList = list(tt)
            makeList1 = list(tt)

            
                       #### loop to convert dates formats with spaces to DATE matching the same amount of date format tokens 
            howLong = len(makeList1)
            step = 1
           
            while step <= howLong+1:
                makeList1.insert(step, dateSeparators[0])
                step+=(1+1)

            index4DaysOfWeek = [i for i,x in enumerate(makeList1) if x == daysOfWeek[0]]

            addOrdinal = ["("+daysOfWeek[0]+")("+dayOfWeekOrdinalIndicator[0]+")"]

            for location, replacement in zip(index4DaysOfWeek,(addOrdinal[0:]*(len(index4DaysOfWeek)))):
                setitem(makeList1,location, replacement)     


            if len(makeList1) == 7:
                
                newString = re.sub(r"(("+makeList1[0]+")("+makeList1[1]+")("+makeList1[2]+")("+makeList1[3]+")("+
                                   makeList1[4]+")("+makeList1[5]+")("+makeList1[6]+"))",'DATE DATE DATE DATE',newString)
                #newString = re.sub('\b\d+\b', 'NUM',newString)
            else:
                if len(makeList1) == 5:
                    newString = re.sub(r"(("+makeList1[0]+")("+makeList1[1]+")("+makeList1[2]+")("+makeList1[3]+")("+
                                           makeList1[4]+"))",'DATE DATE DATE',newString)
                else:
                    if len(makeList1) == 4:
                        newString = re.sub(r"(("+makeList1[0]+")("+makeList1[1]+")("+makeList1[2]+"))",'DATE DATE',newString)
                    else:
                        pass

            
            
            
            
            
            #### loop to convert dates formats with no spaces to DATE
            howLong1 = len(makeList)
            step1 = 1
            while step1 <= howLong1+1:
                makeList.insert(step1, dateSeparatorsNoSpace[0])
                step1+=(1+1)

            if len(makeList) == 7:

                newString = re.sub(r"(("+makeList[0]+")("+makeList[1]+")("+makeList[2]+")("+makeList[3]+")("+makeList[4]+")("+makeList[5]+")("+makeList[6]+"))",'DATE',newString)
            else:
                if len(makeList) == 5:
                    newString = re.sub(r"(("+makeList[0]+")("+makeList[1]+")("+makeList[2]+")("+makeList[3]+")("+makeList[4]+"))",'DATE',newString)
                else:
                    if len(makeList) == 4:
                        newString = re.sub(r"(("+makeList[0]+")("+makeList[1]+")("+makeList[2]+"))",'DATE',newString)
                    else:
                        pass


 
        counter = counter-1

    #clean up DATES that have characters on either end     
    newString = re.sub('\S*\w*DATE\w*\S*', 'DATE',newString)  
        
    #newString = re.sub('\b\d+\b', 'NUM',newString)
    
    #### this ends the date processing section     
    #####################################################################################    
    #### this starts the number processing section 
    

        #################################################################################################

    #### the following finds our target list idenifers and converts to unicode characters 

    numberMap1 = {r'\d+\.\)':'NUM',
                  '1.)':u'\u0241',
                  '2.)':u'\u0242',
                  '3.)':u'\u0243',
                  '4.)':u'\u0244',
                  '5.)':u'\u0245',
                  '6.)':u'\u0246',
                  '7.)':u'\u0247',
                  '8.)':u'\u0248',
                  '9.)':u'\u0249',
                  '10.)':u'\u0250',
                  '11.)':u'\u0251',
                  '12.)':u'\u0252',
                  '13.)':u'\u0253',
                  '14.)':u'\u0254',
                  '15.)':u'\u0255',
                  '16.)':u'\u0256',
                  '17.)':u'\u0257',
                  '18.)':u'\u0258',
                  '19.)':u'\u0259',
                  '20.)':u'\u0260'}

    replaceNumberMap1 = re.sub(r'\d+\.\)', lambda x: numberMap1.get(x.group(),x.group(0)),newString)

    numberMap2 = {r'\d+\)':'NUM',
                  '1)':u'\u0261',
                  '2)':u'\u0262',
                  '3)':u'\u0263',
                  '4)':u'\u0264',
                  '5)':u'\u0265',
                  '6)':u'\u0266',
                  '7)':u'\u0267',
                  '8)':u'\u0268',
                  '9)':u'\u0269',
                  '10)':u'\u0270',
                  '11)':u'\u0271',
                  '12)':u'\u0272',
                  '13)':u'\u0273',
                  '14)':u'\u0274',
                  '15)':u'\u0275',
                  '16)':u'\u0276',
                  '17)':u'\u0277',
                  '18)':u'\u0278',
                  '19)':u'\u0279',
                  '20)':u'\u0280'}

    replaceNumberMap2 = re.sub(r'\d+\)', lambda x: numberMap2.get(x.group(),x.group(0)),replaceNumberMap1)


    numberMap4 = {r'd+\.\s':'NUM',
                  '1. ':u'\u0200',
                  '2. ':u'\u0201',
                  '3. ':u'\u0202',
                  '4. ':u'\u0203',
                  '5. ':u'\u0204',
                  '6. ':u'\u0205',
                  '7. ':u'\u0206',
                  '8. ':u'\u0207',
                  '9. ':u'\u0208',
                  '10. ':u'\u0209',
                  '11. ':u'\u0210',
                  '12. ':u'\u0211',
                  '13. ':u'\u0212',
                  '14. ':u'\u0213',
                  '15. ':u'\u0214',
                  '16. ':u'\u0215',
                  '17. ':u'\u0216',
                  '18. ':u'\u0217',
                  '19. ':u'\u0218',
                  '20. ':u'\u0219'}

    replaceNumberMap4 = re.sub(r'\d+\.\s', lambda x: numberMap4.get(x.group(),x.group(0)),replaceNumberMap2)


    #### convert all remining numbers to NUM
    numbers2NUM1 = re.sub(r'(\d+)','NUM',replaceNumberMap4)


    ### remap the mapping of list identifers back to their original form

    remapNumberMap1 = {u'\u0241':'1.)',
                       u'\u0242':'2.)',
                       u'\u0243':'3.)',
                       u'\u0244':'4.)',
                       u'\u0245':'5.)',
                       u'\u0246':'6.)',
                       u'\u0247':'7.)',
                       u'\u0248':'8.)',
                       u'\u0249':'9.)',
                       u'\u0250':'10.)',
                       u'\u0251':'11.)',
                       u'\u0252':'12.)',
                       u'\u0253':'13.)',
                       u'\u0254':'14.)',
                       u'\u0255':'15.)',
                       u'\u0256':'16.)',
                       u'\u0257':'17.)',
                       u'\u0258':'18.)',
                       u'\u0259':'19.)',
                       u'\u0260':'20.)'}


    remapNumberMap11= u'\u0241'
    remapNumberMap12= u'\u0242'
    remapNumberMap13= u'\u0243'
    remapNumberMap14= u'\u0244'
    remapNumberMap15= u'\u0245'
    remapNumberMap16= u'\u0246'
    remapNumberMap17= u'\u0247'
    remapNumberMap18= u'\u0248'
    remapNumberMap19= u'\u0249'
    remapNumberMap110= u'\u0250'
    remapNumberMap111= u'\u0251'
    remapNumberMap112= u'\u0252'
    remapNumberMap113= u'\u0253'
    remapNumberMap114= u'\u0254'
    remapNumberMap115= u'\u0255'
    remapNumberMap116= u'\u0256'
    remapNumberMap117= u'\u0257'
    remapNumberMap118= u'\u0258'
    remapNumberMap119= u'\u0259'
    remapNumberMap120= u'\u0260'



    replaceRemapNumberMap1 = re.sub(remapNumberMap11, '1.)',numbers2NUM1)
    replaceRemapNumberMap11 = re.sub(remapNumberMap12, '2.)',replaceRemapNumberMap1)
    replaceRemapNumberMap12 = re.sub(remapNumberMap13, '3.)',replaceRemapNumberMap11)
    replaceRemapNumberMap13 = re.sub(remapNumberMap14, '4.)',replaceRemapNumberMap12)
    replaceRemapNumberMap14 = re.sub(remapNumberMap15, '5.)',replaceRemapNumberMap13)
    replaceRemapNumberMap15 = re.sub(remapNumberMap16, '6.)',replaceRemapNumberMap14)
    replaceRemapNumberMap16 = re.sub(remapNumberMap17, '7.)',replaceRemapNumberMap15)
    replaceRemapNumberMap17 = re.sub(remapNumberMap18, '8.)',replaceRemapNumberMap16)
    replaceRemapNumberMap18 = re.sub(remapNumberMap19,'9.)',replaceRemapNumberMap17)
    replaceRemapNumberMap19= re.sub(remapNumberMap110, '10.)',replaceRemapNumberMap18)
    replaceRemapNumberMap110 = re.sub(remapNumberMap111, '11.)',replaceRemapNumberMap19)
    replaceRemapNumberMap111 = re.sub(remapNumberMap112, '12.)',replaceRemapNumberMap110)
    replaceRemapNumberMap112 = re.sub(remapNumberMap113, '13.)',replaceRemapNumberMap111)
    replaceRemapNumberMap113 = re.sub(remapNumberMap114, '14.)',replaceRemapNumberMap112)
    replaceRemapNumberMap114 = re.sub(remapNumberMap115, '15.)',replaceRemapNumberMap113)
    replaceRemapNumberMap115 = re.sub(remapNumberMap116, '16.)',replaceRemapNumberMap114)
    replaceRemapNumberMap116 = re.sub(remapNumberMap117, '17.)',replaceRemapNumberMap115)
    replaceRemapNumberMap117 = re.sub(remapNumberMap118, '18.)',replaceRemapNumberMap116)
    replaceRemapNumberMap118 = re.sub(remapNumberMap119, '19.)',replaceRemapNumberMap117)
    replaceRemapNumberMap119 = re.sub(remapNumberMap120, '20.)',replaceRemapNumberMap118)



    remapNumberMap2 = {u'\u0261':'1)',
                       u'\u0262':'2)',
                       u'\u0263':'3)',
                       u'\u0264':'4)',
                       u'\u0265':'5)',
                       u'\u0266':'6)',
                       u'\u0267':'7)',
                       u'\u0268':'8)',
                       u'\u0269':'9)',
                       u'\u0270':'10)',
                       u'\u0271':'11)',
                       u'\u0272':'12)',
                       u'\u0273':'13)',
                       u'\u0274':'14)',
                       u'\u0275':'15)',
                       u'\u0276':'16)',
                       u'\u0277':'17)',
                       u'\u0278':'18)',
                       u'\u0279':'19)',
                       u'\u0280':'20)'}

    remapNumberMap21= u'\u0261'
    remapNumberMap22= u'\u0262'
    remapNumberMap23= u'\u0263'
    remapNumberMap24= u'\u0264'
    remapNumberMap25= u'\u0265'
    remapNumberMap26= u'\u0266'
    remapNumberMap27= u'\u0267'
    remapNumberMap28= u'\u0268'
    remapNumberMap29= u'\u0269'
    remapNumberMap210= u'\u0270'
    remapNumberMap211= u'\u0271'
    remapNumberMap212= u'\u0272'
    remapNumberMap213= u'\u0273'
    remapNumberMap214= u'\u0274'
    remapNumberMap215= u'\u0275'
    remapNumberMap216= u'\u0276'
    remapNumberMap217= u'\u0277'
    remapNumberMap218= u'\u0278'
    remapNumberMap219= u'\u0279'
    remapNumberMap220= u'\u0280'



    replaceRemapNumberMap2 = re.sub(remapNumberMap21, '1)',replaceRemapNumberMap119)
    replaceRemapNumberMap21 = re.sub(remapNumberMap22, '2)',replaceRemapNumberMap2)
    replaceRemapNumberMap22 = re.sub(remapNumberMap23, '3)',replaceRemapNumberMap21)
    replaceRemapNumberMap23 = re.sub(remapNumberMap24, '4)',replaceRemapNumberMap22)
    replaceRemapNumberMap24 = re.sub(remapNumberMap25, '5)',replaceRemapNumberMap23)
    replaceRemapNumberMap25 = re.sub(remapNumberMap26, '6)',replaceRemapNumberMap24)
    replaceRemapNumberMap26 = re.sub(remapNumberMap27, '7)',replaceRemapNumberMap25)
    replaceRemapNumberMap27 = re.sub(remapNumberMap28,'8)',replaceRemapNumberMap26)
    replaceRemapNumberMap28 = re.sub(remapNumberMap29, '9)',replaceRemapNumberMap27)
    replaceRemapNumberMap29 = re.sub(remapNumberMap210, '10)',replaceRemapNumberMap28)
    replaceRemapNumberMap210 = re.sub(remapNumberMap211, '11)',replaceRemapNumberMap29)
    replaceRemapNumberMap211 = re.sub(remapNumberMap212, '12)',replaceRemapNumberMap210)
    replaceRemapNumberMap212 = re.sub(remapNumberMap213, '13)',replaceRemapNumberMap211)
    replaceRemapNumberMap213 = re.sub(remapNumberMap214, '14)',replaceRemapNumberMap212)
    replaceRemapNumberMap214 = re.sub(remapNumberMap215, '15)',replaceRemapNumberMap213)
    replaceRemapNumberMap215 = re.sub(remapNumberMap216, '16)',replaceRemapNumberMap214)
    replaceRemapNumberMap216 = re.sub(remapNumberMap217, '17)',replaceRemapNumberMap215)
    replaceRemapNumberMap217 = re.sub(remapNumberMap218, '18)',replaceRemapNumberMap216)
    replaceRemapNumberMap218 = re.sub(remapNumberMap219, '19)',replaceRemapNumberMap217)
    replaceRemapNumberMap219 = re.sub(remapNumberMap220, '20)',replaceRemapNumberMap218)


    remapNumberMap4 = {u'\u0200':'1. ',
                       u'\u0201':'2. ',
                       u'\u0202':'3. ',
                       u'\u0203':'4. ',
                       u'\u0204':'5. ',
                       u'\u0205':'6. ',
                       u'\u0206':'7. ',
                       u'\u0207':'8. ',
                       u'\u0208':'9. ',
                       u'\u0209':'10. ',
                       u'\u0210':'11. ',
                       u'\u0211':'12. ',
                       u'\u0212':'13. ',
                       u'\u0213':'14. ',
                       u'\u0214':'15. ',
                       u'\u0215':'16. ',
                       u'\u0216':'17. ',
                       u'\u0217':'18. ',
                       u'\u0218':'19. ',
                       u'\u0219':'20. '}

    remapNumberMap41= u'\u0200'
    remapNumberMap42= u'\u0201'
    remapNumberMap43= u'\u0202'
    remapNumberMap44= u'\u0203'
    remapNumberMap45= u'\u0204'
    remapNumberMap46= u'\u0205'
    remapNumberMap47= u'\u0206'
    remapNumberMap48= u'\u0207'
    remapNumberMap49= u'\u0208'
    remapNumberMap410= u'\u0209'
    remapNumberMap411= u'\u0210'
    remapNumberMap412= u'\u0211'
    remapNumberMap413= u'\u0212'
    remapNumberMap414= u'\u0213'
    remapNumberMap415= u'\u0214'
    remapNumberMap416= u'\u0215'
    remapNumberMap417= u'\u0216'
    remapNumberMap418= u'\u0217'
    remapNumberMap419= u'\u0218'
    remapNumberMap420= u'\u0219'


    replaceRemapNumberMap4 = re.sub(remapNumberMap41, '1. ',replaceRemapNumberMap219)
    replaceRemapNumberMap41 = re.sub(remapNumberMap42, '2. ',replaceRemapNumberMap4)
    replaceRemapNumberMap42 = re.sub(remapNumberMap43, '3. ',replaceRemapNumberMap41)
    replaceRemapNumberMap43 = re.sub(remapNumberMap44, '4. ',replaceRemapNumberMap42)
    replaceRemapNumberMap44 = re.sub(remapNumberMap45, '5. ',replaceRemapNumberMap43)
    replaceRemapNumberMap45 = re.sub(remapNumberMap46, '6. ',replaceRemapNumberMap44)
    replaceRemapNumberMap46 = re.sub(remapNumberMap47, '7. ',replaceRemapNumberMap45)
    replaceRemapNumberMap47 = re.sub(remapNumberMap48, '8. ',replaceRemapNumberMap46)
    replaceRemapNumberMap48 = re.sub(remapNumberMap49, '9. ',replaceRemapNumberMap47)
    replaceRemapNumberMap49 = re.sub(remapNumberMap410, '10. ',replaceRemapNumberMap48)
    replaceRemapNumberMap410 = re.sub(remapNumberMap411, '11. ',replaceRemapNumberMap49)
    replaceRemapNumberMap411 = re.sub(remapNumberMap412, '12. ',replaceRemapNumberMap410)
    replaceRemapNumberMap412 = re.sub(remapNumberMap413, '13. ',replaceRemapNumberMap411)
    replaceRemapNumberMap413 = re.sub(remapNumberMap414, '14. ',replaceRemapNumberMap412)
    replaceRemapNumberMap414 = re.sub(remapNumberMap415, '15. ',replaceRemapNumberMap413)
    replaceRemapNumberMap415 = re.sub(remapNumberMap416, '16. ',replaceRemapNumberMap414)
    replaceRemapNumberMap416 = re.sub(remapNumberMap417, '17. ',replaceRemapNumberMap415)
    replaceRemapNumberMap417 = re.sub(remapNumberMap418, '18. ',replaceRemapNumberMap416)
    replaceRemapNumberMap418 = re.sub(remapNumberMap419, '19. ',replaceRemapNumberMap417)
    replaceRemapNumberMap419 = re.sub(remapNumberMap420, '20. ',replaceRemapNumberMap418)


    
    
    
    newString = replaceRemapNumberMap419
    
    newString = re.sub('\S*\w*NUM\w*\S*', 'NUM',newString)
    

     
    return(newString)
    
    
   
    









# In[ ]:




