from scipy.interpolate import BSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
import numpy as np
import random 
import gc
#######################################################################################
# BLOCK : here we generate lines and draw a grid 
#######################################################################################
# here is a function drawing a $n \times m$ grid 
def draw_initial_grid(n,m,fig): 
    plt.xlim([0,n]),plt.ylim([0,m])    
    for i in range(1,n):
        plt.vlines(x=i,ymin=0,ymax=m,color='black',linewidth=0.5)     
    for j in range(1,m): 
        plt.hlines(y=j,xmin=0,xmax=n,color='black',linewidth=0.5)
    plt.tick_params(left = False, bottom = False) # here we remove ticks 

    return fig       

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

# in this function we draw a vertical line segment on a grid 
def draw_vertical_line(vline_x, vline_ymin, vline_ymax, fig):       
    plt.vlines(x=vline_x,ymin=vline_ymin,ymax=vline_ymax,color='black',linewidth=0.5)
    
    return fig
    
# in this function we randomly generate a horizontal line segment 
def generate_horizontal_line(n,m,d,l): 
    i = random.randint(0,m-1)  
    j = random.randint(1,d-1)    
    hline_xmin = random.randint(0,n-l)  
    hline_xmax = random.randint(hline_xmin + l,n) 

    return i, j, hline_xmin, hline_xmax  

# in this function we draw a horizontal line segment on a grid
def draw_horizontal_line(hline_y, hline_xmin, hline_xmax,fig):  
    plt.hlines(y=hline_y,xmin=hline_xmin,xmax=hline_xmax,color='black',linewidth=0.5)

    return fig

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
#########################################################################################
#BLOCK : here we update a tree of segments
#########################################################################################
# here we update a tree of horizontal segments  
def update_hsegments(hsegments,hline_y_int,hline_y_frac,hline_xmin, hline_xmax):
    new_segment=(hline_xmin,hline_xmax)
    hsegments_int_val=hsegments.get(hline_y_int)
    if hsegments_int_val is not None: 
        hsegments_frac_val=hsegments_int_val.get(hline_y_frac)
        if hsegments_frac_val is not None:            
            insert_segment_main(hsegments_frac_val,hsegments_frac_val.head,hline_xmin,hline_xmax)
            hsegments_int_val.update({hline_y_frac:hsegments_frac_val})
            hsegments.update({hline_y_int:hsegments_int_val})
        else:    
            hsegments_frac_val = DoublyLinkedList()
            hsegments_frac_val.insert_in_empty(new_segment)
            hsegments_int_val.update({hline_y_frac:hsegments_frac_val})
            hsegments.update({hline_y_int:hsegments_int_val})
    else: 
        hsegments_frac_val = DoublyLinkedList()
        hsegments_frac_val.insert_in_empty(new_segment)
        hsegments_int_val ={hline_y_frac:hsegments_frac_val}       
        hsegments.update({hline_y_int:hsegments_int_val})                                
    return hsegments   

# here we update a tree of vertical segments  
def update_vsegments(vsegments,vline_x_int,vline_x_frac,vline_ymin, vline_ymax):
    new_segment=(vline_ymin,vline_ymax)
    vsegments_int_val=vsegments.get(vline_x_int)
    if vsegments_int_val is not None: 
        vsegments_frac_val=vsegments_int_val.get(vline_x_frac)
        if vsegments_frac_val is not None:            
            insert_segment_main(vsegments_frac_val,vsegments_frac_val.head,vline_ymin,vline_ymax)
            vsegments_int_val.update({vline_x_frac:vsegments_frac_val})
            vsegments.update({vline_x_int:vsegments_int_val})
        else:    
            vsegments_frac_val = DoublyLinkedList()
            vsegments_frac_val.insert_in_empty(new_segment)
            vsegments_int_val.update({vline_x_frac:vsegments_frac_val})
            vsegments.update({vline_x_int:vsegments_int_val})
    else: 
        vsegments_frac_val = DoublyLinkedList()
        vsegments_frac_val.insert_in_empty(new_segment)
        vsegments_int_val ={vline_x_frac:vsegments_frac_val}       
        vsegments.update({vline_x_int:vsegments_int_val})                                
    return vsegments   

# here we print the trees of horizontal and vertical segments 
def  display_segments(segments): 
    for int_val in segments.keys(): 
        segments_frac_val=segments.get(int_val)
        for frac_val in segments_frac_val.keys():             
            print(); print("int="+str(int_val)+","+"frac="+str(frac_val)+":")
            segment_list=segments_frac_val.get(frac_val)
            segment_list.display_list(segment_list.head)      
