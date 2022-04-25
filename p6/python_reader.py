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
        self.forPattern = re.compile('for\s*\((.*)\).*')
        self.ifPattern = re.compile('if\s*\((.*?)\)')
        self.elseIfPattern = re.compile('else if *\((.*?)\)')
        self.elsePattern = re.compile('else')
        self.functionCallPattern = re.compile('\s*((\-)*[_a-zA-Z][a-zA-Z0-9_\-]*)\((.*?)\)();')
        self.booleanPattern = re.compile('\s*([a-zA-Z0-9]+)\s*(==|<=|>=|<|>|!=)\s*([a-zA-Z0-9]+)\s*')
        self.numberPattern = re.compile('[0-9]*')

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
        elseCounter = 0
        shouldPop = False
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
                    self.scopeName.append('.for' + '(' + str(self.forNameCounter) + ')')
                    self.forNameCounter += 1
                    self.handle_for(searchResult)
                    isInScope = True
                else:
                    #Checks if the line is an if logic statement.
                    searchResult = re.search(self.ifPattern, line)

                    if searchResult != None and counter == 0 and re.search(self.elseIfPattern, line) == None:
                        self.scopeName.append('.if' + '(' + str(self.ifNameCounter) + ')')
                        elseCounter = self.ifNameCounter
                        scope = ''
                        for s in self.scopeName:
                            scope = scope + s
                        ifStatement = {"scope": scope,
                            "name": f"if({str(self.ifNameCounter)})",
                            "value": searchResult.group(1),
                            "lineCounter": lineCounter,
                            "commandType": "ifStatement"}
                        self.result.append(ifStatement)
                        lineCounter += 1
                        self.ifNameCounter += 1
                        isInScope = True

                    else:
                        #Checks if the line is an if-else statement
                        searchResult = re.search(self.elseIfPattern, line)

                        if searchResult != None and counter == 0:
                            self.scopeName.append('.ifelse' + '(' + str(elseCounter) + '-' + str(self.ifElseNameCounter) + ')')
                            scope = ''
                            for s in self.scopeName:
                                scope = scope + s
                            ifStatement = {"scope": scope,
                                "name": f"ifElse({str(self.ifElseNameCounter)})",
                                "value": searchResult.group(1),
                                "lineCounter": lineCounter,
                                "commandType": "ifElseStatement"}
                            self.result.append(ifStatement)
                            lineCounter += 1
                            self.ifElseNameCounter += 1
                            isInScope = True

                        else:
                            #Checks if the line is an else statement
                            searchResult = re.search(self.elsePattern, line)
                            
                            if searchResult != None and counter == 0:
                                self.scopeName.append('.else' + '(' + str(elseCounter) + ')')
                                scope = ''
                                for s in self.scopeName:
                                    scope = scope + s
                                ifStatement = {"scope": scope,
                                        "name": f"else({elseCounter})",
                                        "value": "",
                                        "lineCounter": lineCounter,
                                        "commandType":"elseStatement"}
                                self.result.append(ifStatement)
                                lineCounter += 1
                                isInScope = True
            
            #Appends text that is not the start of a scope, or end of a scope, to a string.
            if isInScope == True:
                text, counter = self.get_scope_body(line, counter, text)

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
        print(isInScope)
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

    def handle_for(self, forParam):
        splitResult = forParam.group(1).split(';')
        variableName = ''
        iterationCounter = 0
        variableStartValue = ''
        booleanDelta = 0
        searchResult = re.search(self.declarationPattern, splitResult[0] + ';')
        if searchResult != None:
            variableName = searchResult.group(4)
            variableStartValue = searchResult.group(8)
        else:
            searchResult = re.search(self.assignmentPattern, splitResult[0] + ';')
            if searchResult != None:
                variableName = searchResult.group(2)
                variableStartValue = searchResult.group(7)
            else:
                print("try to compile the code, i swear it wont compile")
        booleanResult = re.search(self.booleanPattern, splitResult[1])
        for value in booleanResult.groups():
            
            if value.isnumeric():
                booleanDelta = abs(int(variableStartValue) - int(value))
        if splitResult[2].strip() == variableName + '++' or splitResult[2].strip() == variableName + '--':
            iterationCounter = booleanDelta
        else:
            numberResult = re.search(self.numberPattern, splitResult[2])
            if numberResult != None:
                iterationCounter = booleanDelta/int(numberResult.group())

        return [variableName, iterationCounter]

    def get_scope_body(self, line, counter, text):
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
        return text, counter

# Debugging
reader = C_Reader("ifelse.c")
reader.get_scopes(reader.file)
for r in reader.result:
    print(r)
