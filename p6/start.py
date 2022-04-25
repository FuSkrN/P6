import sys

import python_reader
import generator
import reducer

def start(args):
    if len(args) <= 1:
        print("This program is called as 'python start.py <filename> <reduction option>'")
        print("The reduction options are:")
        print("-r1\tReduces states that are in a sequence, in which the middle state only has one ingoing and outgoing transition")
        print("-ra\tPerforms all reductions")
    else:
        reader = python_reader.C_Reader(args[1])
        reader.get_scopes(reader.file, 0)
        graph = generator.graph(reader.result)
        red = reducer.reducer(graph.stateArray)
        
        if len(args) == 3:
            outputName = args[1] + "." + args[2] + ".graph.txt"
            if args[2] == "-ra" or args[2] == "-r1":
                print(f"performing -r1 on a set of size {len(graph.stateArray)}")
                red.reduce_sequence()
                print(f"Resulting size is {len(graph.stateArray)}")
            if args[2] == "-ra" or args[2] == "-r2":
                print(f"performing -r2 on a set of size {len(graph.stateArray)}")
                red.reduce_local_varsplit()
                print(f"Resulting size is {len(graph.stateArray)}")
        else:
            outputName = args[1] + ".graph.txt"

        with open(outputName, "a") as fileWriter:
            for x in graph.stateArray:
                fileWriter.write(f"stateName: {x.label}\n")
                fileWriter.write(f"programCounters: {x.programCounters}\n")
                for p in x.symboltable.symboltable:
                    fileWriter.write(str(p))
                    fileWriter.write("\n")
                for y in x.ingoing:
                    fileWriter.write(f"ingoing: {y.label}\n")
                for z in x.outgoing:
                    fileWriter.write(f"outgoing: {z.label}\n")
                fileWriter.write("\n")

start(sys.argv)
