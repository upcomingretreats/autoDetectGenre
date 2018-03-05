#!/usr/bin/python3

from sys import argv
from sys import exit

def print_error(num):
    options = {
        1 : "Invalid number of arguments passed.",
        2 : "Inappropriate file type for first argument.",
        3 : "Inappropriate file type for second argument.",
        4 : "Could not successfully open JSON file.",
        5 : "Could not successfully open CSV file.",
        6 : "Lengths of JSON titles and descriptions are incorrect.",
        7 : "Could not continue program due to empty CSV file."
    }
    txt, csv = "sample_book_json.txt", "sample_genre_keyword_value.csv"

    print ("\n"+options[num]+"\n")
    print ("To successfully run this program, execute with whichever parameter order in the styles below:\n")
    print ("python3 autoDetectGenre.py", txt, csv)
    print ("./autoDetectGenre.py", csv, txt, "\n")

    exit(1)


def validate_arguments():
    if len(argv) != 3:
        print_error(1)

    csv = ".csv"
    json = "json.txt"

    if json not in argv[1] and csv not in argv[1]:
        print_error(2)
    if json not in argv[2] and csv not in argv[2]:
        print_error(3)

    if csv in argv[1] and csv in argv[2]:
        print_error(4)
    if json in argv[1] and json in argv[2]:
        print_error(5)

    if json in argv[1] and csv in argv[2]:
        return argv[1], argv[2]
    return argv[2], argv[1]

def extract_json(json):
    try:
        with open(json) as lines:
            titles, descriptions = [], []
            for line in lines:
                line = line.strip()
                if "title" in line:
                    line = line.replace("\"", "").replace(",", "")
                    start = line.find(":")
                    titles.append(line[start+1:])
                elif "description" in line:
                    start = line.find(":")
                    descriptions.append(line[start+1:])
    except IOError:
        print_error(4)
    
    return titles, descriptions

def extract_csv(csv):
    try:
        with open(csv) as lines:
            next(lines)
            dicto = {}
            for line in lines:
                line = line.split(",")
                key = line[0]
                value1 = line[1].lstrip(" ")
                value2 = int(line[2].strip())
                if key in dicto:
                    dicto[key].append([value1, value2])
                else:
                    dicto[key] = [[value1, value2]]
    except IOError:
        print_error(5)

    return dicto

class Results:
    
    def __init__(self):
        self.res = []
        self.ans = []
        self.new_title = False

    def find_occurences(self, dicto, des, title):
        tmp = []
        for k, v in dicto.items():
            for i in range(0, len(v)):
                num = des.count(v[i][0])
                while num > 0:
                    self.res.append(v[i][1])
                    num -= 1
            if self.res:
                if self.new_title:
                    tmp.append(title.lstrip(" ")+"\n")
                    self.new_title = False
                calc = sum(set(self.res)) // len(set(self.res)) * len(self.res)
                tmp.append(k+", "+str(calc)+"\n")
                self.res.clear()
        self.ans.append(tmp)
    
    def calculate(self, titles, descriptions, dicto):
        for title, description in zip(titles, descriptions):
            self.new_title = True
            self.find_occurences(dicto, description, title)
        
        self.ans.sort()
        
        for answer in self.ans:
            for i in range(0, len(answer)):
                if i < 3:
                    print (answer[i])
                else:
                    break

            print ("\n")

def main():

    json, csv = validate_arguments()
    titles, descriptions = extract_json(json)
    dicto = extract_csv(csv)

    if len(titles) != len(descriptions) or len(titles) <= 0:
        print_error(6)
    if len(dicto) <= 0:
        print_error(7)

    result = Results()
    result.calculate(titles, descriptions, dicto)
    

if __name__ == "__main__":
    main()