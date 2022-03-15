import matplotlib.pyplot as plt
import random 



# here is a function drawing a $n \times m$ grid 
def draw_initial_grid(n,m,fig): 
    plt.xlim([0,n]),plt.ylim([0,m])
    # here we draw $n-1$ vertical lines
    for i in range(1,n):
        plt.vlines(x=i,ymin=0,ymax=m,color='black',linewidth=0.5) 
    # here we draw $m-1$ horizontal lines 
    for j in range(1,m): 
        plt.hlines(y=j,xmin=0,xmax=n,color='black',linewidth=0.5)
    plt.tick_params(left = False, bottom = False) # here we remove ticks 

    return fig       

# tossing a coin: vertical or horizontal line 
def tosscoin():
    return random.randint(0,1)

# in this function we randomly generate a vertical line segment
def generate_vertical_line(n,m,d,l):

    i = random.randint(0,n-1) # here we randomly generate an integer between 0 and n-1  
    j = random.randint(1,d-1) # here we randomly generate an integer between 1 and d-1 
    vline_x = i + j/d # here we define the x-coordinate of a vertical line
    vline_ymin = random.randint(0,m-l) # here we define the ymin coordinate of a vertical line 
    vline_ymax = random.randint(vline_ymin + l,m) # here we define the ymax coordinate of a vertical line

    return vline_x, vline_ymin, vline_ymax
# in this function we draw a vertical line segment on a grid 
def draw_vertical_line(vline_x, vline_ymin, vline_ymax, fig):   
    
    # here we draw a vertical line 
    plt.vlines(x=vline_x,ymin=vline_ymin,ymax=vline_ymax,color='black',linewidth=0.5)

    return fig
    

# in this function we randomly generate a horizontal line segment 
def generate_horizontal_line(n,m,d,l): 

    i = random.randint(0,m-1) # here we randomly generate an integer between 0 and m-1 
    j = random.randint(1,d-1) # here we randomly generate an integer between 1 and d-1 
    hline_y= i + j/d # here we define the y-coordinate of a horizontal line 
    hline_xmin = random.randint(0,n-l) # here we define the xmin coordinate of a horizontal line 
    hline_xmax = random.randint(hline_xmin + l,n) # here we define the xmax coordinate of a horizontal line

    return hline_y, hline_xmin, hline_xmax  

# in this function we draw a horizontal line segment on a grid
def draw_horizontal_line(hline_y, hline_xmin, hline_xmax,fig):  

    # here we draw a horizontal line 
    plt.hlines(y=hline_y,xmin=hline_xmin,xmax=hline_xmax,color='black',linewidth=0.5)

    return fig

# here we create a list of lines 
def generate_hv_lines(hcells,vcells,hdiv,vdiv,poldegree,nlines):    
    
    # here we create a list of objects (lines) consisting of four fields:
    # the first field is 0, which corresponds to a horizontal line, or 1, which corresponds to a vertical line;    
    # if it is a horizontal line, the other three fields: hline_y, hline_xmin, hline_xmax;
    # if it is a vertical line, the other three fields: vline_x, vline_ymin, vline_ymax; 
     
    Lines=[]
        

    for i in range(nlines):

        if tosscoin()==0:
            hline_y, hline_xmin, hline_xmax = generate_horizontal_line(hcells,vcells,vdiv,poldegree)
            tuple = (0,hline_y, hline_xmin, hline_xmax)
            Lines.append(tuple)

        else:            
            vline_x, vline_ymin, vline_ymax = generate_vertical_line(hcells,vcells,hdiv,poldegree)
            tuple = (1,vline_x, vline_ymin, vline_ymax)
            Lines.append(tuple)
    
    return Lines 


# here we draw lines from a given list 
def draw_lines (Lines,fig): 
    
    nlines = len(Lines) 

    for i in range(nlines): 
        tuple = Lines[i]
        if tuple[0]==0: 
            hline_y = tuple[1]; hline_xmin = tuple[2]; hline_xmax = tuple[3]
            fig = draw_horizontal_line(hline_y,hline_xmin,hline_xmax,fig)
        else: 
            vline_x = tuple[1]; vline_ymin = tuple[2]; vline_ymax = tuple[3]    
            fig = draw_vertical_line(vline_x, vline_ymin, vline_ymax,fig)

    return fig

def draw_mesh(hcells,vcells,Lines): 
     
    # here we create a figure 
    fig =  plt.figure()  
    
    # he we draw an initial grid
    fig = draw_initial_grid(hcells,vcells,fig) 
    
    # here we draw lines 
    draw_lines(Lines,fig)

    plt.show()


# here we define the number of horizontal and vertical cells: hcells and vcells 
hcells=15;  vcells=10 

# here we define in how many parts we divide a cell horizontally and vertically  
hdiv=10;  vdiv=10 

# here we define the degree of polynomials; we assume that the degree is the same for x and y   
poldegree=3  

# number of lines dropped on a grid
nlines=80

#Lines = generate_hv_lines(hcells,vcells,hdiv,vdiv,poldegree,nlines)

Lines = [(0,3.1,5,11),(0,7.4,2,13),(1,2.6,2,7),(1,4.7,1,8)]

draw_mesh(hcells,vcells,Lines)