import os

def create_dict(folder_path):
    file_dictionary = {}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                first_line = file.readline().strip()
                file_dictionary[filename] = first_line
    return file_dictionary


folder_path = input("enter folder path: ")
result_dict = create_dict(folder_path)

inv_map = {v: k for k, v in result_dict.items()}

print(inv_map)