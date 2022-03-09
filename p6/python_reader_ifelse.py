from fileinput import filename
import re

class C_reader:
    def __init__(self, fileName):
        self.fileName = filename
        with open(self.fileName) as file:
            self.fileLines = file.readlines()

    def get_ifelse(self, line):
        #regex pattern to match if-else-else if statements; accounts for multiline formatting
        declarationPattern = re.compile('^if\s*\((.*?)\)\s*{(.*?)}(\s*(else|else\s+if\s*\((.*?)\))\s*{(.*?)})*$')
        searchResult = re.search(declarationPattern, line, flags=re.MULTILINE)
        if(searchResult != None):
            print(f"searchResult: {searchResult.string}")
            print(f"Group 1: {searchResult.group(1)}")
            print(f"Group 2: {searchResult.group(2)}")
            print(f"Group 3: {searchResult.group(3)}")
            print(f"Group 4: {searchResult.group(4)}")
            print(f"Group 5: {searchResult.group(5)}\n\n")
            #returns the conditional structure (if-else-elseif ...)
            return {"ifCondition": searchResult.group(1),
                    "ifScope": searchResult.group(2),
                    "elseScope": searchResult.group(3),
                    "elseIfCondition": searchResult.group(4),
                    "elseIfScope": searchResult.group(5)}
            