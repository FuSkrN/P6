import python_reader

class Symboltable:
    def __init__(self):
        #create symboltable
        self.symboltable = [{"scope": "global",
                            "varList": []}]

    def add_symbol(self, symbolDict):
        #add a symbol to the symboltable
        tempDict = {"name": symbolDict['name'],
                    "value": symbolDict['value'],
                    "scope": symbolDict['scope']}
        scopeFound = False

        for sAdd in self.symboltable:
            if sAdd['scope'] == tempDict['scope']:
                sAdd['varList'].append(tempDict)
                scopeFound = True
                break
        if scopeFound == False:
            self.symboltable.append({"scope": tempDict['scope'],
                                "varList": [tempDict]})

    def update_symbol_value(self, symbolDict):
        #update the value of a symbol in the symboltable
        seperator = "."

        varFound = False
        while varFound == False:
            for sUpdate in self.symboltable:
                if sUpdate['scope'] == symbolDict['scope']:
                    for var in sUpdate['varList']:
                        if var['name'] == symbolDict['name']:
                            var['value'] = symbolDict['value']
                            varFound = True
                            break
                    break
            tempName = symbolDict['scope'].split(seperator)
            tempName.pop()
            symbolDict['scope'] = seperator.join(tempName)


    def update_symbol(self, dictionary):
        if dictionary['commandType'] == "declaration":
            #add variable to dictionary
            self.add_symbol(dictionary)
            
        elif dictionary['commandType'] == "assignment":
            #replace value in dictionary
            self.update_symbol_value(dictionary)

        else:
            #something went wrong
            pass

    def retrieve_symbol(self, dictionary):
        seperator = "."
        while True:
            for scope in self.symboltable:
                if scope['scope'] == dictionary['scope']:
                    for var in scope['varList']:
                        if var['name'] == dictionary['name']:
                            return var['value']

            tempName = dictionary['scope'].split(seperator) 
            tempName.pop()
            dictionary['scope'] = seperator.join(tempName)
            if len(dictionary['scope'].split(seperator)) == 0:
                return
        


