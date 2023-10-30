import sys
from tkinter import messagebox
from tkinter import simpledialog

def ask_number_lines():

    answer = simpledialog.askinteger("Question", 
                                     "How many lines would you like to drop?")
                                     

    return answer        

def animation_yesno(n):
    answer=messagebox.askyesno('There are '+str(n)+' new basis functions.',
                                 'Would you like to see them?')
    
    if not answer: 
        sys.exit()

