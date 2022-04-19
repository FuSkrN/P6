import re
import python_reader
import symboltable

def findVars(expression):
    """Finds and extracts the variables in an expression using regex pattern matching.
    Returns a list of matches in the given string."""
    variableRegex = re.compile('[a-zA-Z][a-zA-Z0-9]*')
    variables = re.findall(variableRegex, str(expression))
    return variables

def replace_vars_without_update(variabledict, symboltable):
    # Finds the parts of a variable expression and saves it as a list.
    varsInExpression = findVars(variabledict['value'])

    #Sorts the list in descending order to replace the larger variable names first.
    varsInExpression.sort(key=sortByNameLength, reverse=True)

    #For each variable in the expression...
    for variable in varsInExpression:

        #Create a temporary dictionary used to update the value in a symbol table.
        tempdict = {"name": variable, "scope": variabledict['scope']}

        #Find the actual value in the symbol table.
        varVal = symboltable.retrieve_symbol(tempdict)

        #Replace the value of the corresponding dictionary.
        variabledict['value'] = variabledict['value'].replace(variable, f"({varVal})")
        
    return variabledict
 

def replaceVars(variabledict, symboltable):
    """Updates the stored value of a variable in a symbol table with the input variable dictionary."""
    
    #Error handling to prevent crashing when passing the dictionary to symboltable.
    if variabledict['commandType'] == 'functionCall' or variabledict['value'] == None:
        return
    
    variabledict = replace_vars_without_update(variabledict, symboltable)

    #Evaluate the expression isn't NULL or empty. Afterwards, update the value.
    if variabledict['value'] != None or variabledict['value'] != "":
        variabledict['value'] = evaluateExpression(variabledict['value'])
    symboltable.update_symbol(variabledict)

def evaluateExpression(expression):
    """Evaluates the contents of an expression using eval()."""
    try:
        if expression == "":
            return "0"
        else:
            return str(eval(expression))
    except:
        pass

def sortByNameLength(x):
    return len(x)


