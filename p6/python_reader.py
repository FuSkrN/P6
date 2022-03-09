import pthread_race_cond
import sys
import re

class C_Reader:
    def __init__(self, fileName):
        self.fileName = fileName
        with open(self.fileName) as file:
                self.fileLines = file.readlines()

    def get_scopes(self):
        indentationCount = 0
        scopeName = 'hej'
        r = []
        for line in self.fileLines:
            result = self.get_variables(line, scopeName)
            if result != None:
                print(result)
                r.append(result)
            for symbol in line:
                if symbol == '{':
                    indentationCount += 1
                elif symbol == '}':
                    indentationCount -= 1
        for d in r:
            pass
            #print(f"{d}\n")

    def get_variables(self, line, scope):
        #regex pattern to detect variable types, names and assignment values
        declarationPattern = re.compile(' *(int|long|pthread_t|void|char) +\*?((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *(=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%)? *([^;]* *);$')
        variablePattern = re.compile('^ *((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *((=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%) *([^;]* *);).*$')
        prototypePattern = re.compile('^ *(int|long|pthread_t|void|char) +\*?(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\));$')
        searchResult = re.search(declarationPattern, line)
        if searchResult == None:
            searchResult = re.search(variablePattern, line)
        
        #debugging code, can be deleted
        if searchResult != None and re.search(prototypePattern, searchResult.group()) == None:
            print(f"searchResult: {searchResult.group()}")
            print(f"searchResult 1: {searchResult.group(1)}")
            print(f"searchResult 2: {searchResult.group(2)}")
            print(f"searchResult 3: {searchResult.group(3)}")
            print(f"searchResult 4: {searchResult.group(4)}")
            print(f"searchResult 5: {searchResult.group(5)}")
            print(f"searchResult 6: {searchResult.group(6)}")
            print(f"searchResult 7: {searchResult.group(7)}")
            print(f"searchResult 8: {searchResult.group(8)}")

        #returns the scope name, variable name and assignment value as a 3-tuple
        if searchResult != None and re.search(prototypePattern, searchResult.group()) == None:
            return {"scope": scope, 
                    "name": searchResult.group(4), 
                    "value": searchResult.group(8)}
        else:
            return None

class Python_Reader:
    def __init__(self, fileName):
        self.fileName = fileName
        with open(self.fileName) as file:
            self.fileLines = file.readlines()
    def print_functions(self):
        indentationCount = 0
        insideFunction = False
        functionIndentation = 0
        for line in self.fileLines:
            if line != '\n':
                i = 0
                while line[i] == ' ':
                    i = i + 1
                #    if i % 4 == 0 and i > 0:
                #        print("test")
                if i % 4 == 0:
                    indentationCount = int(i/4)
                    print(f"indent count: {int(i/4)}")

                if line[i] == 'd' and line[i+1] == 'e' and line[i+2] == 'f':
                    insideFunction = True
                    functionIndentation = indentationCount
                    print("entered function")
                
                if indentationCount <= functionIndentation:
                    insideFunction = False
                    print("exitted function")

                print(line)
    def print_variables(self):
        #a = vars(self).values()
        #print(a)
        print(dir(pthread_race_cond))

#if __name__ == "__main__":
if len(sys.argv) == 2:
    reader = C_Reader(sys.argv[1])
else:
    reader = C_Reader("pthread_race_cond.c")
reader.get_scopes()
#reader = Python_Reader("pthread_race_cond.py")
#reader.print_functions()
#reader.print_variables()
