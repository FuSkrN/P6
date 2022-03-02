import pthread_race_cond

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

reader = Python_Reader("pthread_race_cond.py")
#reader.print_functions()
reader.print_variables()
