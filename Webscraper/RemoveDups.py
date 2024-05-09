import os

for filename in os.listdir(os.getcwd()): #iterate through all files in directory
    print(filename)
    if '.txt' in filename: #only .txt files
        lines_seen = set() #list of lines which are already present
        with open(os.path.join(os.getcwd(), '../NoDup/' + filename), 'w') as out_file: #open new destination file
            with open(os.path.join(os.getcwd(), filename), 'r') as in_file: #open input file
                for line in in_file:
                    if line not in lines_seen: #if next line not in the set of lines already present add it to the output file and then add the line to the set
                        out_file.write(line)
                        lines_seen.add(line)
