import gc

################################################
# my modules 
################################################
import draw_mesh_module
import line_generator_module
import record_lines_module
import record_knots_module
import draw_spline_module
################################################


###############################################################################
#BLOCK : here we update a tree of segments
###############################################################################

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
#BLOCK : here we use doubly linked list for storing line segments   
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
###############################################################################
# BLOCK : generate new subsegments 
###############################################################################
#generating a list of new subsegments after inserting a segment (main function)
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
nlines=10

# here we randomly generate lines that are "dropped" on a mesh   
Lines = line_generator_module.generate_hv_lines(hcells,vcells,hdiv,vdiv,
                                                poldegree,nlines)

# here we record generated lines in a text file 
record_lines_module.save_lines(Lines)

# here we draw a mesh
draw_mesh_module.draw_mesh(hcells,vcells,Lines,hdiv,vdiv) 

# in this array we will store the knots of the B-spline basis functions
list_knots =[] 

# in these dictionaries we will store horizontal/vertical segments
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
        
# here we save a list of knots in a file    
record_knots_module.save_knots(list_knots)   

# here we draw a spline
draw_spline_module.draw_spline(list_knots,hcells,vcells)  
 
