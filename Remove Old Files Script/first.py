import sys,os,datetime

results = {}

def CheckPath():
    if len(sys.argv) <2:
        print('\nPath was not inserted.')
        return False
    if(os.path.exists(sys.argv[1])==False):
        print("Invalid path")
        return False
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

def GetDirectorySize(path):
    finalSize = 0
    for (root,directories,files) in os.walk(path):
        for fileName in files:
            full_fileName = os.path.join(root,fileName)
            finalSize+=os.stat(full_fileName).st_size
    return finalSize


def GetUnitSize(size):
    unit =''
    final_size = 1
    if size == 1:
        unit = 'byte'
    elif size < 1024:
        unit = 'bytes'
        final_size = size 
    elif size < 1024*1024 and size >= 1024:
        unit = 'KB'
        final_size = size/1024
    elif size < 1024*1024*1024 and size >= 1024*1024:
        unit = 'MB'
        final_size = size/(1024*1024)
    elif size <1024*1024*1024*1024 and size >= 1024*1024*1024:
        unit = 'GB'
        final_size = size/(1024*1024*1024)
    elif size <1024*1024*1024*1024*1024 and size >= 1024*1024*1024*1024:
        unit = 'TB'
        final_size = size/(1024*1024*1024*1024)
    return final_size,unit

def WalkDir():
    for (root,directories,files) in os.walk(sys.argv[1]):
        for fileName in files:
            full_fileName = os.path.join(root,fileName)
            size,unit = GetUnitSize(os.stat(full_fileName).st_size)
            size = float("{:.2f}".format(size))#limita la 2 zecimale
            if(size.is_integer()):
                size = int(size)
            #print (f"{full_fileName} : {size} {unit}")
            results[fileName] = {'path':full_fileName,'size':os.stat(full_fileName).st_size,'date':os.stat(full_fileName).st_atime}
        if len(directories) > 0 :
            for d in directories:
                full_directory =os.path.join(root,d)
                results[d] = {'path':full_directory,'size':GetDirectorySize(full_directory),'date':os.stat(full_directory).st_atime}

def RemoveNonEmptyDirectory(path):
    for (root,directories,files) in os.walk(path,topdown=False):
        for file in files:
            os.remove(os.path.join(root,file))
        for d in directories:
            os.rmdir(os.path.join(root,d))

if(CheckPath() == False):
    raise SystemExit
else:
    try:
        WalkDir()
    except Exception as e:
        print("WalkDir: ",str(e))

sortedResult = sorted(results.items(),key=lambda item:item[1]['date'],reverse=False)
show = {k[0]:k[1] for k in sortedResult[:10]}
counter = 1

mapped={}
for name,d in show.items():
    size,unit = GetUnitSize(d['size'])
    size = float("{:.2f}".format(size))#limita la 2 zecimale
    if(size.is_integer()):
        size = int(size)
    lt = datetime.datetime.fromtimestamp(d['date']).strftime('%H:%M %d.%m.%Y')#formatare data
    print(f'{counter}. {name}:'.ljust(50),f'{size} {unit}'.ljust(25),f'accesed: {lt}')#aliniem la stanga
    mapped[counter]=name
    counter+=1    

answer =''
toDelete=[]
while(1):

    if answer.lower() == 'yes':
        pass
    else:
        answer = input("\nDo you want to delete files? (yes/no) ->  ")
    if answer.lower() == 'no':
        print("Have a great day!")
        break
    elif answer.lower() == 'yes':
        filesToDelete = input('\nInsert the numbers you want to delete (type the numbers with commas between them. ex: 3,1)->  ')
        try:
            toDelete=[int(x) for x in filesToDelete.split(',')]
            if max(toDelete) >10:
                raise Exception('You have inserted a value over max available.')
            break
        except Exception as e:
            print(str(e))
    else:
        print('\nInvalid input. Try again')

for item in toDelete:
    path = show[mapped[item]]['path']
    if os.path.isdir(path):
        RemoveNonEmptyDirectory(path)
        os.rmdir(path)
        print(f'\n{mapped[item]} was successfully removed')
    else:
        try:
           os.remove(path)
           print(f'\n{mapped[item]} was successfully removed')
        except Exception as e:
            print(str(e))