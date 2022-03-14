import pthread_race_cond
import sys
import re

class C_Reader:
    def __init__(self, fileName):
        self.fileName = fileName
        with open(self.fileName) as file:
                self.file = file.read()
        self.fileLines = self.file.split("\n")
        print(self.fileLines)

       #regex pattern to detect variable types, names and assignment values
        self.declarationPattern = re.compile(' *(int|long|pthread_t|void|char) +\**((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *(=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%)? *([^;]* *);$')
        self.variablePattern = re.compile('^ *((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *((=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%) *([^;]* *);).*$')
        self.prototypePattern = re.compile('^ *(int|long|pthread_t|void|char) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\));$')
        self.functionPattern = re.compile('^ *(int|long|pthread_t|void) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\)).*$')


    #get new name maybe?
    def get_fucked_noob(self):
        for line in self.fileLines:
            #find declaration
            if re.search(self.declarationPattern, line) != None and re.search(self.prototypePattern, line) == None:
                #declaration function
            #find variable assignments
            elif re.search(self.variablePattern, line) != None:
                #assignment function
            #find function declarations
            elif re.search(self.functionPattern, line) != None and re.search(self.prototypePattern, line) == None:
                #

    def get_func_scope(self):
        counter = 0
        isInFunc = False
        result = []
        for line in self.fileLines:
            searchResult = re.search(self.functionPattern, line)
            #check if line is a function definition and is not a prototype
            if searchResult != None and re.search(self.prototypePattern, line) == None:
                isInFunc = True
                funcName = searchResult.group(3)
                print("entered function", funcName)
            if isInFunc == True:
                for symbol in line:
                    if symbol == '{':
                        counter += 1
                    elif symbol =='}':
                        counter -= 1
                if counter == 0:
                    isInFunc = False
                    print("exited function")
                a = self.get_variables(line, funcName)
                if a != None:
                    result.append(a)
        print(result)

    def get_scopes(self):
        scopeName = ''
        results = []
        for line in self.fileLines:
            result = self.get_variables(line, scopeName)
            if result != None:
                print(result)
                results.append(result)

    def get_variables(self, line, scope):
        searchResult = re.search(self.declarationPattern, line)
        if searchResult == None:
            searchResult = re.search(self.variablePattern, line)
        
        #debugging code, can be deleted
        if searchResult != None and re.search(self.prototypePattern, searchResult.group()) == None:
            #print(f"searchResult: {searchResult.group()}")
            #print(f"searchResult 1: {searchResult.group(1)}")
            #print(f"searchResult 2: {searchResult.group(2)}")
            #print(f"searchResult 3: {searchResult.group(3)}")
            #print(f"searchResult 4: {searchResult.group(4)}")
            #print(f"searchResult 5: {searchResult.group(5)}")
            #print(f"searchResult 6: {searchResult.group(6)}")
            #print(f"searchResult 7: {searchResult.group(7)}")
            #print(f"searchResult 8: {searchResult.group(8)}")
            pass
           
        #returns the scope name, variable name and assignment value as a 3-tuple
        if searchResult != None and re.search(self.prototypePattern, searchResult.group()) == None:
            if searchResult.group(4) == None:
                return {"scope": scope,
                        "name": searchResult.group(3),
                        "value": searchResult.group(8)} 
            else:
                return {"scope": scope, 
                    "name": searchResult.group(4), 
                    "value": searchResult.group(8)}
        else:
            return None


if len(sys.argv) == 2:
    reader = C_Reader(sys.argv[1])
else:
    reader = C_Reader("pthread_race_cond.c")
reader.get_scopes()
#reader = Python_Reader("pthread_race_cond.py")
#reader.print_functions()
#reader.print_variables()
reader.get_func_scope()
