
# String compares the name of a dictionary (assumed functionCall) with pthread matches
# Figures out whether the function is a pthread_create or pthread_join call, otherwise returns null
def find_pthread(dict):
    x = dict["name"]
    if x == "pthread_create":
        return {"create", dict}
    elif x == "pthread_join":
        return {"join", dict}
    else:
        return {"null", dict}

# TODO: implement
def create_thread(thread, func):

# TODO: implement
# Paramenters?
def simulate_configuration():