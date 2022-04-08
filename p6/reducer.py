#TODO: delete imports after
import generator
import python_reader

class reducer:
    """A collection (class) of methods used in graph reduction."""
    def __init__(self, stateArray):
        self.stateArray = stateArray.copy()
    
    def reduce_sequence(self):
        """Implements the function link_ingoing_outgoing using a state queue."""
        stateQueue = self.stateArray.copy()
        while len(stateQueue) != 0:

            #resultFlag is a flag indicating whether a state in the stateQueue is able to be reduced in first-order.
            resultFlag = stateQueue[0].link_ingoing_outgoing()
            
            # If True, remove the reduced state from the state array.
            if resultFlag:
                self.stateArray.pop(self.stateArray.index(stateQueue[0]))
            
            #Remove the state from the state queue.
            stateQueue.pop(0)

# Read and parse a C file, and then generate its resulting state array graph.
#a = python_reader.C_Reader('pthread_setting_variables.c')
#a.get_scopes(a.file)
#b = generator.graph(a.result)

#Perform graph reduction.
#r = reducer(b.stateArray)
#r.reduce_sequence()
#for r in a.result:
#    print(r)
#for x in r.stateArray:
#    print(f"stateName: {x.label}")
#    print(f"programCounters: {x.programCounters:}")
#    for p in x.symboltable.symboltable:
#        print(p)
#    for y in x.ingoing:
#        print(f"ingoing: {y.label}")
#    for z in x.outgoing:
#        print(f"outgoing: {z.label}")
#    print("\n")

#print(f"size before: {len(b.stateArray)}")
#print(f"size after: {len(r.stateArray)}")
