import json
import os
import sys



def get_input_file(name):
    try:
        with open(name) as f:
            content = json.load(f)
    except FileNotFoundError as e:
            content = e
    return content

def check_input_path(name):
    return os.path.exists(name)

def create_directories(directory_path, structure):
    os.chdir(directory_path)
    for key,value in structure.items():
        if type(value) == dict:
            try:
                os.mkdir(key)
            except OSError as e:
                print(e)
            new_path = os.path.join(directory_path,key)
            create_directories(new_path,value)
        else:
            with open(key,'w') as new_file:
                new_file.write(value)
    os.chdir('..')

if __name__ == '__main__':
    if check_input_path('/home/radu/Documents/algo1'):
        json_content = get_input_file(name)