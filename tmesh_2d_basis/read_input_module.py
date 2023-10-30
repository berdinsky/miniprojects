import os

def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)

   return file_path

def read_input():        
    
    file_path = open_file_in_same_directory('input.txt')    

    file = open(file_path,'r')   
    
    rows = file.readlines()

    return int(rows[4]), int(rows[5]), int(rows[6]), int(rows[7])
