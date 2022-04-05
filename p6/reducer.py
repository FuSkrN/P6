#TODO: delete imports after
import generator
import python_reader

class reducer:
    def __init__(self, stateArray):
        self.stateArray = stateArray.copy()
    
    def reduce_sequence(self):
        stateQueue = self.stateArray.copy()
        while len(stateQueue) != 0:
            resultFlag = stateQueue[0].link_ingoing_outgoing()
            if resultFlag:
                self.stateArray.pop(self.stateArray.index(stateQueue[0]))
            stateQueue.pop(0)


a = python_reader.C_Reader('pthread_setting_variables.c')
a.get_scopes(a.file)
b = generator.graph(a.result)

r = reducer(b.stateArray)
r.reduce_sequence()
#for r in a.result:
#    print(r)
for x in r.stateArray:
    print(f"stateName: {x.label}")
    print(f"programCounters: {x.programCounters:}")
    for p in x.symboltable.symboltable:
        print(p)
    for y in x.ingoing:
        print(f"ingoing: {y.label}")
    for z in x.outgoing:
        print(f"outgoing: {z.label}")
    print("\n")

print(f"size before: {len(b.stateArray)}")
print(f"size after: {len(r.stateArray)}")
