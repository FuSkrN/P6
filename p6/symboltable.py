import python_reader

class Symboltable:
    """A class used to represent the symbol table.
       The symbol table is a dictionary, which consists of a scope and its corresponding list of variables."""
    def __init__(self):
        self.symboltable = [{"scope": "global",
                            "varList": []}]

    def add_symbol(self, symbolDict):
        """Inserts a symbol (variable) in the symbol table."""
        tempDict = {"name": symbolDict['name'],
                    "value": symbolDict['value'],
                    "scope": symbolDict['scope']}
        scopeFound = False

        #Loop through each symbol in the symbol table.
        for sAdd in self.symboltable:

            #If the temporary dictionary variable and an existing symbol shares a scope, 
            #append the temp var list to the existing var list.
            if sAdd['scope'] == tempDict['scope']:
                sAdd['varList'].append(tempDict)
                scopeFound = True
                break
        
        #If no scope is found, create one and append the var list to it.
        if scopeFound == False:
            self.symboltable.append({"scope": tempDict['scope'],
                                "varList": [tempDict]})

    def update_symbol_value(self, symbolDict):
        """Updates the value of a symbol in the symbol table with the given parameter symbolDict."""
        #Each scope level is separated by a seperator (.)
        seperator = "."
        
        # Flag indicating whether the var to be updated exists.
        varFound = False

        while varFound == False:

            #Loop through the entries in the symbol table.
            for sUpdate in self.symboltable:

                #If the input shares the same scope with an entry ...
                if sUpdate['scope'] == symbolDict['scope']:

                    #Loop through all variables in the list of variables.
                    for var in sUpdate['varList']:

                        #If a match is found (name and values), a variable match is found.
                        if var['name'] == symbolDict['name']:
                            var['value'] = symbolDict['value']
                            varFound = True
                            break
                    break

            #Split the scope name on the separator and remove the last part.
            #Go one scope level up ...
            tempName = symbolDict['scope'].split(seperator)
            tempName.pop()
            symbolDict['scope'] = seperator.join(tempName)


    def update_symbol(self, dictionary):
        """Update the symbol of a dictionary using the given input dictionary. 
        Conditions for declaration and assignment differ."""
        if dictionary['commandType'] == "declaration":
            
            #Add the variable to dictionary directly.
            self.add_symbol(dictionary)
            
        elif dictionary['commandType'] == "assignment":
            
            #Replace value in dictionary rather than inserting a new entry.
            self.update_symbol_value(dictionary)

        else:
            #Something went wrong
            pass

    def retrieve_symbol(self, dictionary):
        """Retrieves a symbol in the dictionary based on the input variable dictionary."""
        seperator = "."
        #Loop until the condition is met.
        while True:

            #Loop through each entry (scope) in the symbol table.
            for scope in self.symboltable:

                #Check whether a match is found based on the scope name and their variables.
                if scope['scope'] == dictionary['scope']:
                    for var in scope['varList']:
                        if var['name'] == dictionary['name']:
                            return var['value']
                elif dictionary['scope'] == "":
                    return

            #Go up one scope level. 
            #If the scope name is empty, return nothing.
            tempName = dictionary['scope'].split(seperator) 
            tempName.pop()
            dictionary['scope'] = seperator.join(tempName)
            if len(dictionary['scope'].split(seperator)) == 0:
                return

    def find_global_vars(self):
        returnList = []
        for var in self.symboltable[0]['varList']:
            if var['scope'] == "global":
                returnList.append(var)
        return returnList
