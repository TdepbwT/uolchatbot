import os
import re

for filename in os.listdir(os.getcwd()): #get the current directory and iterate through each file
    with open(os.path.join(os.getcwd(), filename), 'r') as f: #open the current file
        content = f.readlines() #read the content
    f.close()
    print(filename)
    if '.txt' in filename:
        if ('MB' in content[0]) or ('MB' in content[1]):
            print("Remove")
            os.remove('./' + filename) #remove the file if it is .txt and has MB in the first 2 lines
            
            
