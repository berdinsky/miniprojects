from scipy.interpolate import BSpline
import matplotlib.pyplot as plt
import numpy as np

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