##################################################################
#BLOCK : here use doubly linked list for storing line segments   
##################################################################
# node creation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    def insert_in_empty(self, data):
        new_node = Node(data)
        self.head = new_node
    
    def insert_before(self, next_node, data):
        prev_node = next_node.prev
        new_node = Node(data)
        new_node.next = next_node
        next_node.prev=new_node
         
        if prev_node is None: 
            self.head=new_node
        else:     
            prev_node.next = new_node    
            new_node.prev=prev_node
    
    def insert_after(self, prev_node, data):       
        new_node = Node(data)       
        new_node.next = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node
        
        if new_node.next:
            new_node.next.prev = new_node

    def deleteNode(self, dele):
        if self.head is None or dele is None:
            return
        if self.head == dele:
            self.head = dele.next
        if dele.next is not None:
            dele.next.prev = dele.prev
        if dele.prev is not None:
            dele.prev.next = dele.next

        gc.collect()

    def display_list(self, node):
        while node:
            print(node.data, end="->")
            last = node
            node = node.next
        
# insert a new line segment in a linked list  
def insert_segment_main(d_linked_list,current_node,new_seg_l,new_seg_r):  
    while True:
        if new_seg_l<current_node.data[0]: 
            insert_right_end(d_linked_list,current_node,new_seg_l,new_seg_r)  
            break
        elif new_seg_l<=current_node.data[1]:
            new_seg_l=current_node.data[0] 
            insert_right_end(d_linked_list,current_node,new_seg_l,new_seg_r) 
            break
        else: 
            if current_node.next is None: 
                d_linked_list.insert_after(current_node,(new_seg_l,new_seg_r))
                break
            else: 
                current_node=current_node.next            
    return d_linked_list 

# auxiliary function for inserting a new line segment in a linked list
def insert_right_end(d_linked_list,current_node,new_seg_l,new_seg_r):
    while True:   
        if new_seg_r<current_node.data[0]: 
            d_linked_list.insert_before(current_node,(new_seg_l,new_seg_r))
            break
        elif new_seg_r<=current_node.data[1]: 
            if new_seg_l<current_node.data[0]:
                current_node.data=(new_seg_l,current_node.data[1])
            break
        else: 
            if current_node.next is None: 
                current_node.data=(new_seg_l,new_seg_r)
                break
            else: 
                d_linked_list.deleteNode(current_node)
                current_node=current_node.next      
    return d_linked_list         
#######################################################################################
# BLOCK : generate new subsegments 
#######################################################################################
# generating a list of new subsegments after inserting a segment (main function)
def gen_list_int_main(segments,line_c_int,line_c_frac,line_min,line_max):
    segments_int_val=segments.get(line_c_int)
    if segments_int_val is not None: 
        segments_frac_val=segments_int_val.get(line_c_frac) 
        if segments_frac_val is not None: 
            list_intervals,left_end_bool,right_end_bool=gen_list_int_core(segments_frac_val.head,line_min,line_max)     
        else:
            list_intervals=[line_min,line_max]
            left_end_bool = True; right_end_bool= True
    else:     
        list_intervals=[line_min,line_max]          
        left_end_bool = True; right_end_bool= True
    
    return list_intervals, left_end_bool, right_end_bool  

# generating a list of new subsegments after inserting a segment (core function)   
def gen_list_int_core(current_node,new_seg_l,new_seg_r):
    list_intervals=[]; left_end_bool=False; right_end_bool=False
    while True: 
        if new_seg_l<current_node.data[0]: 
            list_intervals.append(new_seg_l)
            list_intervals,right_end_bool=gen_list_int_right(current_node, \
                                                             new_seg_l,new_seg_r,list_intervals)  
            left_end_bool=True
            break
        elif new_seg_l<=current_node.data[1]: 
            list_intervals,right_end_bool=gen_list_int_right(current_node, \
                                                             new_seg_l,new_seg_r,list_intervals)  
            break    
        else: 
            if current_node.next is None:
                left_end_bool=True; right_end_bool=True
                list_intervals.append(new_seg_l); list_intervals.append(new_seg_r) 
                break
            else: 
                current_node=current_node.next  
    return list_intervals, left_end_bool, right_end_bool  

