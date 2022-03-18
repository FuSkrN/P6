# Example dictionaries
# Dict1 contains terms that should be updated with key-value pairs from dict1
dict1 = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
dict2 = {'value1': 'AAA', 'value3': 'CCC'}

print("dict1 is: ", dict1)
print("dict2 is: ", dict2)

# Updates dict1 with values from dict2
# Step 1: Create a new list of dicts res
# Step 1.5: Creating 'res' can be omitted by using a one-liner: dict1 = {k: dict2.get(v, v) for k, v in dict1.items()} ...
# Step 2: Create a key-value pair in 'res' iff some key (key_2) in dict2 is equal to val_1 = dict1[key_1] (if key_2 == dict1[key_1])
# Step 3: Each key-value pair now represents the updated key-value pairs of dict1
res = {key: dict2.get(value, value) for key, value in dict1.items()}
dict1 = res
print(dict1)