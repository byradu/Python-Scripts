import os
import json

def get_input_file(name:str)->str:
    '''
    Loads the structure from the file.
    '''
    try:
        with open(name) as f:
            content = json.load(f)
    except FileNotFoundError as e:
            print(str(e))
            return ''
    else:
        return content

def check_input_path(name:str)->bool:
    '''
    Checks if user path exists.
    '''
    return os.path.exists(name)

def create_directories(directory_path:str, structure:str)->None:
    '''
    Creates files & directories recursively.
    '''
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
    while True:
        file_path = input('Insert the path to the file structure -> ')
        if check_input_path(file_path):
            json_content = get_input_file(file_path)
            break
        else: 
            print('Check your path and try again.')

    while True:
        target_directory = input('Path to target directory -> ')
        if check_input_path(target_directory):
            break
        else:
            print('Check your path and try again.')

    create_directories(target_directory,json_content)