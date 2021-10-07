""" Script to check that every columns with floats of the csv file respect the same format """

import re

# definition of regex
REGEX_DATE = "([0-9]{1,2}/){2}[0-9]{4}"
REGEX_TIME = "([0-9]{2}:){2}[0-9]{2}"
REGEX_ELECTRICAL = "([0-9]+\.[0-9][0-9][0-9];){6}[0-9]+\.[0-9][0-9][0-9]"
REGEX_ELECTRICAL_BIG = "[0-9]{6}\.[0-9][0-9][0-9]"


f = open("household_power_consumption.txt","r")
f.readline
lines = f.readlines()

regex_expr = REGEX_DATE + ";" + REGEX_TIME + ";" + REGEX_ELECTRICAL
regex_interro = REGEX_DATE + ";" + REGEX_TIME + ";?;?;?;?;?;?;"

# To analyse final results
match = True # did everything match the expected format (regex expr)
match_interrogative = False # if a line does not match the expected format, is it because every number is replaced by '?'
match_big_number = False # Can a number have more that 6 digit before the comma?


nb_lines = 0
for line in lines:
    nb_lines += 1
    if not re.match(regex_expr, line):
        if not re.match(regex_interro, line):
            print("A line does not match the expected pattern: \n\t"+line)
            match_interrogative = True
        match = False
    if re.match(REGEX_ELECTRICAL_BIG, line):
        print("more that 6 digits:"+line)
        match_big_number = True
if not match:
    print("Final result : at least one line does not match the expected pattern")
if match_interrogative:
    print("Final result : at least one line does not match the interrogative pattern")
if match_big_number:
    print("Final result : at least one line contains a number with more than 6 digit before comma")
print("Nb lines: ",nb_lines)