# auxiliary function for generating a list of new subsegments after inserting a segment
def gen_list_int_right(current_node,new_seg_l,new_seg_r,list_intervals):
    right_end_bool=False
    while True:
        if new_seg_r<current_node.data[0]: 
            right_end_bool=True
            list_intervals.append(new_seg_r)
            break
        elif new_seg_r<=current_node.data[1]: 
            if new_seg_l<current_node.data[0]:
                list_intervals.append(current_node.data[0])
            break
        else: 
            if new_seg_l<current_node.data[0]:
                list_intervals.append(current_node.data[0])
            list_intervals.append(current_node.data[1])
            if current_node.next is None: 
                list_intervals.append(new_seg_r)
                right_end_bool=True
                break
            else: 
                current_node=current_node.next      
    return list_intervals, right_end_bool         

#######################################################################################
# BLOCK : generate new subsegments 
#######################################################################################
# here we list only basis functions with integer knots  
def knots_int(list_intervals,left_end_bool,right_end_bool,line_type,hcells,vcells,line_c_int,line_c_frac,div):
    list_knots_int=[]; left_end_int=list_intervals[0]; right_end_int=list_intervals[-1]  
    if line_type==0: 
        m=hcells; n=vcells  
    else: 
        m=vcells; n=hcells

    if left_end_bool==True: 
        leftmost_knot=left_end_int
    else: 
        leftmost_knot=max(left_end_int-3,0)
    
    if right_end_bool==True:  
        rightmost_knot=right_end_int-4     
    else: 
        rightmost_knot=min(right_end_int-1,m-4)
    
    left_knot=leftmost_knot; L=len(list_intervals)    
    for i in range(0,L-2,2):
        while left_knot<=list_intervals[i+1]-1:
            tuple = tuple_knots_int(left_knot,line_type,n,line_c_int,line_c_frac,div)
            list_knots_int.append(tuple)
            left_knot=left_knot+1  
        left_knot=max(left_knot,list_intervals[i+2]-3)
    while left_knot<=rightmost_knot:
        tuple = tuple_knots_int(left_knot,line_type,n,line_c_int,line_c_frac,div)
        list_knots_int.append(tuple)
        left_knot=left_knot+1 
    
    return list_knots_int

# here we form a knot tuple for knots_int 
def tuple_knots_int(left_knot,line_type,n,line_c_int,line_c_frac,div): 
    tuple_one = (left_knot,left_knot+1,left_knot+2,left_knot+3,left_knot+4)
    if line_c_int==0: 
        tuple_two=(0,line_c_int+line_c_frac/div,1,2,3)
    elif line_c_int==n-1: 
        tuple_two=(n-3,n-2,n-1,line_c_int+line_c_frac/div,n)    
    else: 
        tuple_two=(line_c_int-1,line_c_int,line_c_int+line_c_frac/div,line_c_int+1,line_c_int+2)
    
    if line_type == 0: 
        tuple = (tuple_one,tuple_two)
    else:           
        tuple = (tuple_two,tuple_one)

    return tuple 

# here we list only basis functions with one noninteger knots
def knots_nonint(segments,list_intervals,left_end_bool,right_end_bool,line_c_int,line_c_frac,div,div2,line_type,\
                 hcells,vcells):
    list_knots_nonint=[]; left_end_int=list_intervals[0]; right_end_int=list_intervals[-1]-1  
    
    if left_end_bool==True: 
        tuple_one_list=[left_end_int,"blank",left_end_int+1,left_end_int+2,left_end_int+3]; blank_ind=2
                
        gen_knots(segments,left_end_int,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,list_knots_nonint,\
        line_type)
    else: 
        
        if (line_type==0) and (left_end_int<hcells-1): 
            tuple_one_list=[left_end_int-1,left_end_int,"blank",left_end_int+1,left_end_int+2]; blank_ind=3
        if (line_type==0) and (left_end_int==hcells-1):
            tuple_one_list=[left_end_int-2,left_end_int-1,left_end_int,"blank",left_end_int+1]; blank_ind=4
        
        if (line_type==1) and (left_end_int<vcells-1):
            tuple_one_list=[left_end_int-1,left_end_int,"blank",left_end_int+1,left_end_int+2]; blank_ind=3
        if (line_type==1) and (left_end_int==vcells-1):
            tuple_one_list=[left_end_int-2,left_end_int-1,left_end_int,"blank",left_end_int+1]; blank_ind=4 
        
        gen_knots(segments,left_end_int,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,list_knots_nonint,\
        line_type)

    mid_knot=left_end_int+1; L=len(list_intervals)
    for i in range(0,L-2,2):
        while mid_knot<=list_intervals[i+1]-1:
            tuple_one_list=[mid_knot-1,mid_knot,"blank",mid_knot+1,mid_knot+2]; blank_ind=3
                      
            gen_knots(segments,mid_knot,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,list_knots_nonint,\
            line_type)
            mid_knot=mid_knot+1  
        mid_knot=list_intervals[i+2]
    
    while mid_knot<=right_end_int-1:
        tuple_one_list=[mid_knot-1,mid_knot,"blank",mid_knot+1,mid_knot+2]; blank_ind=3
                 
        gen_knots(segments,mid_knot,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,list_knots_nonint,\
        line_type)
        mid_knot=mid_knot+1
    
    if right_end_bool==True:  
        tuple_one_list=[right_end_int-2,right_end_int-1,right_end_int,"blank",right_end_int+1]; blank_ind=4
        gen_knots(segments,right_end_int,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,\
        list_knots_nonint,line_type)     
    else: 
        tuple_one_list=[right_end_int-1,right_end_int,"blank",right_end_int+1,right_end_int+2]; blank_ind=3
        gen_knots(segments,right_end_int,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,\
        list_knots_nonint,line_type)

    return list_knots_nonint 

