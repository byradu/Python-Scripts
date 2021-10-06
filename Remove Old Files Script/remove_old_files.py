import os
import datetime

ROOT = None
DIRECTORIES = None
FILES = None
DATA = {}
MAPPED_FILE_NAMES = {}

def check_path_existence(path:str)->bool:
    '''
    Checks if user's path exists in system. 
    '''
    global ROOT,DIRECTORIES,FILES
    if os.path.exists(path) == True:
        ROOT,DIRECTORIES,FILES = get_data(path)
        return True
    return False

def format_time(time:float) -> str:
    '''
    Returns the date in a readable format.

    '''
    return datetime.datetime.fromtimestamp(time).strftime('%d-%B-%y %H:%M')

def get_size_and_unit(size:int) -> tuple() :
    '''
    This function provides the size of a file in biggest unit available.
    Example: get_size_in_unit(1024) -> (1,'KB')
    '''
    biggest_size = 1
    if size == 1:
        unit = 'byte'
    elif size < 1024:
        unit = 'bytes'
        biggest_size = size
    elif size < 1024*1024 and size >= 1024:
        unit = 'KB'
        biggest_size = size/1024
    elif size < 1024*1024*1024 and size >= 1024*1024:
        unit = 'MB'
        biggest_size = size/(1024*1024)
    elif size <1024*1024*1024*1024 and size >= 1024*1024*1024:
        unit = 'GB'
        biggest_size = size/(1024*1024*1024)
    elif size <1024*1024*1024*1024*1024 and size >= 1024*1024*1024*1024:
        unit = 'TB'
        biggest_size = size/(1024*1024*1024*1024)
    return (biggest_size,unit)

def get_data(path:str)->tuple():
    '''
    It returns the root, directories and files from provided path.
    '''
    return tuple(os.walk(path))[0]

def get_information_from_directory(path:str)->tuple():
    '''
    Computes the size of the directory and returns: directory_size, unit_size, last_date_modified.
    '''

    directory_name = os.path.basename(path)
    directory_size = 0

    for root,_,files in os.walk(path):
        _,d,_ = get_information_from_files(files,root)
        directory_size += sum(d)

    last_time_accessed = os.stat(path).st_mtime
    
    return (directory_name,directory_size,last_time_accessed)

def get_information_from_files(files:list,path:str)->tuple():
    '''
    Computes the size of the files and returns:
    file_size, unit_size, last_date_modified for each file in directory.
    '''
    sizes = []
    file_names = []
    file_dates = []
    for file in files:
        file_names.append(file)
        
        full_path = os.path.join(path,file)

        structure = os.stat(full_path)
        sizes.append(structure.st_size)
        
        last_time_accessed = structure.st_mtime
        file_dates.append(last_time_accessed)

    return (file_names,sizes,file_dates)

def format_data(names:list,sizes:list,dates:list) :
    '''
    Formats all the necesary data and saves it in a global dictionary.
    '''
    for name,size,date in zip(names,sizes,dates):
        size,unit = get_size_and_unit(size)
        DATA[name] = {
                        'size':format(size,'.2f'),
                        'unit':unit,
                        'date':date
                     }

def show_results():
    '''
    Displays formated data to user.
    '''
    global MAPPED_FILE_NAMES

    counter = 1
    for key,value in sorted(DATA.items(),key = lambda element : element[1]['date'])[:10]:
        date = format_time(value["date"])
        print(f'{counter}. {key}:'.ljust(50),f'{value["size"]} {value["unit"]}'.ljust(25),f'accesed: {date}')#aliniem la stanga
        MAPPED_FILE_NAMES[counter] = key
        counter += 1

def get_entries_to_delete():
    '''
    Get the files user wants to delete, if he wants to delete something.
    '''
    while True:
        user_answer = input('Do you want to delete something? (yes/no) -> ').lower()
        if user_answer == 'yes':
            entries = set(map(int,input('''\nInsert the file numbers you want to delete.\nExample: 1 3 4 \n -> ''').split()))
            begin_to_delete(entries)
            break
        elif user_answer == 'no':
            print('Have a great day!')
            return
        else:
            print('Invalid answer. Try again.\n')


def begin_to_delete(entries:list):
    '''
    Begins to delete the entries that user provides.
    '''
    for entry in entries:
        if os.path.isfile(os.path.join(ROOT,MAPPED_FILE_NAMES[entry])):
            delete_file(MAPPED_FILE_NAMES[entry],ROOT)
        elif os.path.isdir(os.path.join(ROOT,MAPPED_FILE_NAMES[entry])):
            delete_directory(MAPPED_FILE_NAMES[entry])
        
    print('Everything was successfully deleted.')
    

def delete_file(filename:str,path:str):
    '''
    It will try to delete the file. If not will print an error.
    '''
    try:
        os.remove(os.path.join(path,filename))
    except Exception as e:
        print(str(e), f"error deleting file {filename}")

def delete_directory(filename:str):
    '''
    Since the function built to remove directories can't do that without
    an empty directory, we have to delete every file inside that directory.
    '''
    path = os.path.join(ROOT,filename)
    for root,directories,files in os.walk(path,topdown=False):
        for file in files:
            delete_file(file,root)
        try:
            for directory in directories:
                os.rmdir(os.path.join(root,directory))
        except Exception as e:
            print(str(e), 'Error deleting directory {filename}')
    try:
        os.removedirs(path)
    except Exception as e:
        print(str(e),"Last folder couldn't be deleted.")


if __name__ == '__main__':
    #Let's clear the terminal first
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        path = input('Insert the path to the directory -> ')
        if check_path_existence(path):
            break
        else:
            print("The path doesn't exists.")

    data = get_information_from_files(FILES,ROOT)
    format_data(data[0],data[1],data[2])

    for directory in DIRECTORIES:
        data = get_information_from_directory(os.path.join(ROOT,directory))
        data = [[x,] for x in data]
        format_data(data[0], data[1], data[2])

    show_results()
    get_entries_to_delete()
