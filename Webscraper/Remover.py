import os
import re

for filename in os.listdir(os.getcwd()): #iterate through files in directory
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        content = f.readlines() #read the content of the file
    f.close()
    print(filename)
    if '.txt' in filename:
        if ('B' in content[0]) or ('B' in content[1]): #if it has B in the first 2 lines it's safe overwise remove the file
            print("safe")
        else:
            print("Remove")
            os.remove('./' + filename)
    
