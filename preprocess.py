"""
preprocess.py
Scope: Converts Dates to DATE and Numbers to NUM
Authors: Bill Cramer
"""

#TODO(Bill) Revamp the preprocessing module.
#TODO(Jeff) Make style doc compatible.

# Import packages
import re

"""
Takes in a string and converts all dates to a singular DATE and all numbers to a singular NUM. 
"""
def preprocess(text):
    
    preNum = re.sub(r'\d+\#|\d+\%|\d+\^|\d+\*','NUM',text)

    batch1 = re.sub(r'\d+\/\d+\/\d+','DATE',preNum)
    batch2 = re.sub(r'\d\d\d\d\-\d+\-\d+','DATE',batch1)
    #'9-11-2014'
    batch3 = re.sub(r'\d+\-\d+\-\d\d\d\d','DATE',batch2)
    #09.11.2014
    batch4 = re.sub(r'\d\d\d\d\.\d+\.\d+','DATE',batch3)
    batch5 = re.sub(r'\d+\.\d+\.\d\d\d\d','DATE',batch4)
    #'Monday, 3 of August 2006' 
    batch6 = re.sub(r'Monday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch5)
    batch6a = re.sub(r'Tuesday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6)
    batch6b = re.sub(r'Wednesday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6a)
    batch6c = re.sub(r'Thursday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6b)
    batch6d = re.sub(r'Friday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6c)
    batch6e = re.sub(r'Saturday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6d)
    batch6f = re.sub(r'Sunday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6e)
    batch6g = re.sub(r'monday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6f)
    batch6h = re.sub(r'tuesday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6g)
    batch6i = re.sub(r'wednesday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6h)
    batch6j = re.sub(r'thursday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6i)
    batch6k = re.sub(r'friday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6j)
    batch6l = re.sub(r'saturday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6k)
    batch6m = re.sub(r'sunday\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6l)
    batch6n = re.sub(r'MONDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6m)
    batch6o = re.sub(r'TUESDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6n)
    batch6p = re.sub(r'WEDNESDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6o)
    batch6q = re.sub(r'THURSDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6p)
    batch6r = re.sub(r'FRIDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6q)
    batch6s = re.sub(r'SATURDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6r)
    batch6t = re.sub(r'SUNDAY\,\s+\d+\s+\D+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE DATE',batch6s)

    #Sunday, 9 November 2014
    batch7 = re.sub(r'Sunday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch6t)
    batch7a = re.sub(r'Monday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7)
    batch7b = re.sub(r'Tuesday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7a)
    batch7c = re.sub(r'Wednesday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7b)
    batch7d = re.sub(r'Thursday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7c)
    batch7e = re.sub(r'Friday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7d)
    batch7f = re.sub(r'Saturday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7e)
    batch7g = re.sub(r'sunday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7f)
    batch7h = re.sub(r'monday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7g)
    batch7i = re.sub(r'tuesday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7h)
    batch7j = re.sub(r'wednesday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7i)
    batch7k = re.sub(r'thursday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7j)
    batch7l = re.sub(r'friday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7k)
    batch7m = re.sub(r'saturday\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7l)
    batch7n = re.sub(r'SUNDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7m)
    batch7o = re.sub(r'MONDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7n)
    batch7p = re.sub(r'TUESDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7o)
    batch7q = re.sub(r'WEDNESDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7p)
    batch7r = re.sub(r'THURSDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7q)
    batch7s = re.sub(r'FRIDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7r)
    batch7t = re.sub(r'SATURDAY\,\s+\d+\s+\D+\s+\d\d\d\d','DATE DATE DATE DATE',batch7s)

    #11-18
    batch8 = re.sub(r'\d\d\-\d+','DATE',batch7t)


    sreplaceJan = re.sub(r'(Jan)\/\w+\/\w+','DATE', batch8)
    sreplaceJan1 = re.sub(r'(JAN)\/\w+\/\w+','DATE', sreplaceJan)
    sreplaceFeb = re.sub(r'(Feb)\/\w+\/\w+','DATE', sreplaceJan1)
    sreplaceFeb1 = re.sub(r'(FEB)\/\w+\/\w+','DATE', sreplaceFeb)
    sreplaceMar = re.sub(r'(Mar)\/\w+\/\w+','DATE', sreplaceFeb1)
    sreplaceMar1 = re.sub(r'(MAR)\/\w+\/\w+','DATE', sreplaceMar)
    sreplaceMar2 = re.sub(r'(March)\/\w+\/\w+','DATE', sreplaceMar1)
    sreplaceMar3 = re.sub(r'(MARCH)\/\w+\/\w+','DATE', sreplaceMar2)
    sreplaceApr = re.sub(r'(Apr)\/\w+\/\w+','DATE', sreplaceMar3)
    sreplaceApr1 = re.sub(r'(APR)\/\w+\/\w+','DATE', sreplaceApr)
    sreplaceApr2 = re.sub(r'(April)\/\w+\/\w+','DATE', sreplaceApr1)
    sreplaceApr3 = re.sub(r'(APRIL)\/\w+\/\w+','DATE', sreplaceApr2)
    sreplaceMay = re.sub(r'(May)\/\w+\/\w+','DATE', sreplaceApr3)
    sreplaceMay1 = re.sub(r'(MAY)\/\w+\/\w+','DATE', sreplaceMay)
    sreplaceJune = re.sub(r'(Jun)\/\w+\/\w+','DATE', sreplaceMay1)
    sreplaceJune1 = re.sub(r'(JUN)\/\w+\/\w+','DATE', sreplaceJune)
    sreplaceJune2 = re.sub(r'(June)\/\w+\/\w+','DATE', sreplaceJune1)
    sreplaceJune3 = re.sub(r'(JUNE)\/\w+\/\w+','DATE', sreplaceJune2)
    sreplaceJuly = re.sub(r'(July)\/\w+\/\w+','DATE', sreplaceJune3)
    sreplaceJuly1 = re.sub(r'(JULY)\/\w+\/\w+','DATE', sreplaceJuly)
    sreplaceAug = re.sub(r'(Aug)\/\w+\/\w+','DATE', sreplaceJuly1)
    sreplaceAug1 = re.sub(r'(AUG)\/\w+\/\w+','DATE', sreplaceAug)
    sreplaceSept = re.sub(r'(Sept)\/\w+\/\w+','DATE', sreplaceAug1)
    sreplaceSept1 = re.sub(r'(SEPT)\/\w+\/\w+','DATE', sreplaceSept)
    sreplaceOct = re.sub(r'(Oct)\/\w+\/\w+','DATE', sreplaceSept1)
    sreplaceOct1 = re.sub(r'(OCT)\/\w+\/\w+','DATE', sreplaceOct)
    sreplaceNov = re.sub(r'(Nov)\/\w+\/\w+','DATE', sreplaceOct1)
    sreplaceNov1 = re.sub(r'(NOV)\/\w+\/\w+','DATE', sreplaceNov)
    sreplaceDec = re.sub(r'(Dec)\/\w+\/\w+','DATE', sreplaceNov1)
    sreplaceDec1 = re.sub(r'(DEC)\/\w+\/\w+','DATE', sreplaceDec)

    sRreplaceJan = re.sub(r'\d+\/(Jan)\/\d+','DATE', sreplaceDec1)
    sRreplaceJan1 = re.sub(r'\d+\/(JAN)\/\d+','DATE', sRreplaceJan)
    sRreplaceFeb = re.sub(r'\d+\/(Feb)\/\d+','DATE', sRreplaceJan1)
    sRreplaceFeb1 = re.sub(r'\d+\/(FEB)\/\d+','DATE', sRreplaceFeb)
    sRreplaceMar = re.sub(r'\d+\/(Mar)\/\d+','DATE', sRreplaceFeb1)
    sRreplaceMar1 = re.sub(r'\d+\/(MAR)\/\d+','DATE', sRreplaceMar)
    sRreplaceMar2 = re.sub(r'\d+\/(March)\/\d+','DATE', sRreplaceMar1)
    sRreplaceMar3 = re.sub(r'\d+\/(MARCH)\/\d+','DATE', sRreplaceMar2)
    sRreplaceApr = re.sub(r'\d+\/(Apr)\/\d+','DATE', sRreplaceMar3)
    sRreplaceApr1 = re.sub(r'\d+\/(APR)\/\d+','DATE', sRreplaceApr)
    sRreplaceApr2 = re.sub(r'\d+\/(April)\/\d+','DATE', sRreplaceApr1)
    sRreplaceApr3 = re.sub(r'\d+\/(APRIL)\/\d+','DATE', sRreplaceApr2)
    sRreplaceMay = re.sub(r'\d+\/(May)\/\d+','DATE', sRreplaceApr3)
    sRreplaceMay1 = re.sub(r'\d+\/(MAY)\/\d+','DATE', sRreplaceMay)
    sRreplaceJune = re.sub(r'\d+\/(Jun)\/\d+','DATE', sRreplaceMay1)
    sRreplaceJune1 = re.sub(r'\d+\/(JUN)\/\d+','DATE', sRreplaceJune)
    sRreplaceJune2 = re.sub(r'\d+\/(June)\/\d+','DATE', sRreplaceJune1)
    sRreplaceJune3 = re.sub(r'\d+\/(JUNE)\/\d+','DATE', sRreplaceJune2)
    sRreplaceJuly = re.sub(r'\d+\/(July)\/\d+','DATE', sRreplaceJune3)
    sRreplaceJuly1 = re.sub(r'\d+\/(JULY)\/\d+','DATE', sRreplaceJuly)
    sRreplaceAug = re.sub(r'\d+\/(Aug)\/\d+','DATE', sRreplaceJuly1)
    sRreplaceAug1 = re.sub(r'\d+\/(AUG)\/\d+','DATE', sRreplaceAug)
    sRreplaceSept = re.sub(r'\d+\/(Sept)\/\d+','DATE', sRreplaceAug1)
    sRreplaceSept1 = re.sub(r'\d+\/(SEPT)\/\d+','DATE', sRreplaceSept)
    sRreplaceOct = re.sub(r'\d+\/(Oct)\/\d+','DATE', sRreplaceSept1)
    sRreplaceOct1 = re.sub(r'\d+\/(OCT)\/\d+','DATE', sRreplaceOct)
    sRreplaceNov = re.sub(r'\d+\/(Nov)\/\d+','DATE', sRreplaceOct1)
    sRreplaceNov1 = re.sub(r'\d+\/(NOV)\/\d+','DATE', sRreplaceNov)
    sRreplaceDec = re.sub(r'\d+\/(Dec)\/\d+','DATE', sRreplaceNov1)
    sRreplaceDec1 = re.sub(r'\d+\/(DEC)\/\d+','DATE', sRreplaceDec)

    sRreplaceJanR = re.sub(r'\d\/(Jan)\/\d+','DATE', sRreplaceDec1)
    sRreplaceJan1R = re.sub(r'\d\/(JAN)\/\d+','DATE', sRreplaceJanR)
    sRreplaceFebR = re.sub(r'\d\/(Feb)\/\d+','DATE', sRreplaceJan1R)
    sRreplaceFeb1R = re.sub(r'\d\/(FEB)\/\d+','DATE', sRreplaceFebR)
    sRreplaceMarR = re.sub(r'\d\/(Mar)\/\d+','DATE', sRreplaceFeb1R)
    sRreplaceMar1R = re.sub(r'\d\/(MAR)\/\d+','DATE', sRreplaceMarR)
    sRreplaceMar2R = re.sub(r'\d\/(March)\/\d+','DATE', sRreplaceMar1R)
    sRreplaceMar3R = re.sub(r'\d\/(MARCH)\/\d+','DATE', sRreplaceMar2R)
    sRreplaceAprR = re.sub(r'\d\/(Apr)\/\d+','DATE', sRreplaceMar3R)
    sRreplaceApr1R = re.sub(r'\d\/(APR)\/\d+','DATE', sRreplaceAprR)
    sRreplaceApr2R = re.sub(r'\d\/(April)\/\d+','DATE', sRreplaceApr1R)
    sRreplaceApr3R = re.sub(r'\d\/(APRIL)\/\d+','DATE', sRreplaceApr2R)
    sRreplaceMayR = re.sub(r'\d\/(May)\/\d+','DATE', sRreplaceApr3R)
    sRreplaceMay1R = re.sub(r'\d\/(MAY)\/\d+','DATE', sRreplaceMayR)
    sRreplaceJuneR = re.sub(r'\d\/(Jun)\/\d+','DATE', sRreplaceMay1R)
    sRreplaceJune1R = re.sub(r'\d\/(JUN)\/\d+','DATE', sRreplaceJuneR)
    sRreplaceJune2R = re.sub(r'\d\/(June)\/\d+','DATE', sRreplaceJune1R)
    sRreplaceJune3R = re.sub(r'\d\/(JUNE)\/\d+','DATE', sRreplaceJune2R)
    sRreplaceJulyR = re.sub(r'\d\/(July)\/\d+','DATE', sRreplaceJune3R)
    sRreplaceJuly1R = re.sub(r'\d\/(JULY)\/\d+','DATE', sRreplaceJulyR)
    sRreplaceAugR = re.sub(r'\d\/(Aug)\/\d+','DATE', sRreplaceJuly1R)
    sRreplaceAug1R = re.sub(r'\d\/(AUG)\/\d+','DATE', sRreplaceAugR)
    sRreplaceSeptR = re.sub(r'\d\/(Sept)\/\d+','DATE', sRreplaceAug1R)
    sRreplaceSept1R = re.sub(r'\d\/(SEPT)\/\d+','DATE', sRreplaceSeptR)
    sRreplaceOctR = re.sub(r'\d\/(Oct)\/\d+','DATE', sRreplaceSept1R)
    sRreplaceOct1R = re.sub(r'\d\/(OCT)\/\d+','DATE', sRreplaceOctR)
    sRreplaceNovR = re.sub(r'\d\/(Nov)\/\d+','DATE', sRreplaceOct1R)
    sRreplaceNov1R = re.sub(r'\d\/(NOV)\/\d+','DATE', sRreplaceNovR)
    sRreplaceDecR = re.sub(r'\d\/(Dec)\/\d+','DATE', sRreplaceNov1R)
    sRreplaceDec1R = re.sub(r'\d\/(DEC)\/\d+','DATE', sRreplaceDecR)


    ######
    sRreplaceJanA = re.sub(r'\d+\/(January)\/\d+','DATE', sRreplaceDec1R)
    sRreplaceJan1A = re.sub(r'\d+\/(JANUARY)\/\d+','DATE', sRreplaceJanA)
    sRreplaceFebA = re.sub(r'\d+\/(February)\/\d+','DATE', sRreplaceJan1A)
    sRreplaceFeb1A = re.sub(r'\d+\/(FEBRUARY)\/\d+','DATE', sRreplaceFebA)
    sRreplaceMarA = re.sub(r'\d+\/(March)\/\d+','DATE', sRreplaceFeb1A)
    sRreplaceMar1A = re.sub(r'\d+\/(MARCH)\/\d+','DATE', sRreplaceMarA)
    sRreplaceMar2A = re.sub(r'\d+\/(March)\/\d+','DATE', sRreplaceMar1A)
    sRreplaceMar3A = re.sub(r'\d+\/(MARCH)\/\d+','DATE', sRreplaceMar2A)
    sRreplaceAprA = re.sub(r'\d+\/(April)\/\d+','DATE', sRreplaceMar3A)
    sRreplaceApr1A = re.sub(r'\d+\/(APRIL)\/\d+','DATE', sRreplaceAprA)
    sRreplaceApr2A = re.sub(r'\d+\/(April)\/\d+','DATE', sRreplaceApr1A)
    sRreplaceApr3A = re.sub(r'\d+\/(APRIL)\/\d+','DATE', sRreplaceApr2A)
    sRreplaceMayA = re.sub(r'\d+\/(May)\/\d+','DATE', sRreplaceApr3A)
    sRreplaceMay1A = re.sub(r'\d+\/(MAY)\/\d+','DATE', sRreplaceMayA)
    sRreplaceJuneA = re.sub(r'\d+\/(June)\/\d+','DATE', sRreplaceMay1A)
    sRreplaceJune1A = re.sub(r'\d+\/(JUNE)\/\d+','DATE', sRreplaceJuneA)
    sRreplaceJune2A = re.sub(r'\d+\/(June)\/\d+','DATE', sRreplaceJune1A)
    sRreplaceJune3A = re.sub(r'\d+\/(JUNE)\/\d+','DATE', sRreplaceJune2A)
    sRreplaceJulyA = re.sub(r'\d+\/(July)\/\d+','DATE', sRreplaceJune3A)
    sRreplaceJuly1A = re.sub(r'\d+\/(JULY)\/\d+','DATE', sRreplaceJulyA)
    sRreplaceAugA = re.sub(r'\d+\/(August)\/\d+','DATE', sRreplaceJuly1A)
    sRreplaceAug1A = re.sub(r'\d+\/(AUGUST)\/\d+','DATE', sRreplaceAugA)
    sRreplaceSeptA = re.sub(r'\d+\/(September)\/\d+','DATE', sRreplaceAug1A)
    sRreplaceSept1A = re.sub(r'\d+\/(SEPTEMBER)\/\d+','DATE', sRreplaceSeptA)
    sRreplaceOctA = re.sub(r'\d+\/(October)\/\d+','DATE', sRreplaceSept1A)
    sRreplaceOct1A = re.sub(r'\d+\/(OCTOBER)\/\d+','DATE', sRreplaceOctA)
    sRreplaceNovA = re.sub(r'\d+\/(November)\/\d+','DATE', sRreplaceOct1A)
    sRreplaceNov1A = re.sub(r'\d+\/(NOVEMBER)\/\d+','DATE', sRreplaceNovA)
    sRreplaceDecA = re.sub(r'\d+\/(December)\/\d+','DATE', sRreplaceNov1A)
    sRreplaceDec1A = re.sub(r'\d+\/(DECEMBER)\/\d+','DATE', sRreplaceDecA)

    sRreplaceJanRB = re.sub(r'\d\/(January)\/\d+','DATE', sRreplaceDec1A)
    sRreplaceJan1RB = re.sub(r'\d\/(JANUARY)\/\d+','DATE', sRreplaceJanRB)
    sRreplaceFebRB = re.sub(r'\d\/(February)\/\d+','DATE', sRreplaceJan1RB)
    sRreplaceFeb1RB = re.sub(r'\d\/(FEBRUARY)\/\d+','DATE', sRreplaceFebRB)
    sRreplaceMarRB = re.sub(r'\d\/(March)\/\d+','DATE', sRreplaceFeb1RB)
    sRreplaceMar1RB = re.sub(r'\d\/(MARCH)\/\d+','DATE', sRreplaceMarRB)
    sRreplaceMar2RB = re.sub(r'\d\/(March)\/\d+','DATE', sRreplaceMar1RB)
    sRreplaceMar3RB = re.sub(r'\d\/(MARCH)\/\d+','DATE', sRreplaceMar2RB)
    sRreplaceAprRB = re.sub(r'\d\/(April)\/\d+','DATE', sRreplaceMar3RB)
    sRreplaceApr1RB = re.sub(r'\d\/(APR)\/\d+','DATE', sRreplaceAprRB)
    sRreplaceApr2RB = re.sub(r'\d\/(April)\/\d+','DATE', sRreplaceApr1RB)
    sRreplaceApr3RB = re.sub(r'\d\/(APRIL)\/\d+','DATE', sRreplaceApr2RB)
    sRreplaceMayRB = re.sub(r'\d\/(May)\/\d+','DATE', sRreplaceApr3RB)
    sRreplaceMay1RB = re.sub(r'\d\/(MAY)\/\d+','DATE', sRreplaceMayRB)
    sRreplaceJuneRB = re.sub(r'\d\/(June)\/\d+','DATE', sRreplaceMay1RB)
    sRreplaceJune1RB = re.sub(r'\d\/(JUNE)\/\d+','DATE', sRreplaceJuneRB)
    sRreplaceJune2RB = re.sub(r'\d\/(June)\/\d+','DATE', sRreplaceJune1RB)
    sRreplaceJune3RB = re.sub(r'\d\/(JUNE)\/\d+','DATE', sRreplaceJune2RB)
    sRreplaceJulyRB = re.sub(r'\d\/(July)\/\d+','DATE', sRreplaceJune3RB)
    sRreplaceJuly1RB = re.sub(r'\d\/(JULY)\/\d+','DATE', sRreplaceJulyRB)
    sRreplaceAugRB = re.sub(r'\d\/(August)\/\d+','DATE', sRreplaceJuly1RB)
    sRreplaceAug1RB = re.sub(r'\d\/(AUGUST)\/\d+','DATE', sRreplaceAugRB)
    sRreplaceSeptRB = re.sub(r'\d\/(September)\/\d+','DATE', sRreplaceAug1RB)
    sRreplaceSept1RB = re.sub(r'\d\/(SEPTEMBER)\/\d+','DATE', sRreplaceSeptRB)
    sRreplaceOctRB = re.sub(r'\d\/(October)\/\d+','DATE', sRreplaceSept1RB)
    sRreplaceOct1RB = re.sub(r'\d\/(OCTOBER)\/\d+','DATE', sRreplaceOctRB)
    sRreplaceNovRB = re.sub(r'\d\/(November)\/\d+','DATE', sRreplaceOct1RB)
    sRreplaceNov1RB = re.sub(r'\d\/(NOVEMBER)\/\d+','DATE', sRreplaceNovRB)
    sRreplaceDecRB = re.sub(r'\d\/(December)\/\d+','DATE', sRreplaceNov1RB)
    sRreplaceDec1RB = re.sub(r'\d\/(DECEMBER)\/\d+','DATE', sRreplaceDecRB)

    sRreplaceJanRQ = re.sub(r'(Jan)\/\d+','DATE', sRreplaceDec1RB)
    sRreplaceJan1RQ = re.sub(r'(JAN)\/\d+','DATE', sRreplaceJanRQ)
    sRreplaceFebRQ = re.sub(r'(Feb)\/\d+','DATE', sRreplaceJan1RQ)
    sRreplaceFeb1RQ = re.sub(r'(FEB)\/\d+','DATE', sRreplaceFebRQ)
    sRreplaceMarRQ = re.sub(r'(Mar)\/\d+','DATE', sRreplaceFeb1RQ)
    sRreplaceMar1RQ = re.sub(r'(MAR)\/\d+','DATE', sRreplaceMarRQ)
    sRreplaceMar2RQ = re.sub(r'(March)\/\d+','DATE', sRreplaceMar1RQ)
    sRreplaceMar3RQ = re.sub(r'(MARCH)\/\d+','DATE', sRreplaceMar2RQ)
    sRreplaceAprRQ = re.sub(r'(Apr)\/\d+','DATE', sRreplaceMar3RQ)
    sRreplaceApr1RQ = re.sub(r'(APR)\/\d+','DATE', sRreplaceAprRQ)
    sRreplaceApr2RQ = re.sub(r'(April)\/\d+','DATE', sRreplaceApr1RQ)
    sRreplaceApr3RQ = re.sub(r'(APRIL)\/\d+','DATE', sRreplaceApr2RQ)
    sRreplaceMayRQ = re.sub(r'(May)\/\d+','DATE', sRreplaceApr3RQ)
    sRreplaceMay1RQ = re.sub(r'(MAY)\/\d+','DATE', sRreplaceMayRQ)
    sRreplaceJuneRQ = re.sub(r'(Jun)\/\d+','DATE', sRreplaceMay1RQ)
    sRreplaceJune1RQ = re.sub(r'(JUN)\/\d+','DATE', sRreplaceJuneRQ)
    sRreplaceJune2RQ = re.sub(r'(June)\/\d+','DATE', sRreplaceJune1RQ)
    sRreplaceJune3RQ = re.sub(r'(JUNE)\/\d+','DATE', sRreplaceJune2RQ)
    sRreplaceJulyRQ = re.sub(r'(July)\/\d+','DATE', sRreplaceJune3RQ)
    sRreplaceJuly1RQ = re.sub(r'(JULY)\/\d+','DATE', sRreplaceJulyRQ)
    sRreplaceAugRQ = re.sub(r'(Aug)\/\d+','DATE', sRreplaceJuly1RQ)
    sRreplaceAug1RQ = re.sub(r'(AUG)\/\d+','DATE', sRreplaceAugRQ)
    sRreplaceSeptRQ = re.sub(r'(Sept)\/\d+','DATE', sRreplaceAug1RQ)
    sRreplaceSept1RQ = re.sub(r'(SEPT)\/\d+','DATE', sRreplaceSeptRQ)
    sRreplaceOctRQ = re.sub(r'(Oct)\/\d+','DATE', sRreplaceSept1RQ)
    sRreplaceOct1RQ = re.sub(r'(OCT)\/\d+','DATE', sRreplaceOctRQ)
    sRreplaceNovRQ = re.sub(r'(Nov)\/\d+','DATE', sRreplaceOct1RQ)
    sRreplaceNov1RQ = re.sub(r'(NOV)\/\d+','DATE', sRreplaceNovRQ)
    sRreplaceDecRQ = re.sub(r'(Dec)\/\d+','DATE', sRreplaceNov1RQ)
    sRreplaceDec1RQ = re.sub(r'(DEC)\/\d+','DATE', sRreplaceDecRQ)

    sRreplaceJanAK = re.sub(r'(January)\/\d+','DATE', sRreplaceDec1RQ)
    sRreplaceJan1AK = re.sub(r'(JANUARY)\/\d+','DATE', sRreplaceJanAK)
    sRreplaceFebAK = re.sub(r'(February)\/\d+','DATE', sRreplaceJan1AK)
    sRreplaceFeb1AK = re.sub(r'(FEBRUARY)\/\d+','DATE', sRreplaceFebAK)
    sRreplaceMarAK = re.sub(r'(March)\/\d+','DATE', sRreplaceFeb1AK)
    sRreplaceMar1AK = re.sub(r'(MARCH)\/\d+','DATE', sRreplaceMarAK)
    sRreplaceMar2AK = re.sub(r'(March)\/\d+','DATE', sRreplaceMar1AK)
    sRreplaceMar3AK = re.sub(r'(MARCH)\/\d+','DATE', sRreplaceMar2AK)
    sRreplaceAprAK = re.sub(r'(April)\/\d+','DATE', sRreplaceMar3AK)
    sRreplaceApr1AK = re.sub(r'(APRIL)\/\d+','DATE', sRreplaceAprAK)
    sRreplaceApr2AK = re.sub(r'(April)\/\d+','DATE', sRreplaceApr1AK)
    sRreplaceApr3AK = re.sub(r'(APRIL)\/\d+','DATE', sRreplaceApr2AK)
    sRreplaceMayAK = re.sub(r'(May)\/\d+','DATE', sRreplaceApr3AK)
    sRreplaceMay1AK = re.sub(r'(MAY)\/\d+','DATE', sRreplaceMayAK)
    sRreplaceJuneAK = re.sub(r'(June)\/\d+','DATE', sRreplaceMay1AK)
    sRreplaceJune1AK = re.sub(r'(JUNE)\/\d+','DATE', sRreplaceJuneAK)
    sRreplaceJune2AK = re.sub(r'(June)\/\d+','DATE', sRreplaceJune1AK)
    sRreplaceJune3AK = re.sub(r'(JUNE)\/\d+','DATE', sRreplaceJune2AK)
    sRreplaceJulyAK = re.sub(r'(July)\/\d+','DATE', sRreplaceJune3AK)
    sRreplaceJuly1AK = re.sub(r'(JULY)\/\d+','DATE', sRreplaceJulyAK)
    sRreplaceAugAK = re.sub(r'(August)\/\d+','DATE', sRreplaceJuly1AK)
    sRreplaceAug1AK = re.sub(r'(AUGUST)\/\d+','DATE', sRreplaceAugAK)
    sRreplaceSeptAK = re.sub(r'(September)\/\d+','DATE', sRreplaceAug1AK)
    sRreplaceSept1AK = re.sub(r'(SEPTEMBER)\/\d+','DATE', sRreplaceSeptAK)
    sRreplaceOctAK = re.sub(r'(October)\/\d+','DATE', sRreplaceSept1AK)
    sRreplaceOct1AK = re.sub(r'(OCTOBER)\/\d+','DATE', sRreplaceOctAK)
    sRreplaceNovAK = re.sub(r'(November)\/\d+','DATE', sRreplaceOct1AK)
    sRreplaceNov1AK = re.sub(r'(NOVEMBER)\/\d+','DATE', sRreplaceNovAK)
    sRreplaceDecAK = re.sub(r'(December)\/\d+','DATE', sRreplaceNov1AK)
    sRreplaceDec1AK = re.sub(r'(DECEMBER)\/\d+','DATE', sRreplaceDecAK)

    ##

    jRreplaceJanRQ = re.sub(r'(Jan)\s+\d+','DATE DATE', sRreplaceDec1AK)
    jRreplaceJan1RQ = re.sub(r'(JAN)\s+\d+','DATE DATE', jRreplaceJanRQ)
    jRreplaceFebRQ = re.sub(r'(Feb)\s+\d+','DATE DATE', jRreplaceJan1RQ)
    jRreplaceFeb1RQ = re.sub(r'(FEB)\s+\d+','DATE DATE', jRreplaceFebRQ)
    jRreplaceMarRQ = re.sub(r'(Mar)\s+\d+','DATE DATE', jRreplaceFeb1RQ)
    jRreplaceMar1RQ = re.sub(r'(MAR)\s+\d+','DATE DATE', jRreplaceMarRQ)
    jRreplaceMar2RQ = re.sub(r'(March)\s+\d+','DATE DATE', jRreplaceMar1RQ)
    jRreplaceMar3RQ = re.sub(r'(MARCH)\s+\d+','DATE DATE', jRreplaceMar2RQ)
    jRreplaceAprRQ = re.sub(r'(Apr)\s+\d+','DATE DATE', jRreplaceMar3RQ)
    jRreplaceApr1RQ = re.sub(r'(APR)\s+\d+','DATE DATE', jRreplaceAprRQ)
    jRreplaceApr2RQ = re.sub(r'(April)\s+\d+','DATE DATE', jRreplaceApr1RQ)
    jRreplaceApr3RQ = re.sub(r'(APRIL)\s+\d+','DATE DATE', jRreplaceApr2RQ)
    jRreplaceMayRQ = re.sub(r'(May)\s+\d+','DATE DATE', jRreplaceApr3RQ)
    jRreplaceMay1RQ = re.sub(r'(MAY)\s+\d+','DATE DATE', jRreplaceMayRQ)
    jRreplaceJuneRQ = re.sub(r'(Jun)\s+\d+','DATE DATE', jRreplaceMay1RQ)
    jRreplaceJune1RQ = re.sub(r'(JUN)\s+\d+','DATE DATE', jRreplaceJuneRQ)
    jRreplaceJune2RQ = re.sub(r'(June)\s+\d+','DATE DATE', jRreplaceJune1RQ)
    jRreplaceJune3RQ = re.sub(r'(JUNE)\s+\d+','DATE DATE', jRreplaceJune2RQ)
    jRreplaceJulyRQ = re.sub(r'(July)\s+\d+','DATE DATE', jRreplaceJune3RQ)
    jRreplaceJuly1RQ = re.sub(r'(JULY)\s+\d+','DATE DATE', jRreplaceJulyRQ)
    jRreplaceAugRQ = re.sub(r'(Aug)\s+\d+','DATE DATE', jRreplaceJuly1RQ)
    jRreplaceAug1RQ = re.sub(r'(AUG)\s+\d+','DATE DATE', jRreplaceAugRQ)
    jRreplaceSeptRQ = re.sub(r'(Sept)\s+\d+','DATE DATE', jRreplaceAug1RQ)
    jRreplaceSept1RQ = re.sub(r'(SEPT)\s+\d+','DATE DATE', jRreplaceSeptRQ)
    jRreplaceOctRQ = re.sub(r'(Oct)\s+\d+','DATE DATE', jRreplaceSept1RQ)
    jRreplaceOct1RQ = re.sub(r'(OCT)\s+\d+','DATE DATE', jRreplaceOctRQ)
    jRreplaceNovRQ = re.sub(r'(Nov)\s+\d+','DATE DATE', jRreplaceOct1RQ)
    jRreplaceNov1RQ = re.sub(r'(NOV)\s+\d+','DATE DATE', jRreplaceNovRQ)
    jRreplaceDecRQ = re.sub(r'(Dec)\s+\d+','DATE DATE', jRreplaceNov1RQ)
    jRreplaceDec1RQ = re.sub(r'(DEC)\s+\d+','DATE DATE', jRreplaceDecRQ)

    jRreplaceJanAK = re.sub(r'(January)\s+\d+','DATE DATE', jRreplaceDec1RQ)
    jRreplaceJan1AK = re.sub(r'(JANUARY)\s+\d+','DATE DATE', jRreplaceJanAK)
    jRreplaceFebAK = re.sub(r'(February)\s+\d+','DATE DATE', jRreplaceJan1AK)
    jRreplaceFeb1AK = re.sub(r'(FEBRUARY)\s+\d+','DATE DATE', jRreplaceFebAK)
    jRreplaceMarAK = re.sub(r'(March)\s+\d+','DATE DATE', jRreplaceFeb1AK)
    jRreplaceMar1AK = re.sub(r'(MARCH)\s+\d+','DATE DATE', jRreplaceMarAK)
    jRreplaceMar2AK = re.sub(r'(March)\s+\d+','DATE DATE', jRreplaceMar1AK)
    jRreplaceMar3AK = re.sub(r'(MARCH)\s+\d+','DATE DATE', jRreplaceMar2AK)
    jRreplaceAprAK = re.sub(r'(April)\s+\d+','DATE DATE', jRreplaceMar3AK)
    jRreplaceApr1AK = re.sub(r'(APRIL)\s+\d+','DATE DATE', jRreplaceAprAK)
    jRreplaceApr2AK = re.sub(r'(April)\s+\d+','DATE DATE', jRreplaceApr1AK)
    jRreplaceApr3AK = re.sub(r'(APRIL)\s+\d+','DATE DATE', jRreplaceApr2AK)
    jRreplaceMayAK = re.sub(r'(May)\s+\d+','DATE DATE', jRreplaceApr3AK)
    jRreplaceMay1AK = re.sub(r'(MAY)\s+\d+','DATE DATE', jRreplaceMayAK)
    jRreplaceJuneAK = re.sub(r'(June)\s+\d+','DATE DATE', jRreplaceMay1AK)
    jRreplaceJune1AK = re.sub(r'(JUNE)\s+\d+','DATE DATE', jRreplaceJuneAK)
    jRreplaceJune2AK = re.sub(r'(June)\s+\d+','DATE DATE', jRreplaceJune1AK)
    jRreplaceJune3AK = re.sub(r'(JUNE)\s+\d+','DATE DATE', jRreplaceJune2AK)
    jRreplaceJulyAK = re.sub(r'(July)\s+\d+','DATE DATE', jRreplaceJune3AK)
    jRreplaceJuly1AK = re.sub(r'(JULY)\s+\d+','DATE DATE', jRreplaceJulyAK)
    jRreplaceAugAK = re.sub(r'(August)\s+\d+','DATE DATE', jRreplaceJuly1AK)
    jRreplaceAug1AK = re.sub(r'(AUGUST)\s+\d+','DATE DATE', jRreplaceAugAK)
    jRreplaceSeptAK = re.sub(r'(September)\s+\d+','DATE DATE', jRreplaceAug1AK)
    jRreplaceSept1AK = re.sub(r'(SEPTEMBER)\s+\d+','DATE DATE', jRreplaceSeptAK)
    jRreplaceOctAK = re.sub(r'(October)\s+\d+','DATE DATE', jRreplaceSept1AK)
    jRreplaceOct1AK = re.sub(r'(OCTOBER)\s+\d+','DATE DATE', jRreplaceOctAK)
    jRreplaceNovAK = re.sub(r'(November)\s+\d+','DATE DATE', jRreplaceOct1AK)
    jRreplaceNov1AK = re.sub(r'(NOVEMBER)\s+\d+','DATE DATE', jRreplaceNovAK)
    jRreplaceDecAK = re.sub(r'(December)\s+\d+','DATE DATE', jRreplaceNov1AK)
    jRreplaceDec1AK = re.sub(r'(DECEMBER)\s+\d+','DATE DATE', jRreplaceDecAK)

############################################################################


    djRreplaceJanRQ = re.sub(r'(Jan)\-\d+\-\d+','DATE', jRreplaceDec1AK)
    djRreplaceJan1RQ = re.sub(r'(JAN)\-\d+\-\d+','DATE', djRreplaceJanRQ)
    djRreplaceFebRQ = re.sub(r'(Feb)\-\d+\-\d+','DATE', djRreplaceJan1RQ)
    djRreplaceFeb1RQ = re.sub(r'(FEB)\-\d+\-\d+','DATE', djRreplaceFebRQ)
    djRreplaceMarRQ = re.sub(r'(Mar)\-\d+\-\d+','DATE', djRreplaceFeb1RQ)
    djRreplaceMar1RQ = re.sub(r'(MAR)\-\d+\-\d+','DATE', djRreplaceMarRQ)
    djRreplaceMar2RQ = re.sub(r'(March)\-\d+\-\d+','DATE', djRreplaceMar1RQ)
    djRreplaceMar3RQ = re.sub(r'(MARCH)\-\d+\-\d+','DATE', djRreplaceMar2RQ)
    djRreplaceAprRQ = re.sub(r'(Apr)\-\d+\-\d+','DATE', djRreplaceMar3RQ)
    djRreplaceApr1RQ = re.sub(r'(APR)\-\d+\-\d+','DATE', djRreplaceAprRQ)
    djRreplaceApr2RQ = re.sub(r'(April)\-\d+\-\d+','DATE', djRreplaceApr1RQ)
    djRreplaceApr3RQ = re.sub(r'(APRIL)\-\d+\-\d+','DATE', djRreplaceApr2RQ)
    djRreplaceMayRQ = re.sub(r'(May)\-\d+\-\d+','DATE', djRreplaceApr3RQ)
    djRreplaceMay1RQ = re.sub(r'(MAY)\-\d+\-\d+','DATE', djRreplaceMayRQ)
    djRreplaceJuneRQ = re.sub(r'(Jun)\-\d+\-\d+','DATE', djRreplaceMay1RQ)
    djRreplaceJune1RQ = re.sub(r'(JUN)\-\d+\-\d+','DATE', djRreplaceJuneRQ)
    djRreplaceJune2RQ = re.sub(r'(June)\-\d+\-\d+','DATE', djRreplaceJune1RQ)
    djRreplaceJune3RQ = re.sub(r'(JUNE)\-\d+\-\d+','DATE', djRreplaceJune2RQ)
    djRreplaceJulyRQ = re.sub(r'(July)\-\d+\-\d+','DATE', djRreplaceJune3RQ)
    djRreplaceJuly1RQ = re.sub(r'(JULY)\-\d+\-\d+','DATE', djRreplaceJulyRQ)
    djRreplaceAugRQ = re.sub(r'(Aug)\-\d+\-\d+','DATE', djRreplaceJuly1RQ)
    djRreplaceAug1RQ = re.sub(r'(AUG)\-\d+\-\d+','DATE', djRreplaceAugRQ)
    djRreplaceSeptRQ = re.sub(r'(Sept)\-\d+\-\d+','DATE', djRreplaceAug1RQ)
    djRreplaceSept1RQ = re.sub(r'(SEPT)\-\d+\-\d+','DATE', djRreplaceSeptRQ)
    djRreplaceOctRQ = re.sub(r'(Oct)\-\d+\-\d+','DATE', djRreplaceSept1RQ)
    djRreplaceOct1RQ = re.sub(r'(OCT)\-\d+\-\d+','DATE', djRreplaceOctRQ)
    djRreplaceNovRQ = re.sub(r'(Nov)\-\d+\-\d+','DATE', djRreplaceOct1RQ)
    djRreplaceNov1RQ = re.sub(r'(NOV)\-\d+\-\d+','DATE', djRreplaceNovRQ)
    djRreplaceDecRQ = re.sub(r'(Dec)\-\d+\-\d+','DATE', djRreplaceNov1RQ)
    djRreplaceDec1RQ = re.sub(r'(DEC)\-\d+\-\d+','DATE', djRreplaceDecRQ)

    djRreplaceJanAK = re.sub(r'(January)\-\d+\-\d+','DATE', djRreplaceDec1RQ)
    djRreplaceJan1AK = re.sub(r'(JANUARY)\-\d+\-\d+','DATE', djRreplaceJanAK)
    djRreplaceFebAK = re.sub(r'(February)\-\d+\-\d+','DATE', djRreplaceJan1AK)
    djRreplaceFeb1AK = re.sub(r'(FEBRUARY)\-\d+\-\d+','DATE', djRreplaceFebAK)
    djRreplaceMarAK = re.sub(r'(March)\-\d+\-\d+','DATE', djRreplaceFeb1AK)
    djRreplaceMar1AK = re.sub(r'(MARCH)\-\d+\-\d+','DATE', djRreplaceMarAK)
    djRreplaceMar2AK = re.sub(r'(March)\-\d+\-\d+','DATE', djRreplaceMar1AK)
    djRreplaceMar3AK = re.sub(r'(MARCH)\-\d+\-\d+','DATE', djRreplaceMar2AK)
    djRreplaceAprAK = re.sub(r'(April)\-\d+\-\d+','DATE', djRreplaceMar3AK)
    djRreplaceApr1AK = re.sub(r'(APRIL)\-\d+\-\d+','DATE', djRreplaceAprAK)
    djRreplaceApr2AK = re.sub(r'(April)\-\d+\-\d+','DATE', djRreplaceApr1AK)
    djRreplaceApr3AK = re.sub(r'(APRIL)\-\d+\-\d+','DATE', djRreplaceApr2AK)
    djRreplaceMayAK = re.sub(r'(May)\-\d+\-\d+','DATE', djRreplaceApr3AK)
    djRreplaceMay1AK = re.sub(r'(MAY)\-\d+\-\d+','DATE', djRreplaceMayAK)
    djRreplaceJuneAK = re.sub(r'(June)\-\d+\-\d+','DATE', djRreplaceMay1AK)
    djRreplaceJune1AK = re.sub(r'(JUNE)\-\d+\-\d+','DATE', djRreplaceJuneAK)
    djRreplaceJune2AK = re.sub(r'(June)\-\d+\-\d+','DATE', djRreplaceJune1AK)
    djRreplaceJune3AK = re.sub(r'(JUNE)\-\d+\-\d+','DATE', djRreplaceJune2AK)
    djRreplaceJulyAK = re.sub(r'(July)\-\d+\-\d+','DATE', djRreplaceJune3AK)
    djRreplaceJuly1AK = re.sub(r'(JULY)\-\d+\-\d+','DATE', djRreplaceJulyAK)
    djRreplaceAugAK = re.sub(r'(August)\-\d+\-\d+','DATE', djRreplaceJuly1AK)
    djRreplaceAug1AK = re.sub(r'(AUGUST)\-\d+\-\d+','DATE', djRreplaceAugAK)
    djRreplaceSeptAK = re.sub(r'(September)\-\d+\-\d+','DATE', djRreplaceAug1AK)
    djRreplaceSept1AK = re.sub(r'(SEPTEMBER)\-\d+\-\d+','DATE', djRreplaceSeptAK)
    djRreplaceOctAK = re.sub(r'(October)\-\d+\-\d+','DATE', djRreplaceSept1AK)
    djRreplaceOct1AK = re.sub(r'(OCTOBER)\-\d+\-\d+','DATE', djRreplaceOctAK)
    djRreplaceNovAK = re.sub(r'(November)\-\d+\-\d+','DATE', djRreplaceOct1AK)
    djRreplaceNov1AK = re.sub(r'(NOVEMBER)\-\d+\-\d+','DATE', djRreplaceNovAK)
    djRreplaceDecAK = re.sub(r'(December)\-\d+\-\d+','DATE', djRreplaceNov1AK)
    djRreplaceDec1AK = re.sub(r'(DECEMBER)\-\d+\-\d+','DATE', djRreplaceDecAK)


#############################################################################       
    replaceJan = re.sub(r'(Jan)\-\w+\-\w+','DATE', djRreplaceDec1AK)
    replaceJan1 = re.sub(r'(JAN)\-\w+\-\w+','DATE', replaceJan)
    replaceFeb = re.sub(r'(Feb)\-\w+\-\w+','DATE', replaceJan1)
    replaceFeb1 = re.sub(r'(FEB)\-\w+\-\w+','DATE', replaceFeb)
    replaceMar = re.sub(r'(Mar)\-\w+\-\w+','DATE', replaceFeb1)
    replaceMar1 = re.sub(r'(MAR)\-\w+\-\w+','DATE', replaceMar)
    replaceMar2 = re.sub(r'(March)\-\w+\-\w+','DATE', replaceMar1)
    replaceMar3 = re.sub(r'(MARCH)\-\w+\-\w+','DATE', replaceMar2)
    replaceApr = re.sub(r'(Apr)\-\w+\-\w+','DATE', replaceMar3)
    replaceApr1 = re.sub(r'(APR)\-\w+\-\w+','DATE', replaceApr)
    replaceApr2 = re.sub(r'(April)\-\w+\-\w+','DATE', replaceApr1)
    replaceApr3 = re.sub(r'(APRIL)\-\w+\-\w+','DATE', replaceApr2)
    replaceMay = re.sub(r'(May)\-\w+\-\w+','DATE', replaceApr3)
    replaceMay1 = re.sub(r'(MAY)\-\w+\-\w+','DATE', replaceMay)
    replaceJune = re.sub(r'(Jun)\-\w+\-\w+','DATE', replaceMay1)
    replaceJune1 = re.sub(r'(JUN)\-\w+\-\w+','DATE', replaceJune)
    replaceJune2 = re.sub(r'(June)\-\w+\-\w+','DATE', replaceJune1)
    replaceJune3 = re.sub(r'(JUNE)\-\w+\-\w+','DATE', replaceJune2)
    replaceJuly = re.sub(r'(July)\-\w+\-\w+','DATE', replaceJune3)
    replaceJuly1 = re.sub(r'(JULY)\-\w+\-\w+','DATE', replaceJuly)
    replaceAug = re.sub(r'(Aug)\-\w+\-\w+','DATE', replaceJuly1)
    replaceAug1 = re.sub(r'(AUG)\-\w+\-\w+','DATE', replaceAug)
    replaceSept = re.sub(r'(Sept)\-\w+\-\w+','DATE', replaceAug1)
    replaceSept1 = re.sub(r'(SEPT)\-\w+\-\w+','DATE', replaceSept)
    replaceOct = re.sub(r'(Oct)\-\w+\-\w+','DATE', replaceSept1)
    replaceOct1 = re.sub(r'(OCT)\-\w+\-\w+','DATE', replaceOct)
    replaceNov = re.sub(r'(Nov)\-\w+\-\w+','DATE', replaceOct1)
    replaceNov1 = re.sub(r'(NOV)\-\w+\-\w+','DATE', replaceNov)
    replaceDec = re.sub(r'(Dec)\-\w+\-\w+','DATE', replaceNov1)
    replaceDec1 = re.sub(r'(DEC)\-\w+\-\w+','DATE', replaceDec)

    RreplaceJan = re.sub(r'\d+\-(Jan)\-\d+','DATE', replaceDec1)
    RreplaceJan1 = re.sub(r'\d+\-(JAN)\-\d+','DATE', RreplaceJan)
    RreplaceFeb = re.sub(r'\d+\-(Feb)\-\d+','DATE', RreplaceJan1)
    RreplaceFeb1 = re.sub(r'\d+\-(FEB)\-\d+','DATE', RreplaceFeb)
    RreplaceMar = re.sub(r'\d+\-(Mar)\-\d+','DATE', RreplaceFeb1)
    RreplaceMar1 = re.sub(r'\d+\-(MAR)\-\d+','DATE', RreplaceMar)
    RreplaceMar2 = re.sub(r'\d+\-(March)\-\d+','DATE', RreplaceMar1)
    RreplaceMar3 = re.sub(r'\d+\-(MARCH)\-\d+','DATE', RreplaceMar2)
    RreplaceApr = re.sub(r'\d+\-(Apr)\-\d+','DATE', RreplaceMar3)
    RreplaceApr1 = re.sub(r'\d+\-(APR)\-\d+','DATE', RreplaceApr)
    RreplaceApr2 = re.sub(r'\d+\-(April)\-\d+','DATE', RreplaceApr1)
    RreplaceApr3 = re.sub(r'\d+\-(APRIL)\-\d+','DATE', RreplaceApr2)
    RreplaceMay = re.sub(r'\d+\-(May)\-\d+','DATE', RreplaceApr3)
    RreplaceMay1 = re.sub(r'\d+\-(MAY)\-\d+','DATE', RreplaceMay)
    RreplaceJune = re.sub(r'\d+\-(Jun)\-\d+','DATE', RreplaceMay1)
    RreplaceJune1 = re.sub(r'\d+\-(JUN)\-\d+','DATE', RreplaceJune)
    RreplaceJune2 = re.sub(r'\d+\-(June)\-\d+','DATE', RreplaceJune1)
    RreplaceJune3 = re.sub(r'\d+\-(JUNE)\-\d+','DATE', RreplaceJune2)
    RreplaceJuly = re.sub(r'\d+\-(July)\-\d+','DATE', RreplaceJune3)
    RreplaceJuly1 = re.sub(r'\d+\-(JULY)\-\d+','DATE', RreplaceJuly)
    RreplaceAug = re.sub(r'\d+\-(Aug)\-\d+','DATE', RreplaceJuly1)
    RreplaceAug1 = re.sub(r'\d+\-(AUG)\-\d+','DATE', RreplaceAug)
    RreplaceSept = re.sub(r'\d+\-(Sept)\-\d+','DATE', RreplaceAug1)
    RreplaceSept1 = re.sub(r'\d+\-(SEPT)\-\d+','DATE', RreplaceSept)
    RreplaceOct = re.sub(r'\d+\-(Oct)\-\d+','DATE', RreplaceSept1)
    RreplaceOct1 = re.sub(r'\d+\-(OCT)\-\d+','DATE', RreplaceOct)
    RreplaceNov = re.sub(r'\d+\-(Nov)\-\d+','DATE', RreplaceOct1)
    RreplaceNov1 = re.sub(r'\d+\-(NOV)\-\d+','DATE', RreplaceNov)
    RreplaceDec = re.sub(r'\d+\-(Dec)\-\d+','DATE', RreplaceNov1)
    RreplaceDec1 = re.sub(r'\d+\-(DEC)\-\d+','DATE', RreplaceDec)

    RreplaceJanR = re.sub(r'\d\-(Jan)\-\d+','DATE', RreplaceDec1)
    RreplaceJan1R = re.sub(r'\d\-(JAN)\-\d+','DATE', RreplaceJanR)
    RreplaceFebR = re.sub(r'\d\-(Feb)\-\d+','DATE', RreplaceJan1R)
    RreplaceFeb1R = re.sub(r'\d\-(FEB)\-\d+','DATE', RreplaceFebR)
    RreplaceMarR = re.sub(r'\d\-(Mar)\-\d+','DATE', RreplaceFeb1R)
    RreplaceMar1R = re.sub(r'\d\-(MAR)\-\d+','DATE', RreplaceMarR)
    RreplaceMar2R = re.sub(r'\d\-(March)\-\d+','DATE', RreplaceMar1R)
    RreplaceMar3R = re.sub(r'\d\-(MARCH)\-\d+','DATE', RreplaceMar2R)
    RreplaceAprR = re.sub(r'\d\-(Apr)\-\d+','DATE', RreplaceMar3R)
    RreplaceApr1R = re.sub(r'\d\-(APR)\-\d+','DATE', RreplaceAprR)
    RreplaceApr2R = re.sub(r'\d\-(April)\-\d+','DATE', RreplaceApr1R)
    RreplaceApr3R = re.sub(r'\d\-(APRIL)\-\d+','DATE', RreplaceApr2R)
    RreplaceMayR = re.sub(r'\d\-(May)\-\d+','DATE', RreplaceApr3R)
    RreplaceMay1R = re.sub(r'\d\-(MAY)\-\d+','DATE', RreplaceMayR)
    RreplaceJuneR = re.sub(r'\d\-(Jun)\-\d+','DATE', RreplaceMay1R)
    RreplaceJune1R = re.sub(r'\d\-(JUN)\-\d+','DATE', RreplaceJuneR)
    RreplaceJune2R = re.sub(r'\d\-(June)\-\d+','DATE', RreplaceJune1R)
    RreplaceJune3R = re.sub(r'\d\-(JUNE)\-\d+','DATE', RreplaceJune2R)
    RreplaceJulyR = re.sub(r'\d\-(July)\-\d+','DATE', RreplaceJune3R)
    RreplaceJuly1R = re.sub(r'\d\-(JULY)\-\d+','DATE', RreplaceJulyR)
    RreplaceAugR = re.sub(r'\d\-(Aug)\-\d+','DATE', RreplaceJuly1R)
    RreplaceAug1R = re.sub(r'\d\-(AUG)\-\d+','DATE', RreplaceAugR)
    RreplaceSeptR = re.sub(r'\d\-(Sept)\-\d+','DATE', RreplaceAug1R)
    RreplaceSept1R = re.sub(r'\d\-(SEPT)\-\d+','DATE', RreplaceSeptR)
    RreplaceOctR = re.sub(r'\d\-(Oct)\-\d+','DATE', RreplaceSept1R)
    RreplaceOct1R = re.sub(r'\d\-(OCT)\-\d+','DATE', RreplaceOctR)
    RreplaceNovR = re.sub(r'\d\-(Nov)\-\d+','DATE', RreplaceOct1R)
    RreplaceNov1R = re.sub(r'\d\-(NOV)\-\d+','DATE', RreplaceNovR)
    RreplaceDecR = re.sub(r'\d\-(Dec)\-\d+','DATE', RreplaceNov1R)
    RreplaceDec1R = re.sub(r'\d\-(DEC)\-\d+','DATE', RreplaceDecR)


    ######
    RreplaceJanA = re.sub(r'\d+\-(January)\-\d+','DATE', RreplaceDec1R)
    RreplaceJan1A = re.sub(r'\d+\-(JANUARY)\-\d+','DATE', RreplaceJanA)
    RreplaceFebA = re.sub(r'\d+\-(February)\-\d+','DATE', RreplaceJan1A)
    RreplaceFeb1A = re.sub(r'\d+\-(FEBRUARY)\-\d+','DATE', RreplaceFebA)
    RreplaceMarA = re.sub(r'\d+\-(March)\-\d+','DATE', RreplaceFeb1A)
    RreplaceMar1A = re.sub(r'\d+\-(MARCH)\-\d+','DATE', RreplaceMarA)
    RreplaceMar2A = re.sub(r'\d+\-(March)\-\d+','DATE', RreplaceMar1A)
    RreplaceMar3A = re.sub(r'\d+\-(MARCH)\-\d+','DATE', RreplaceMar2A)
    RreplaceAprA = re.sub(r'\d+\-(April)\-\d+','DATE', RreplaceMar3A)
    RreplaceApr1A = re.sub(r'\d+\-(APRIL)\-\d+','DATE', RreplaceAprA)
    RreplaceApr2A = re.sub(r'\d+\-(April)\-\d+','DATE', RreplaceApr1A)
    RreplaceApr3A = re.sub(r'\d+\-(APRIL)\-\d+','DATE', RreplaceApr2A)
    RreplaceMayA = re.sub(r'\d+\-(May)\-\d+','DATE', RreplaceApr3A)
    RreplaceMay1A = re.sub(r'\d+\-(MAY)\-\d+','DATE', RreplaceMayA)
    RreplaceJuneA = re.sub(r'\d+\-(June)\-\d+','DATE', RreplaceMay1A)
    RreplaceJune1A = re.sub(r'\d+\-(JUNE)\-\d+','DATE', RreplaceJuneA)
    RreplaceJune2A = re.sub(r'\d+\-(June)\-\d+','DATE', RreplaceJune1A)
    RreplaceJune3A = re.sub(r'\d+\-(JUNE)\-\d+','DATE', RreplaceJune2A)
    RreplaceJulyA = re.sub(r'\d+\-(July)\-\d+','DATE', RreplaceJune3A)
    RreplaceJuly1A = re.sub(r'\d+\-(JULY)\-\d+','DATE', RreplaceJulyA)
    RreplaceAugA = re.sub(r'\d+\-(August)\-\d+','DATE', RreplaceJuly1A)
    RreplaceAug1A = re.sub(r'\d+\-(AUGUST)\-\d+','DATE', RreplaceAugA)
    RreplaceSeptA = re.sub(r'\d+\-(September)\-\d+','DATE', RreplaceAug1A)
    RreplaceSept1A = re.sub(r'\d+\-(SEPTEMBER)\-\d+','DATE', RreplaceSeptA)
    RreplaceOctA = re.sub(r'\d+\-(October)\-\d+','DATE', RreplaceSept1A)
    RreplaceOct1A = re.sub(r'\d+\-(OCTOBER)\-\d+','DATE', RreplaceOctA)
    RreplaceNovA = re.sub(r'\d+\-(November)\-\d+','DATE', RreplaceOct1A)
    RreplaceNov1A = re.sub(r'\d+\-(NOVEMBER)\-\d+','DATE', RreplaceNovA)
    RreplaceDecA = re.sub(r'\d+\-(December)\-\d+','DATE', RreplaceNov1A)
    RreplaceDec1A = re.sub(r'\d+\-(DECEMBER)\-\d+','DATE', RreplaceDecA)

    RreplaceJanRB = re.sub(r'\d\-(January)\-\d+','DATE', RreplaceDec1A)
    RreplaceJan1RB = re.sub(r'\d\-(JANUARY)\-\d+','DATE', RreplaceJanRB)
    RreplaceFebRB = re.sub(r'\d\-(February)\-\d+','DATE', RreplaceJan1RB)
    RreplaceFeb1RB = re.sub(r'\d\-(FEBRUARY)\-\d+','DATE', RreplaceFebRB)
    RreplaceMarRB = re.sub(r'\d\-(March)\-\d+','DATE', RreplaceFeb1RB)
    RreplaceMar1RB = re.sub(r'\d\-(MARCH)\-\d+','DATE', RreplaceMarRB)
    RreplaceMar2RB = re.sub(r'\d\-(March)\-\d+','DATE', RreplaceMar1RB)
    RreplaceMar3RB = re.sub(r'\d\-(MARCH)\-\d+','DATE', RreplaceMar2RB)
    RreplaceAprRB = re.sub(r'\d\-(April)\-\d+','DATE', RreplaceMar3RB)
    RreplaceApr1RB = re.sub(r'\d\-(APR)\-\d+','DATE', RreplaceAprRB)
    RreplaceApr2RB = re.sub(r'\d\-(April)\-\d+','DATE', RreplaceApr1RB)
    RreplaceApr3RB = re.sub(r'\d\-(APRIL)\-\d+','DATE', RreplaceApr2RB)
    RreplaceMayRB = re.sub(r'\d\-(May)\-\d+','DATE', RreplaceApr3RB)
    RreplaceMay1RB = re.sub(r'\d\-(MAY)\-\d+','DATE', RreplaceMayRB)
    RreplaceJuneRB = re.sub(r'\d\-(June)\-\d+','DATE', RreplaceMay1RB)
    RreplaceJune1RB = re.sub(r'\d\-(JUNE)\-\d+','DATE', RreplaceJuneRB)
    RreplaceJune2RB = re.sub(r'\d\-(June)\-\d+','DATE', RreplaceJune1RB)
    RreplaceJune3RB = re.sub(r'\d\-(JUNE)\-\d+','DATE', RreplaceJune2RB)
    RreplaceJulyRB = re.sub(r'\d\-(July)\-\d+','DATE', RreplaceJune3RB)
    RreplaceJuly1RB = re.sub(r'\d\-(JULY)\-\d+','DATE', RreplaceJulyRB)
    RreplaceAugRB = re.sub(r'\d\-(August)\-\d+','DATE', RreplaceJuly1RB)
    RreplaceAug1RB = re.sub(r'\d\-(AUGUST)\-\d+','DATE', RreplaceAugRB)
    RreplaceSeptRB = re.sub(r'\d\-(September)\-\d+','DATE', RreplaceAug1RB)
    RreplaceSept1RB = re.sub(r'\d\-(SEPTEMBER)\-\d+','DATE', RreplaceSeptRB)
    RreplaceOctRB = re.sub(r'\d\-(October)\-\d+','DATE', RreplaceSept1RB)
    RreplaceOct1RB = re.sub(r'\d\-(OCTOBER)\-\d+','DATE', RreplaceOctRB)
    RreplaceNovRB = re.sub(r'\d\-(November)\-\d+','DATE', RreplaceOct1RB)
    RreplaceNov1RB = re.sub(r'\d\-(NOVEMBER)\-\d+','DATE', RreplaceNovRB)
    RreplaceDecRB = re.sub(r'\d\-(December)\-\d+','DATE', RreplaceNov1RB)
    RreplaceDec1RB = re.sub(r'\d\-(DECEMBER)\-\d+','DATE', RreplaceDecRB)


    ####  ####  ####

    RreplaceJanRP = re.sub(r'\d+(Jan)\d+','DATE', RreplaceDec1RB)
    RreplaceJan1RP = re.sub(r'\d+(JAN)\d+','DATE', RreplaceJanRP)
    RreplaceFebRP = re.sub(r'\d+(Feb)\d+','DATE', RreplaceJan1RP)
    RreplaceFeb1RP = re.sub(r'\d+(FEB)\d+','DATE', RreplaceFebRP)
    RreplaceMarRP = re.sub(r'\d+(Mar)\d+','DATE', RreplaceFeb1RP)
    RreplaceMar1RP = re.sub(r'\d+(MAR)\d+','DATE', RreplaceMarRP)
    RreplaceMar2RP = re.sub(r'\d+(March)\d+','DATE', RreplaceMar1RP)
    RreplaceMar3RP = re.sub(r'\d+(MARCH)\d+','DATE', RreplaceMar2RP)
    RreplaceAprRP = re.sub(r'\d+(Apr)\d+','DATE', RreplaceMar3RP)
    RreplaceApr1RP = re.sub(r'\d+(APR)\d+','DATE', RreplaceAprRP)
    RreplaceApr2RP = re.sub(r'\d+(April)\d+','DATE', RreplaceApr1RP)
    RreplaceApr3RP = re.sub(r'\d+(APRIL)\d+','DATE', RreplaceApr2RP)
    RreplaceMayRP = re.sub(r'\d+(May)\d+','DATE', RreplaceApr3RP)
    RreplaceMay1RP = re.sub(r'\d+(MAY)\d+','DATE', RreplaceMayRP)
    RreplaceJuneRP = re.sub(r'\d+(Jun)\d+','DATE', RreplaceMay1RP)
    RreplaceJune1RP = re.sub(r'\d+(JUN)\d+','DATE', RreplaceJuneRP)
    RreplaceJune2RP = re.sub(r'\d+(June)\d+','DATE', RreplaceJune1RP)
    RreplaceJune3RP = re.sub(r'\d+(JUNE)\d+','DATE', RreplaceJune2RP)
    RreplaceJulyRP = re.sub(r'\d+(July)\d+','DATE', RreplaceJune3RP)
    RreplaceJuly1RP = re.sub(r'\d+(JULY)\d+','DATE', RreplaceJulyRP)
    RreplaceAugRP = re.sub(r'\d+(Aug)\d+','DATE', RreplaceJuly1RP)
    RreplaceAug1RP = re.sub(r'\d+(AUG)\d+','DATE', RreplaceAugRP)
    RreplaceSeptRP = re.sub(r'\d+(Sept)\d+','DATE', RreplaceAug1RP)
    RreplaceSept1RP = re.sub(r'\d+(SEPT)\d+','DATE', RreplaceSeptRP)
    RreplaceOctRP = re.sub(r'\d+(Oct)\d+','DATE', RreplaceSept1RP)
    RreplaceOct1RP = re.sub(r'\d+(OCT)\d+','DATE', RreplaceOctRP)
    RreplaceNovRP = re.sub(r'\d+(Nov)\d+','DATE', RreplaceOct1RP)
    RreplaceNov1RP = re.sub(r'\d+(NOV)\d+','DATE', RreplaceNovRP)
    RreplaceDecRP = re.sub(r'\d+(Dec)\d+','DATE', RreplaceNov1RP)
    RreplaceDec1RP = re.sub(r'\d+(DEC)\d+','DATE', RreplaceDecRP)

    RreplaceJanAS = re.sub(r'\d+(January)\d+','DATE', RreplaceDec1RP)
    RreplaceJan1AS = re.sub(r'\d+(JANUARY)\d+','DATE', RreplaceJanAS)
    RreplaceFebAS = re.sub(r'\d+(February)\d+','DATE', RreplaceJan1AS)
    RreplaceFeb1AS = re.sub(r'\d+(FEBRUARY)\d+','DATE', RreplaceFebAS)
    RreplaceMarAS = re.sub(r'\d+(March)\d+','DATE', RreplaceFeb1AS)
    RreplaceMar1AS = re.sub(r'\d+(MARCH)\d+','DATE', RreplaceMarAS)
    RreplaceMar2AS = re.sub(r'\d+(March)\d+','DATE', RreplaceMar1AS)
    RreplaceMar3AS = re.sub(r'\d+(MARCH)\d+','DATE', RreplaceMar2AS)
    RreplaceAprAS = re.sub(r'\d+(April)\d+','DATE', RreplaceMar3AS)
    RreplaceApr1AS = re.sub(r'\d+(APRIL)\d+','DATE', RreplaceAprAS)
    RreplaceApr2AS = re.sub(r'\d+(April)\d+','DATE', RreplaceApr1AS)
    RreplaceApr3AS = re.sub(r'\d+(APRIL)\d+','DATE', RreplaceApr2AS)
    RreplaceMayAS = re.sub(r'\d+(May)\d+','DATE', RreplaceApr3AS)
    RreplaceMay1AS = re.sub(r'\d+(MAY)\d+','DATE', RreplaceMayAS)
    RreplaceJuneAS = re.sub(r'\d+(June)\d+','DATE', RreplaceMay1AS)
    RreplaceJune1AS = re.sub(r'\d+(JUNE)\d+','DATE', RreplaceJuneAS)
    RreplaceJune2AS = re.sub(r'\d+(June)\d+','DATE', RreplaceJune1AS)
    RreplaceJune3AS = re.sub(r'\d+(JUNE)\d+','DATE', RreplaceJune2AS)
    RreplaceJulyAS = re.sub(r'\d+(July)\d+','DATE', RreplaceJune3AS)
    RreplaceJuly1AS = re.sub(r'\d+(JULY)\d+','DATE', RreplaceJulyAS)
    RreplaceAugAS = re.sub(r'\d+(August)\d+','DATE', RreplaceJuly1AS)
    RreplaceAug1AS = re.sub(r'\d+(AUGUST)\d+','DATE', RreplaceAugAS)
    RreplaceSeptAS = re.sub(r'\d+(September)\d+','DATE', RreplaceAug1AS)
    RreplaceSept1AS = re.sub(r'\d+(SEPTEMBER)\d+','DATE', RreplaceSeptAS)
    RreplaceOctAS = re.sub(r'\d+(October)\d+','DATE', RreplaceSept1AS)
    RreplaceOct1AS = re.sub(r'\d+(OCTOBER)\d+','DATE', RreplaceOctAS)
    RreplaceNovAS = re.sub(r'\d+(November)\d+','DATE', RreplaceOct1AS)
    RreplaceNov1AS = re.sub(r'\d+(NOVEMBER)\d+','DATE', RreplaceNovAS)
    RreplaceDecAS = re.sub(r'\d+(December)\d+','DATE', RreplaceNov1AS)
    RreplaceDec1AS = re.sub(r'\d+(DECEMBER)\d+','DATE', RreplaceDecAS)


    ###  ### - 

    RreplaceJanRQ = re.sub(r'(Jan)\-\d+','DATE', RreplaceDec1AS)
    RreplaceJan1RQ = re.sub(r'(JAN)\-\d+','DATE', RreplaceJanRQ)
    RreplaceFebRQ = re.sub(r'(Feb)\-\d+','DATE', RreplaceJan1RQ)
    RreplaceFeb1RQ = re.sub(r'(FEB)\-\d+','DATE', RreplaceFebRQ)
    RreplaceMarRQ = re.sub(r'(Mar)\-\d+','DATE', RreplaceFeb1RQ)
    RreplaceMar1RQ = re.sub(r'(MAR)\-\d+','DATE', RreplaceMarRQ)
    RreplaceMar2RQ = re.sub(r'(March)\-\d+','DATE', RreplaceMar1RQ)
    RreplaceMar3RQ = re.sub(r'(MARCH)\-\d+','DATE', RreplaceMar2RQ)
    RreplaceAprRQ = re.sub(r'(Apr)\-\d+','DATE', RreplaceMar3RQ)
    RreplaceApr1RQ = re.sub(r'(APR)\-\d+','DATE', RreplaceAprRQ)
    RreplaceApr2RQ = re.sub(r'(April)\-\d+','DATE', RreplaceApr1RQ)
    RreplaceApr3RQ = re.sub(r'(APRIL)\-\d+','DATE', RreplaceApr2RQ)
    RreplaceMayRQ = re.sub(r'(May)\-\d+','DATE', RreplaceApr3RQ)
    RreplaceMay1RQ = re.sub(r'(MAY)\-\d+','DATE', RreplaceMayRQ)
    RreplaceJuneRQ = re.sub(r'(Jun)\-\d+','DATE', RreplaceMay1RQ)
    RreplaceJune1RQ = re.sub(r'(JUN)\-\d+','DATE', RreplaceJuneRQ)
    RreplaceJune2RQ = re.sub(r'(June)\-\d+','DATE', RreplaceJune1RQ)
    RreplaceJune3RQ = re.sub(r'(JUNE)\-\d+','DATE', RreplaceJune2RQ)
    RreplaceJulyRQ = re.sub(r'(July)\-\d+','DATE', RreplaceJune3RQ)
    RreplaceJuly1RQ = re.sub(r'(JULY)\-\d+','DATE', RreplaceJulyRQ)
    RreplaceAugRQ = re.sub(r'(Aug)\-\d+','DATE', RreplaceJuly1RQ)
    RreplaceAug1RQ = re.sub(r'(AUG)\-\d+','DATE', RreplaceAugRQ)
    RreplaceSeptRQ = re.sub(r'(Sept)\-\d+','DATE', RreplaceAug1RQ)
    RreplaceSept1RQ = re.sub(r'(SEPT)\-\d+','DATE', RreplaceSeptRQ)
    RreplaceOctRQ = re.sub(r'(Oct)\-\d+','DATE', RreplaceSept1RQ)
    RreplaceOct1RQ = re.sub(r'(OCT)\-\d+','DATE', RreplaceOctRQ)
    RreplaceNovRQ = re.sub(r'(Nov)\-\d+','DATE', RreplaceOct1RQ)
    RreplaceNov1RQ = re.sub(r'(NOV)\-\d+','DATE', RreplaceNovRQ)
    RreplaceDecRQ = re.sub(r'(Dec)\-\d+','DATE', RreplaceNov1RQ)
    RreplaceDec1RQ = re.sub(r'(DEC)\-\d+','DATE', RreplaceDecRQ)

    RreplaceJanAK = re.sub(r'(January)\-\d+','DATE', RreplaceDec1RQ)
    RreplaceJan1AK = re.sub(r'(JANUARY)\-\d+','DATE', RreplaceJanAK)
    RreplaceFebAK = re.sub(r'(February)\-\d+','DATE', RreplaceJan1AK)
    RreplaceFeb1AK = re.sub(r'(FEBRUARY)\-\d+','DATE', RreplaceFebAK)
    RreplaceMarAK = re.sub(r'(March)\-\d+','DATE', RreplaceFeb1AK)
    RreplaceMar1AK = re.sub(r'(MARCH)\-\d+','DATE', RreplaceMarAK)
    RreplaceMar2AK = re.sub(r'(March)\-\d+','DATE', RreplaceMar1AK)
    RreplaceMar3AK = re.sub(r'(MARCH)\-\d+','DATE', RreplaceMar2AK)
    RreplaceAprAK = re.sub(r'(April)\-\d+','DATE', RreplaceMar3AK)
    RreplaceApr1AK = re.sub(r'(APRIL)\-\d+','DATE', RreplaceAprAK)
    RreplaceApr2AK = re.sub(r'(April)\-\d+','DATE', RreplaceApr1AK)
    RreplaceApr3AK = re.sub(r'(APRIL)\-\d+','DATE', RreplaceApr2AK)
    RreplaceMayAK = re.sub(r'(May)\-\d+','DATE', RreplaceApr3AK)
    RreplaceMay1AK = re.sub(r'(MAY)\-\d+','DATE', RreplaceMayAK)
    RreplaceJuneAK = re.sub(r'(June)\-\d+','DATE', RreplaceMay1AK)
    RreplaceJune1AK = re.sub(r'(JUNE)\-\d+','DATE', RreplaceJuneAK)
    RreplaceJune2AK = re.sub(r'(June)\-\d+','DATE', RreplaceJune1AK)
    RreplaceJune3AK = re.sub(r'(JUNE)\-\d+','DATE', RreplaceJune2AK)
    RreplaceJulyAK = re.sub(r'(July)\-\d+','DATE', RreplaceJune3AK)
    RreplaceJuly1AK = re.sub(r'(JULY)\-\d+','DATE', RreplaceJulyAK)
    RreplaceAugAK = re.sub(r'(August)\-\d+','DATE', RreplaceJuly1AK)
    RreplaceAug1AK = re.sub(r'(AUGUST)\-\d+','DATE', RreplaceAugAK)
    RreplaceSeptAK = re.sub(r'(September)\-\d+','DATE', RreplaceAug1AK)
    RreplaceSept1AK = re.sub(r'(SEPTEMBER)\-\d+','DATE', RreplaceSeptAK)
    RreplaceOctAK = re.sub(r'(October)\-\d+','DATE', RreplaceSept1AK)
    RreplaceOct1AK = re.sub(r'(OCTOBER)\-\d+','DATE', RreplaceOctAK)
    RreplaceNovAK = re.sub(r'(November)\-\d+','DATE', RreplaceOct1AK)
    RreplaceNov1AK = re.sub(r'(NOVEMBER)\-\d+','DATE', RreplaceNovAK)
    RreplaceDecAK = re.sub(r'(December)\-\d+','DATE', RreplaceNov1AK)
    RreplaceDec1AK = re.sub(r'(DECEMBER)\-\d+','DATE', RreplaceDecAK)

#################################################10/20/2018

   ######
    gRreplaceJanA = re.sub(r'\d+\s+(January )','DATE DATE', RreplaceDec1AK)
    gRreplaceJan1A = re.sub(r'\d+\s+(JANUARY )','DATE DATE', gRreplaceJanA)
    gRreplaceFebA = re.sub(r'\d+\s+(February )','DATE DATE', gRreplaceJan1A)
    gRreplaceFeb1A = re.sub(r'\d+\s+(FEBRUARY )','DATE DATE', gRreplaceFebA)
    gRreplaceMarA = re.sub(r'\d+\s+(March )','DATE DATE', gRreplaceFeb1A)
    gRreplaceMar1A = re.sub(r'\d+\s+(MARCH )','DATE DATE', gRreplaceMarA)
    gRreplaceMar2A = re.sub(r'\d+\s+(March )','DATE DATE', gRreplaceMar1A)
    gRreplaceMar3A = re.sub(r'\d+\s+(MARCH )','DATE DATE', gRreplaceMar2A)
    gRreplaceAprA = re.sub(r'\d+\s+(April )','DATE DATE', gRreplaceMar3A)
    gRreplaceApr1A = re.sub(r'\d+\s+(APRIL )','DATE DATE', gRreplaceAprA)
    gRreplaceApr2A = re.sub(r'\d+\s+(April )','DATE DATE', gRreplaceApr1A)
    gRreplaceApr3A = re.sub(r'\d+\s+(APRIL )','DATE DATE', gRreplaceApr2A)
    gRreplaceMayA = re.sub(r'\d+\s+(May )','DATE DATE', gRreplaceApr3A)
    gRreplaceMay1A = re.sub(r'\d+\s+(MAY )','DATE DATE', gRreplaceMayA)
    gRreplaceJuneA = re.sub(r'\d+\s+(June )','DATE DATE', gRreplaceMay1A)
    gRreplaceJune1A = re.sub(r'\d+\s+(JUNE )','DATE DATE', gRreplaceJuneA)
    gRreplaceJune2A = re.sub(r'\d+\s+(June )','DATE DATE', gRreplaceJune1A)
    gRreplaceJune3A = re.sub(r'\d+\s+(JUNE )','DATE DATE', gRreplaceJune2A)
    gRreplaceJulyA = re.sub(r'\d+\s+(July )','DATE DATE', gRreplaceJune3A)
    gRreplaceJuly1A = re.sub(r'\d+\s+(JULY )','DATE DATE', gRreplaceJulyA)
    gRreplaceAugA = re.sub(r'\d+\s+(August )','DATE DATE', gRreplaceJuly1A)
    gRreplaceAug1A = re.sub(r'\d+\s+(AUGUST )','DATE DATE', gRreplaceAugA)
    gRreplaceSeptA = re.sub(r'\d+\s+(September )','DATE DATE', gRreplaceAug1A)
    gRreplaceSept1A = re.sub(r'\d+\s+(SEPTEMBER )','DATE DATE', gRreplaceSeptA)
    gRreplaceOctA = re.sub(r'\d+\s+(October )','DATE DATE', gRreplaceSept1A)
    gRreplaceOct1A = re.sub(r'\d+\s+(OCTOBER )','DATE DATE', gRreplaceOctA)
    gRreplaceNovA = re.sub(r'\d+\s+(November )','DATE DATE', gRreplaceOct1A)
    gRreplaceNov1A = re.sub(r'\d+\s+(NOVEMBER )','DATE DATE', gRreplaceNovA)
    gRreplaceDecA = re.sub(r'\d+\s+(December )','DATE DATE', gRreplaceNov1A)
    gRreplaceDec1A = re.sub(r'\d+\s+(DECEMBER )','DATE DATE', gRreplaceDecA)


    gRreplaceJanR = re.sub(r'\d+\s+(Jan )','DATE DATE', gRreplaceDec1A)
    gRreplaceJan1R = re.sub(r'\d+\s+(JAN )','DATE DATE', gRreplaceJanR)
    gRreplaceFebR = re.sub(r'\d+\s+(Feb )','DATE DATE', gRreplaceJan1R)
    gRreplaceFeb1R = re.sub(r'\d+\s+(FEB )','DATE DATE', gRreplaceFebR)
    gRreplaceMarR = re.sub(r'\d+\s+(Mar )','DATE DATE', gRreplaceFeb1R)
    gRreplaceMar1R = re.sub(r'\d+\s+(MAR )','DATE DATE', gRreplaceMarR)
    gRreplaceMar2R = re.sub(r'\d+\s+(March )','DATE DATE', gRreplaceMar1R)
    gRreplaceMar3R = re.sub(r'\d+\s+(MARCH )','DATE DATE', gRreplaceMar2R)
    gRreplaceAprR = re.sub(r'\d+\s+(Apr )','DATE DATE', gRreplaceMar3R)
    gRreplaceApr1R = re.sub(r'\d+\s+(APR )','DATE DATE', gRreplaceAprR)
    gRreplaceApr2R = re.sub(r'\d+\s+(April )','DATE DATE', gRreplaceApr1R)
    gRreplaceApr3R = re.sub(r'\d+\s+(APRIL )','DATE DATE', gRreplaceApr2R)
    gRreplaceMayR = re.sub(r'\d+\s+(May )','DATE DATE', gRreplaceApr3R)
    gRreplaceMay1R = re.sub(r'\d+\s+(MAY )','DATE DATE', gRreplaceMayR)
    gRreplaceJuneR = re.sub(r'\d+\s+(Jun )','DATE DATE', gRreplaceMay1R)
    gRreplaceJune1R = re.sub(r'\d+\s+(JUN )','DATE DATE', gRreplaceJuneR)
    gRreplaceJune2R = re.sub(r'\d+\s+(June )','DATE DATE', gRreplaceJune1R)
    gRreplaceJune3R = re.sub(r'\d+\s+(JUNE )','DATE DATE', gRreplaceJune2R)
    gRreplaceJulyR = re.sub(r'\d+\s+(July )','DATE DATE', gRreplaceJune3R)
    gRreplaceJuly1R = re.sub(r'\d+\s+(JULY )','DATE DATE', gRreplaceJulyR)
    gRreplaceAugR = re.sub(r'\d+\s+(Aug )','DATE DATE', gRreplaceJuly1R)
    gRreplaceAug1R = re.sub(r'\d+\s+(AUG )','DATE DATE', gRreplaceAugR)
    gRreplaceSeptR = re.sub(r'\d+\s+(Sept )','DATE DATE', gRreplaceAug1R)
    gRreplaceSept1R = re.sub(r'\d+\s+(SEPT )','DATE DATE', gRreplaceSeptR)
    gRreplaceOctR = re.sub(r'\d+\s+(Oct )','DATE DATE', gRreplaceSept1R)
    gRreplaceOct1R = re.sub(r'\d+\s+(OCT )','DATE DATE', gRreplaceOctR)
    gRreplaceNovR = re.sub(r'\d+\s+(Nov )','DATE DATE', gRreplaceOct1R)
    gRreplaceNov1R = re.sub(r'\d+\s+(NOV )','DATE DATE', gRreplaceNovR)
    gRreplaceDecR = re.sub(r'\d+\s+(Dec )','DATE DATE', gRreplaceNov1R)
    gRreplaceDec1R = re.sub(r'\d+\s+(DEC )','DATE DATE', gRreplaceDecR)



     ######
    ogRreplaceJanA = re.sub(r'(January)\-\d+','DATE', gRreplaceDec1R)
    ogRreplaceJan1A = re.sub(r'(JANUARY)\-\d+','DATE', ogRreplaceJanA)
    ogRreplaceFebA = re.sub(r'(February)\-\d+','DATE', ogRreplaceJan1A)
    ogRreplaceFeb1A = re.sub(r'(FEBRUARY)\-\d+','DATE', ogRreplaceFebA)
    ogRreplaceMarA = re.sub(r'(March)\-\d+','DATE', ogRreplaceFeb1A)
    ogRreplaceMar1A = re.sub(r'(MARCH)\-\d+','DATE', ogRreplaceMarA)
    ogRreplaceMar2A = re.sub(r'(March)\-\d+','DATE', ogRreplaceMar1A)
    ogRreplaceMar3A = re.sub(r'(MARCH)\-\d+','DATE', ogRreplaceMar2A)
    ogRreplaceAprA = re.sub(r'(April)\-\d+','DATE', ogRreplaceMar3A)
    ogRreplaceApr1A = re.sub(r'(APRIL)\-\d+','DATE', ogRreplaceAprA)
    ogRreplaceApr2A = re.sub(r'(April)\-\d+','DATE', ogRreplaceApr1A)
    ogRreplaceApr3A = re.sub(r'(APRIL)\-\d+','DATE', ogRreplaceApr2A)
    ogRreplaceMayA = re.sub(r'(May)\-\d+','DATE', ogRreplaceApr3A)
    ogRreplaceMay1A = re.sub(r'(MAY)\-\d+','DATE', ogRreplaceMayA)
    ogRreplaceJuneA = re.sub(r'(June)\-\d+','DATE', ogRreplaceMay1A)
    ogRreplaceJune1A = re.sub(r'(JUNE)\-\d+','DATE', ogRreplaceJuneA)
    ogRreplaceJune2A = re.sub(r'(June)\-\d+','DATE', ogRreplaceJune1A)
    ogRreplaceJune3A = re.sub(r'(JUNE)\-\d+','DATE', ogRreplaceJune2A)
    ogRreplaceJulyA = re.sub(r'(July)\-\d+','DATE', ogRreplaceJune3A)
    ogRreplaceJuly1A = re.sub(r'(JULY)\-\d+','DATE', ogRreplaceJulyA)
    ogRreplaceAugA = re.sub(r'(August)\-\d+','DATE', ogRreplaceJuly1A)
    ogRreplaceAug1A = re.sub(r'(AUGUST)\-\d+','DATE', ogRreplaceAugA)
    ogRreplaceSeptA = re.sub(r'(September)\-\d+','DATE', ogRreplaceAug1A)
    ogRreplaceSept1A = re.sub(r'(SEPTEMBER)\-\d+','DATE', ogRreplaceSeptA)
    ogRreplaceOctA = re.sub(r'(October)\-\d+','DATE', ogRreplaceSept1A)
    ogRreplaceOct1A = re.sub(r'(OCTOBER)\-\d+','DATE', ogRreplaceOctA)
    ogRreplaceNovA = re.sub(r'(November)\-\d+','DATE', ogRreplaceOct1A)
    ogRreplaceNov1A = re.sub(r'(NOVEMBER)\-\d+','DATE', ogRreplaceNovA)
    ogRreplaceDecA = re.sub(r'(December)\-\d+','DATE', ogRreplaceNov1A)
    ogRreplaceDec1A = re.sub(r'(DECEMBER)\-\d+','DATE', ogRreplaceDecA)



    ogRreplaceJanR = re.sub(r'(Jan)\-\d+','DATE', ogRreplaceDec1A)
    ogRreplaceJan1R = re.sub(r'(JAN)\-\d+','DATE', ogRreplaceJanR)
    ogRreplaceFebR = re.sub(r'(Feb)\-\d+','DATE', ogRreplaceJan1R)
    ogRreplaceFeb1R = re.sub(r'(FEB)\-\d+','DATE', ogRreplaceFebR)
    ogRreplaceMarR = re.sub(r'(Mar)\-\d+','DATE', ogRreplaceFeb1R)
    ogRreplaceMar1R = re.sub(r'(MAR)\-\d+','DATE', ogRreplaceMarR)
    ogRreplaceMar2R = re.sub(r'(March)\-\d+','DATE', ogRreplaceMar1R)
    ogRreplaceMar3R = re.sub(r'(MARCH)\-\d+','DATE', ogRreplaceMar2R)
    ogRreplaceAprR = re.sub(r'(Apr)\-\d+','DATE', ogRreplaceMar3R)
    ogRreplaceApr1R = re.sub(r'(APR)\-\d+','DATE', ogRreplaceAprR)
    ogRreplaceApr2R = re.sub(r'(April)\-\d+','DATE', ogRreplaceApr1R)
    ogRreplaceApr3R = re.sub(r'(APRIL)\-\d+','DATE', ogRreplaceApr2R)
    ogRreplaceMayR = re.sub(r'(May)\-\d+','DATE', ogRreplaceApr3R)
    ogRreplaceMay1R = re.sub(r'(MAY)\-\d+','DATE', ogRreplaceMayR)
    ogRreplaceJuneR = re.sub(r'(Jun)\-\d+','DATE', ogRreplaceMay1R)
    ogRreplaceJune1R = re.sub(r'(JUN)\-\d+','DATE', ogRreplaceJuneR)
    ogRreplaceJune2R = re.sub(r'(June)\-\d+','DATE', ogRreplaceJune1R)
    ogRreplaceJune3R = re.sub(r'(JUNE)\-\d+','DATE', ogRreplaceJune2R)
    ogRreplaceJulyR = re.sub(r'(July)\-\d+','DATE', ogRreplaceJune3R)
    ogRreplaceJuly1R = re.sub(r'(JULY)\-\d+','DATE', ogRreplaceJulyR)
    ogRreplaceAugR = re.sub(r'(Aug)\-\d+','DATE', ogRreplaceJuly1R)
    ogRreplaceAug1R = re.sub(r'(AUG)\-\d+','DATE', ogRreplaceAugR)
    ogRreplaceSeptR = re.sub(r'(Sept)\-\d+','DATE', ogRreplaceAug1R)
    ogRreplaceSept1R = re.sub(r'(SEPT)\-\d+','DATE', ogRreplaceSeptR)
    ogRreplaceOctR = re.sub(r'(Oct)\-\d+','DATE', ogRreplaceSept1R)
    ogRreplaceOct1R = re.sub(r'(OCT)\-\d+','DATE', ogRreplaceOctR)
    ogRreplaceNovR = re.sub(r'(Nov)\-\d+','DATE', ogRreplaceOct1R)
    ogRreplaceNov1R = re.sub(r'(NOV)\-\d+','DATE', ogRreplaceNovR)
    ogRreplaceDecR = re.sub(r'(Dec)\-\d+','DATE', ogRreplaceNov1R)
    ogRreplaceDec1R = re.sub(r'(DEC)\-\d+','DATE', ogRreplaceDecR)


#####################################################10/20/2018
    dPlusStuff = re.sub(r'DATE\%|DATE\&|DATE\$|DATE\*|DATE\^|DATE\#|DATE\@','DATE',ogRreplaceDec1R)

    datest = re.sub(r'DATEst','DATE',dPlusStuff)
    datend = re.sub(r'DATEnd','DATE',datest)
    daterd = re.sub(r'DATErd','DATE',datend)
    dateth = re.sub(r'DATEth','DATE',daterd)
    dateCommaYear = re.sub(r'DATE\,\s+\d\d\d\d','DATE DATE',dateth)

    Monday = re.sub(r'Monday\s+DATE','DATE DATE',dateCommaYear)
    Tuesday = re.sub(r'Tuesday\s+DATE','DATE DATE',Monday)
    Wednesday = re.sub(r'Wednesday\s+DATE','DATE DATE',Tuesday)
    Thursday = re.sub(r'Thursday\s+DATE','DATE DATE',Wednesday)
    Friday = re.sub(r'Friday\s+DATE','DATE DATE',Thursday)
    Saturday = re.sub(r'Saturday\s+DATE','DATE DATE',Friday)
    Sunday = re.sub(r'Sunday\s+DATE','DATE DATE',Saturday)

    monday = re.sub(r'monday\s+DATE','DATE DATE',Sunday)
    tuesday = re.sub(r'tuesday\s+DATE','DATE DATE',monday)
    wednesday = re.sub(r'wednesday\s+DATE','DATE DATE',tuesday)
    thursday = re.sub(r'thursday\s+DATE','DATE DATE',wednesday)
    friday = re.sub(r'friday\s+DATE','DATE DATE',thursday)
    saturday = re.sub(r'saturday\s+DATE','DATE DATE',friday)
    sunday = re.sub(r'sunday\s+DATE','DATE DATE',saturday)

    Mon = re.sub(r'Mon\s+DATE','DATE DATE',sunday)
    Tues = re.sub(r'Tues\s+DATE','DATE DATE',Mon)
    Tue = re.sub(r'Tue\s+DATE','DATE DATE',Tues)
    Wed = re.sub(r'Wed\s+DATE','DATE DATE',Tue)
    Thurs = re.sub(r'Thurs\s+DATE','DATE DATE',Wed)
    Thur = re.sub(r'Thur\s+DATE','DATE DATE',Thurs)
    Fri = re.sub(r'Fri\s+DATE','DATE DATE',Thur)
    Sat = re.sub(r'Sat\s+DATE','DATE DATE',Fri)
    Sun = re.sub(r'Sun\s+DATE','DATE DATE',Sat)

    mon = re.sub(r'mon\s+DATE','DATE DATE',Sun)
    tues = re.sub(r'tues\s+DATE','DATE DATE',mon)
    tue = re.sub(r'tue\s+DATE','DATE DATE',tues)
    wed = re.sub(r'wed\s+DATE','DATE DATE',tue)
    thurs = re.sub(r'thurs\s+DATE','DATE DATE',wed)
    thur = re.sub(r'thur\s+DATE','DATE DATE',thurs)
    fri = re.sub(r'fri\s+DATE','DATE DATE',thur)
    sat = re.sub(r'sat\s+DATE','DATE DATE',fri)
    sun = re.sub(r'sun\s+DATE','DATE DATE',sat)

    MON = re.sub(r'MON\s+DATE','DATE DATE',sun)
    TUES = re.sub(r'TUES\s+DATE','DATE DATE',MON)
    TUE = re.sub(r'TUE\s+DATE','DATE DATE',TUES)
    WED = re.sub(r'WED\s+DATE','DATE DATE',TUE)
    THURS = re.sub(r'THURS\s+DATE','DATE DATE',WED)
    THUR = re.sub(r'THUR\s+DATE','DATE DATE',THURS)
    FRI = re.sub(r'FRI\s+DATE','DATE DATE',THUR)
    SAT = re.sub(r'SAT\s+DATE','DATE DATE',FRI)
    SUN = re.sub(r'SUN\s+DATE','DATE DATE',SAT)



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

    replaceNumberMap1 = re.sub(r'\d+\.\)', lambda x: numberMap1.get(x.group(),x.group(0)),SUN)

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


    numberExtra = re.sub(r'\%NUM\%|\^NUM\^|\*NUM\*|\+NUM\+|NUM\-NUM|\=NUM\=|\#NUM\#','NUM',replaceRemapNumberMap419)

    numberExtraA = re.sub(r"\/NUM\/|\~NUM\~|\`NUM\`|\"NUM\"|\'NUM\'",'NUM',numberExtra)

    numberExtra1 = re.sub(r"NUM\%|NUM\^|NUM\*|NUM\+|NUM\=|NUM\#|NUM\/|NUM\~|NUM\`|NUM\"|NUM\'",'NUM',numberExtraA)

    numberExtra2 = re.sub(r'\<NUM|\>NUM|NUMmg|NUML|NUMml|NUMml\.|NUMC\.', 'NUM',numberExtra1) 

    numberExtra2A = re.sub(r'NUMC|NUMF\.|NUMF|NUMmg\.|\%NUM|\^NUM|\*NUM|\+NUM|NUM\-NUM\-NUM|\=NUM','NUM',numberExtra2)

    numberExtra2B = re.sub(r"\#NUM|\/NUM|\~NUM|\`NUM|\"NUM|\'NUM",'NUM',numberExtra2A)

    numberExtra3A = re.sub(r'NUMPM|NUM\:NUM\:NUM|NUM\:NUM|NUMAM|NUM\:NUMPM|(NUM\.NUM)','NUM',numberExtra2B)

    numberExtra3B = re.sub(r'NUMPM|NUMAM|NUM\w+','NUM',numberExtra3A)

    numberExtra4 = re.sub(r'(NUMNUMNUM)|(NUMNUM)|(NUM-NUM)|(NUM-NUM-NUM)','NUM', numberExtra3B)    


    low = numberExtra4.lower()
                
    return(low)