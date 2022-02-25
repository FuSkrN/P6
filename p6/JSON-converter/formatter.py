import json

# Create temporary Transition System base class
class TS:
    def __init__(self, label, states, transitions):
        self.label = label
        self.states = states
        self.transitions = transitions
    
    def __repr__(self):
        return f'TS(label={self.label}, states={self.states}, transitions={self.transitions})'

# Fetch JSON object data as Python dict
# Each key is a TS object (light bulb, etc.)
data_list = []
with open('source_code.json', 'r') as jf:
    data = json.load(jf)
    for key, value in data.items():
        data_list.append(TS(value['label'], value['states'], value['transitions']))

for i in range(len(data_list)):
    print (data_list[i])