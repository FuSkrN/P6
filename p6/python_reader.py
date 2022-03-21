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
        self.variablePattern = re.compile('^\s*(([a-zA-Z0-9]+)(\[[0-9]*\])?)*() *((=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%) *([^;\n]* *);)\s*$')
        self.prototypePattern = re.compile('^ *(int|long|pthread_t|void|char) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\));$')
        self.functionPattern = re.compile('^ *(int|long|pthread_t|void) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\)).*$')
        self.forPattern = re.compile('for\(.*\).*')
        self.ifElsePattern = re.compile('^if\s*\((.*?)\)\s*((.|\n)*){(.*?)((.|\n)*)}((.|\n)*)(\s*(else|else\s+if\s*\((.*?)\))\s*{(.*?)})*$')
        self.functionCallPattern = re.compile('\s*((\-)*[_a-zA-Z][a-zA-Z0-9_\-]*)\((.*?)\)();')

    def get_scopes(self, scopeText):
        lineCounter = 0
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

            else:
                #checks if the line is a for loop
                searchResult = re.search(self.forPattern, line)
                if searchResult != None and counter == 0:
                    self.scopeName.append('.for')
                    isInScope = True
                else:
                    #checks if the lin is an if else logic statement
                    searchResult = re.search(self.ifElsePattern, line)
                    if searchResult != None and counter == 0:
                        self.scopeName.append('.ifelse')
                        isInScope = True

            #appends text that is not the start of a scope, or end of a scope, to a string
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

                #checks if the scope has ended, and if so, makes a recursive call to itself, with the internal text as input
                if counter == 0:
                    isInScope = False
                    self.get_scopes(text)

                #gets the variables from a line and appends it to the result list
                a = self.get_variables(line, self.scopeName, lineCounter)
                if a != None:
                    self.result.append(a)

                #ends each line with a newline for the next iteration of recursion
                text = text + '\n'
           
            #checks for variables within the global scope (when there's only one element in the scopeName list)
            elif len(self.scopeName) == 1:
                a = self.get_variables(line, self.scopeName, lineCounter)
                if a != None:
                    self.result.append(a)

            lineCounter += 1
        #pops the latest scopename out of the scopeName list.
        self.scopeName.pop(-1)


    def get_variables(self, line, scopeArr, lineCounter):
        #defines the scope name for later usage
        scope = ''
        for text in scopeArr:
            scope = scope + text
        
        #checks if the line contains a declaration, else search for a assignment
        searchResult = re.search(self.declarationPattern, line)
        if searchResult == None:
            searchResult = re.search(self.variablePattern, line)
            if searchResult == None:
                searchResult = re.search(self.functionCallPattern, line)
        
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
            #assignment
            if searchResult.group(3) == None:
                return {"scope": scope,
                        "name": searchResult.group(2),
                        "value": searchResult.group(7),
                        "lineCounter": lineCounter,
                        "commandType": "assignment"}
            #function
            elif searchResult.group(4) == "":
                return {"scope": scope,
                        "name": searchResult.group(1),
                        "value": searchResult.group(3),
                        "lineCounter": lineCounter,
                        "commandType": "functionCall"}
            #declarations
            else:
                return {"scope": scope, 
                        "name": searchResult.group(4), 
                        "value": searchResult.group(8),
                        "lineCounter": lineCounter,
                        "commandType": "declaration"}
        else:
            return None


#reader = C_Reader("pthread_setting_variables.c")
#reader.get_scopes(reader.file)
#for r in reader.result:
#    print(r)
#reader.print_functions()
#reader.print_variables()
