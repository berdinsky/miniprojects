import os

def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)

   return file_path

def save_knots(list_knots):        
    
    file_path = open_file_in_same_directory('knots.txt')    

    file = open(file_path,'w')   
    
    file.write('The number of new added basis functions: ')
    
    file.write(str(len(list_knots)))

    file.write('\n')

    for list_knots_tuple in list_knots: 
        st=str(list_knots_tuple)
        file.write(st)
        file.write('\n')
    
    file.close()    