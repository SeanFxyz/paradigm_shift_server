import json

def texts1():
    return json.dumps(json.load("default_data/texts1.json"))

def texts2():
    return json.dumps(json.load("default_data/texts2.json"))

def texts3():
    return json.dumps(json.load("default_data/texts3.json"))

def images():
    return json.dumps(json.load("default_data/images.json"))