def form_tuple(tuple_one,tuple_two,line_type):
    if line_type==0: 
        tuple = (tuple_one,tuple_two) 
    else:  
        tuple  = (tuple_two,tuple_one)
    return tuple 

# get lists of segments from index and return knots if there exist intersections  
def gen_knots(segments,index,line_c_int,line_c_frac,div,div2,tuple_one_list,blank_ind,list_knots_nonint,line_type):
    segments_int_val=segments.get(index)
    if segments_int_val is not None: 
        for key_frac_val in segments_int_val.keys(): 
            segments_frac_val=segments_int_val.get(key_frac_val)
            tuple_two = find_intersection(segments_frac_val.head,line_c_int,line_c_frac,div) 
            if tuple_two is not None:
        
                tuple_one_list[blank_ind-1]=index+key_frac_val/div2  
                tuple_one=tuple(tuple_one_list) 
                                
                tuple_merged = form_tuple(tuple_one,tuple_two,line_type)  
                list_knots_nonint.append(tuple_merged)
    
    return list_knots_nonint     

# find the intersection of two lines
def find_intersection(current_node,line_c_int,line_c_frac,div):    
    while current_node is not None:
        if line_c_int<current_node.data[0]:
            return None 
        elif line_c_int<current_node.data[1]: 
            tuple=find_knots(current_node.data[0],current_node.data[1],line_c_int,line_c_frac,div)
            return tuple
        else:   
            current_node=current_node.next
    return None

# find the knots for the intersection 
def find_knots(left_end,right_end,line_c_int,line_c_frac,div): 
    if line_c_int==left_end: 
        return (line_c_int,line_c_int+line_c_frac/div,line_c_int+1,line_c_int+2,line_c_int+3)
    elif line_c_int==right_end-1: 
        return (line_c_int-2,line_c_int-1,line_c_int,line_c_int+line_c_frac/div,line_c_int+1)    
    else: 
        return (line_c_int-1,line_c_int,line_c_int+line_c_frac/div,line_c_int+1,line_c_int+2)

#####################################################################
#BLOCK: here we print the final list of knots of basis functions 
#####################################################################
def print_basis_knots(list_knots):     
    
    for list_knots_tuple in list_knots:  
        print(list_knots_tuple)       

##########################################################################
#BLOCK: here we draw a spline from the list of knots 
##########################################################################
def add_bspline2d(z,knotx,knoty,cell_div):  
    left_x = knotx[0]; right_x = knotx[4]; bottom_y=knoty[0]; top_y=knoty[4]
    a = BSpline.basis_element(knotx,extrapolate=False)
    b = BSpline.basis_element(knoty,extrapolate=False)    
    for i in range(left_x,right_x):
        for j in range(bottom_y,top_y):
            for k in range(0,cell_div): 
                for m in range(0,cell_div): 
                    z[i*cell_div+k,j*cell_div+m] = z[i*cell_div+k,j*cell_div+m] + a(i + k/cell_div)*b(j + m/cell_div)
    
    return z
   
