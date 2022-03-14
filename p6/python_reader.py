import pthread_race_cond
import sys
import re

class C_Reader:
    def __init__(self, fileName):
        self.fileName = fileName
        with open(self.fileName) as file:
                self.file = file.read()
        self.fileLines = self.file.split("\n")
        self.result = []
        self.scopeName = ['global']

       #regex pattern to detect variable types, names and assignment values
        self.declarationPattern = re.compile(' *(int|long|pthread_t|void|char) +\**((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *(=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%)? *([^;]* *);$')
        self.variablePattern = re.compile('^ *((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *((=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%) *([^;]* *);).*$')
        self.prototypePattern = re.compile('^ *(int|long|pthread_t|void|char) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\));$')
        self.functionPattern = re.compile('^ *(int|long|pthread_t|void) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\)).*$')
        self.forPattern = re.compile('for\(.*\).*')


    #get new name maybe?
    def get_fucked_noob(self):
        for line in self.fileLines:
            #find declaration
            if re.search(self.declarationPattern, line) != None and re.search(self.prototypePattern, line) == None:
                pass
                #declaration function
            #find variable assignments
            elif re.search(self.variablePattern, line) != None:
                pass
                #assignment function
            #find function declarations
            elif re.search(self.functionPattern, line) != None and re.search(self.prototypePattern, line) == None:
                pass
                #

    def get_scopes(self, scopeText):
        print("entered a new recursion")
        counter = 0
        isInScope = False
        lines = scopeText.split('\n')
        text = ''
        funcName = ''

        for line in lines:
            #check if line is a function definition and is not a prototype
            searchResult = re.search(self.functionPattern, line)
            if searchResult != None and re.search(self.prototypePattern, line) == None and counter == 0:
                self.scopeName.append('.' + searchResult.group(3))
                isInScope = True
                funcName = searchResult.group(3)
                print("entered function", funcName)

            else:
                searchResult = re.search(self.forPattern, line)
                #checks if the line is an if else pattern
                if searchResult != None and counter == 0:
                    self.scopeName.append('.for')
                    print("scopeName: ", self.scopeName)
                    isInScope = True
                    print("entered for loop")
                else:
                    pass

            #appends text that is not the start of a scope, or end of a scope
            if isInScope == True:
                for symbol in line:
                    if symbol == '{':
                        if counter != 0:
                            text = text + symbol

                        counter += 1

                    elif symbol == '}':
                        counter -= 1
                        if counter != 0:
                            text = text + symbol

                    elif counter != 0:
                        text = text + symbol

                if counter == 0:
                    isInScope = False
                    self.get_scopes(text)
                    print("exited scope")
                print("line: ", line)
                a = self.get_variables(line, self.scopeName)

                if a != None:
                    self.result.append(a)
                text = text + '\n'

            elif len(self.scopeName) == 1:
                a = self.get_variables(line, self.scopeName)
                if a != None:
                    self.result.append(a)

        print("scopename before pop: ",self.scopeName)
        self.scopeName.pop(-1)
        print("scopename after pop: ", self.scopeName)


    def get_variables(self, line, scopeArr):
        scope = ''
        for text in scopeArr:
            scope = scope + text
            
        searchResult = re.search(self.declarationPattern, line)
        if searchResult == None:
            searchResult = re.search(self.variablePattern, line)
        
        #debugging code, can be deleted
        if searchResult != None and re.search(self.prototypePattern, searchResult.group()) == None:
            #print(f"searchResult: {searchResult.group()}")
            #print(f"searchResult 1: {searchResult.group(1)}")
            #print(f"searchResult 2: {searchResult.group(2)}")
            #print(f"searchRefile sult 3: {searchResult.group(3)}")
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
#reader.get_scopes()
#reader = Python_Reader("pthread_race_cond.py")
#reader.print_functions()
#reader.print_variables()
reader.get_scopes(reader.file)
for var in reader.result:
    print(var)
