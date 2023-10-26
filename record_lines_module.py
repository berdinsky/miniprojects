import os

def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)

   return file_path

def save_lines(Lines):        
    
    file_path = open_file_in_same_directory('lines.txt')    

    file = open(file_path,'w')   
    
    for Lines_tuple in Lines:  
        st=str(Lines_tuple)
        file.write(st)
        file.write('\n')
    
    file.close()    


