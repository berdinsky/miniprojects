###################################
#This module draws a tmesh        #
###################################
import matplotlib.pyplot as plt

# here is a function drawing a $n \times m$ grid
def draw_initial_grid(n,m,fig): 
    plt.xlim([0,n]),plt.ylim([0,m])    
    for i in range(1,n):
        plt.vlines(x=i,ymin=0,ymax=m,color='black',linewidth=0.5)     
    for j in range(1,m): 
        plt.hlines(y=j,xmin=0,xmax=n,color='black',linewidth=0.5)
    # here we remove ticks
    plt.tick_params(left = False, bottom = False)  

    return fig    

# in this function we draw a vertical line segment on a grid 
def draw_vertical_line(vline_x, vline_ymin, vline_ymax, fig):       
    plt.vlines(x=vline_x,ymin=vline_ymin,ymax=vline_ymax,
               color='black',linewidth=0.5)
    
    return fig   

# in this function we draw a horizontal line segment on a grid
def draw_horizontal_line(hline_y, hline_xmin, hline_xmax,fig):  
    plt.hlines(y=hline_y,xmin=hline_xmin,xmax=hline_xmax,
               color='black',linewidth=0.5)

    return fig

# here we draw lines from a given list 
def draw_lines (Lines,fig,hdiv,vdiv):     
    nlines = len(Lines) 
    for i in range(nlines): 
        tuple = Lines[i]
        if tuple[0]==0: 
            hline_y_int = tuple[1]; hline_y_frac=tuple[2] 
            hline_xmin = tuple[3]; hline_xmax = tuple[4]
            hline_y = hline_y_int + hline_y_frac/vdiv
            fig = draw_horizontal_line(hline_y,hline_xmin,hline_xmax,fig)
        else: 
            vline_x_int = tuple[1]; vline_x_frac = tuple[2]  
            vline_ymin = tuple[3]; vline_ymax = tuple[4]
            vline_x = vline_x_int + vline_x_frac/hdiv    
            fig = draw_vertical_line(vline_x, vline_ymin, vline_ymax,fig)

    return fig

# here we draw a mesh
def draw_mesh(hcells,vcells,Lines,hdiv,vdiv):      
    fig =  plt.figure()  
    fig = draw_initial_grid(hcells,vcells,fig) 
    draw_lines(Lines,fig,hdiv,vdiv)

    plt.show()
