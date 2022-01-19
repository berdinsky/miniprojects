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

# in this function we randomly drop a vertical line segment on a grid 
def drop_vertical_line(n,m,d,l,fig):
    i = random.randint(0,n-1) # here we randomly generate an integer between 0 and n-1  
    j = random.randint(1,d-1) # here we randomly generate an integer between 1 and d-1 
    vline_x = i + j/d # here we define the x-coordinate of a vertical line
    vline_ymin = random.randint(0,m-l) # here we define the ymin coordinate of a vertical line 
    vline_ymax = random.randint(vline_ymin + l,m) # here we define the ymax coordinate of a vertical line   
    
    # here we draw a vertical line 
    plt.vlines(x=vline_x,ymin=vline_ymin,ymax=vline_ymax,color='black',linewidth=0.5)

    return fig

# in this function we randomly drop a horizontal line segment on a grid
def drop_horizontal_line(n,m,d,l,fig):
    i = random.randint(0,m-1) # here we randomly generate an integer between 0 and m-1 
    j = random.randint(1,d-1) # here we randomly generate an integer between 1 and d-1 
    hline_y= i + j/d # here we define the y-coordinate of a horizontal line 
    hline_xmin = random.randint(0,n-l) # here we define the xmin coordinate of a horizontal line 
    hline_xmax = random.randint(hline_xmin + l,n) # here we define the xmax coordinate of a horizontal line  
    
    # here we draw a horizontal line 
    plt.hlines(y=hline_y,xmin=hline_xmin,xmax=hline_xmax,color='black',linewidth=0.5)

    return fig

def tosscoin():
    return random.randint(0,1)

def main(hcells,vcells,hdiv,vdiv,poldegree,nlines): 
    
    # here we create a figure 
    fig =  plt.figure()  


    # he we draw an initial grid
    fig = draw_initial_grid(hcells,vcells,fig) 

    
    for i in range(nlines):

        if tosscoin()==0:
            fig = drop_horizontal_line(hcells,vcells,vdiv,poldegree,fig)
        else:            
            fig = drop_vertical_line(hcells,vcells,hdiv,poldegree,fig)
    
    plt.show()
   

# here we define the number of horizontal and vertical cells: hcells and vcells 
hcells=15;  vcells=10 

# here we define in how many parts we divide a cell horizontally and vertically  
hdiv=10;  vdiv=10 

# here we define the degree of polynomials; we assume that the degree is the same for x and y   
poldegree=3  

# number of lines dropped on a grid
nlines=6

main(hcells,vcells,hdiv,vdiv,poldegree,nlines)