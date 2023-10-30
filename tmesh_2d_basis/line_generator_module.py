###############################################################################
# This module generate lines                                                  #
###############################################################################

import random

# tossing a coin: vertical or horizontal line 
def tosscoin():
    return random.randint(0,1)

# in this function we randomly generate a vertical line segment
def generate_vertical_line(n,m,d,l):
    i = random.randint(0,n-1)   
    j = random.randint(1,d-1) 
    vline_ymin = random.randint(0,m-l) 
    vline_ymax = random.randint(vline_ymin + l,m) 

    return i, j, vline_ymin, vline_ymax
    
# in this function we randomly generate a horizontal line segment 
def generate_horizontal_line(n,m,d,l): 
    i = random.randint(0,m-1)  
    j = random.randint(1,d-1)    
    hline_xmin = random.randint(0,n-l)  
    hline_xmax = random.randint(hline_xmin + l,n) 

    return i, j, hline_xmin, hline_xmax  

# here we create a list of lines; 0 means a horizontal line; 1 means a vertical line 
def generate_hv_lines(hcells,vcells,hdiv,vdiv,poldegree,nlines):    
    Lines=[]       
    for i in range(nlines):
        if tosscoin()==0:
            hline_y_int, hline_y_frac, hline_xmin, hline_xmax  = generate_horizontal_line(hcells,vcells,vdiv,poldegree)
            tuple = (0,hline_y_int, hline_y_frac, hline_xmin, hline_xmax)
            Lines.append(tuple)
        else:            
            vline_x_int, vline_x_frac, vline_ymin, vline_ymax = generate_vertical_line(hcells,vcells,hdiv,poldegree)
            tuple = (1,vline_x_int, vline_x_frac, vline_ymin, vline_ymax)
            Lines.append(tuple)
    
    return Lines 