def draw_spline(list_knots,hcells,vcells): 
    cell_div=5

    hsize = hcells*cell_div+1; vsize = vcells*cell_div+1
    hsize_complex = (hcells*cell_div+1)*1j; vsize_complex = (vcells*cell_div+1)*1j 

    # get points for a mesh grid
    z = np.zeros((hsize,vsize))

    x, y = np.mgrid[0:hcells:hsize_complex, 0:vcells:vsize_complex] 

    for list_knot_tuple in list_knots: 
        knotx = list(list_knot_tuple[0]); knoty = list(list_knot_tuple[1]) 
        z = add_bspline2d(z,knotx,knoty,cell_div) 

    # create a new figure for plotting
    fig = plt.figure()
    
    # create a new subplot on our figure
    spline_fig = fig.add_subplot(projection='3d')

    # plotting the curve
    spline_fig.plot_wireframe(x, y, z, rstride = 1, cstride = 1, linewidth = 1)
    
    plt.show()

##########################################################################
#BLOCK: main program 
##########################################################################

# polynomial degree is equal to 3  - it is fixed! 
poldegree=3
# here we define the number of horizontal and vertical cells 
hcells=15;  vcells=15 
# here we define in how many parts we divide a cell horizontally and vertically  
hdiv=10;  vdiv=10    
# number of lines dropped on a grid
nlines=100


# in the following array we will store the knots of the B-spline basis functions
list_knots =[] 

# here we randomly generate lines that we "drop" on a mesh   
Lines = generate_hv_lines(hcells,vcells,hdiv,vdiv,poldegree,nlines)

##################################################
#Test 1: 
# Lines = [(0,3,1,2,12),(1,2,6,1,9),(1,4,4,2,7),(0,5,7,0,11),(1,8,3,3,11),(0,6,2,1,12),(0,8,3,2,14)]
##################################################
# Test 2: Lines=[(0,3,1,7,14),(1,2,6,1,9),(0,5,2,1,15),(0,3,3,1,15)]
##################################################
#Test 3: 
#Lines=[(0,3,1,8,14),(0,3,1,8,15)]
#######################

draw_mesh(hcells,vcells,Lines,hdiv,vdiv) # here we draw a mesh

hsegments={}; vsegments={}

for Lines_tuple in Lines:  
    
    if Lines_tuple[0]==0:
        hline_y_int=Lines_tuple[1];hline_y_frac=Lines_tuple[2];hline_xmin=Lines_tuple[3];hline_xmax=Lines_tuple[4]
         
        list_intervals,left_end_bool,right_end_bool= gen_list_int_main(hsegments,hline_y_int,hline_y_frac,hline_xmin,\
                                                                       hline_xmax)      
            
        if list_intervals: 
            list_knots_int=knots_int(list_intervals,left_end_bool,right_end_bool,0,hcells,vcells,hline_y_int,\
                                     hline_y_frac,vdiv) 

            list_knots_nonint=knots_nonint(vsegments,list_intervals,left_end_bool,right_end_bool,hline_y_int,\
                                           hline_y_frac,vdiv,hdiv,0,hcells,vcells)
            
            list_knots = list_knots +  list_knots_int + list_knots_nonint # here we update list_knots

            update_hsegments(hsegments,hline_y_int,hline_y_frac,hline_xmin, hline_xmax)
    else: 
        vline_x_int=Lines_tuple[1];vline_x_frac=Lines_tuple[2];vline_ymin=Lines_tuple[3];vline_ymax=Lines_tuple[4]

        list_intervals,left_end_bool,right_end_bool= gen_list_int_main(vsegments,vline_x_int,vline_x_frac,\
                                                                       vline_ymin,vline_ymax)      
                   
        if list_intervals:
            list_knots_int=knots_int(list_intervals,left_end_bool,right_end_bool,1,hcells,vcells,vline_x_int,\
                                     vline_x_frac,hdiv) 

            list_knots_nonint=knots_nonint(hsegments,list_intervals,left_end_bool,right_end_bool,vline_x_int,\
                                           vline_x_frac,hdiv,vdiv,1,hcells,vcells)

            list_knots = list_knots +  list_knots_int + list_knots_nonint # here we update list_knots
            
            update_vsegments(vsegments,vline_x_int,vline_x_frac,vline_ymin,vline_ymax)    
        
    
print_basis_knots(list_knots) # here we print a list of knots  
print("The number of new added basis functions:",len(list_knots)) # here we print a total number of new basis functions 
draw_spline(list_knots,hcells,vcells) # here we draw a spline 
 
