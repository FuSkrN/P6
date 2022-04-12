import sys
import re

class C_Reader:
    """Lexer and parser for a C program. Returns a list of scopes and corresponding variables."""
    def __init__(self, fileName):
        self.fileName = fileName
        self.forNameCounter = 0
        self.ifNameCounter = 0
        self.ifElseNameCounter = 0

        #Opens a filepath and reads its contents line by line, split by newline characters.
        with open(self.fileName) as file:
                self.file = file.read()
        self.fileLines = self.file.split("\n")
        self.result = []
        self.scopeName = ['global']

        #Regex pattern to detect different types of statements (assignments, declarations and functions).
        #Currently not implemented: for loops and if-else statements.
        self.declarationPattern = re.compile('\s*(int|long|pthread_t|void|char) +\**((([a-zA-Z0-9]+)(\[[0-9]*\])?)*(, ?)?)* *(=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%)? *([^;]* *);\s*$')
        self.variablePattern = re.compile('^\s*(([a-zA-Z0-9]+)(\[[0-9]*\])?)*() *((=|\+=|\+\+|\+|\*=|\*|-=|--|-|\\=|\\|\%=|\%) *([^;\n]* *);)\s*$')
        self.prototypePattern = re.compile('^\s*(int|long|pthread_t|void|char) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\));$')
        self.functionPattern = re.compile('^\s*(int|long|pthread_t|void) +\**(([a-zA-Z0-9]+)\(([a-zA-Z0-9]* *\*?,?)*\)).*$')
        self.forPattern = re.compile('for\(.*\).*')
        self.ifElsePattern = re.compile('^if\s*\((.*?)\)\s*((.|\n)*){(.*?)((.|\n)*)}((.|\n)*)(\s*(else|else\s+if\s*\((.*?)\))\s*{(.*?)})*$')
        self.functionCallPattern = re.compile('\s*((\-)*[_a-zA-Z][a-zA-Z0-9_\-]*)\((.*?)\)();')

    def get_scopes(self, scopeText):
        """A function that extracts the contents of a scope. 
        A recursive call is then made in order to continually find scopes."""
        
        #Keep track of line counters and scope recursion levels.
        lineCounter = 0
        counter = 0

        #Flag indicating whether a scope is active or not.
        isInScope = False
        lines = scopeText.split('\n')
        text = ''
        funcName = ''
        for line in lines:
            #Check if line is a function definition and is not a prototype.
            searchResult = re.search(self.functionPattern, line)

            #If the function search result is not empty (no function) and there is no prototype available (along with 0 recursion).
            if searchResult != None and re.search(self.prototypePattern, line) == None and counter == 0:

                #A new scope is found, so append it to the scopeName (function name).
                self.scopeName.append('.' + searchResult.group(3))
                isInScope = True
                funcName = searchResult.group(3)

            else:
                #Checks if the line is a for loop.
                searchResult = re.search(self.forPattern, line)

                if searchResult != None and counter == 0:
                    self.scopeName.append('.for')
                    isInScope = True
                else:
                    #Checks if the line is a if-else logic statement.
                    searchResult = re.search(self.ifElsePattern, line)

                    if searchResult != None and counter == 0:
                        self.scopeName.append('.ifelse')
                        isInScope = True
            
            #Appends text that is not the start of a scope, or end of a scope, to a string.
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

                #Checks if the scope has ended, and if so, makes a recursive call to itself, with the internal text as input.
                #Enters a new scope level upon recursive call.
                if counter == 0:
                    isInScope = False
                    self.get_scopes(text)
                    text = ""

                #Gets the variables from a line and appends it to the result list.
                a = self.get_variables(line, self.scopeName, lineCounter)
                if a != None and counter == 0:
                    self.result.append(a)
                    lineCounter += 1

                #Ends each line with a newline for the next iteration of recursion, as each line is separated as such.
                text = text + '\n'
           
            #Checks for variables within the global scope (when there's only one element in the scopeName list)
            elif counter == 0:
                a = self.get_variables(line, self.scopeName, lineCounter)
                if a != None:
                    self.result.append(a)
                    lineCounter += 1

        #Pops the latest scopename out of the scopeName list.
        #A new recursive call is then made to the previous scope level.
        self.scopeName.pop(-1)

    def get_variables(self, line, scopeArr, lineCounter):
        """Gets the variables from reading input"""
        
        #Defines the scope name for later usage.
        scope = ''

        #Stores the scope of a variable in a string to be used in the creation of variable dictionaries.
        for text in scopeArr:
            scope = scope + text
        
        #Checks if the line contains a declaration, else search for a assignment.
        searchResult = re.search(self.declarationPattern, line)
        if searchResult == None:
            searchResult = re.search(self.variablePattern, line)
            if searchResult == None:
                searchResult = re.search(self.functionCallPattern, line)
        
        #Debugging code, can be deleted.
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

        #Returns the scope name, variable name and assignment value as a dictionary.
        if searchResult != None and re.search(self.prototypePattern, searchResult.group()) == None:

            #Assignment:
            if searchResult.group(3) == None:
                return {"scope": scope,
                        "name": searchResult.group(2),
                        "value": searchResult.group(7),
                        "lineCounter": lineCounter,
                        "commandType": "assignment"}

            #Function:
            elif searchResult.group(4) == "":
                return {"scope": scope,
                        "name": searchResult.group(1),
                        "value": searchResult.group(3),
                        "lineCounter": lineCounter,
                        "commandType": "functionCall"}

            #Declarations:
            else:
                return {"scope": scope, 
                        "name": searchResult.group(4), 
                        "value": searchResult.group(8),
                        "lineCounter": lineCounter,
                        "commandType": "declaration"}
        else:
            return None


# Debugging
#reader = C_Reader("pthread_setting_variables.c")
#reader.get_scopes(reader.file)
#for r in reader.result:
#    print(r)
