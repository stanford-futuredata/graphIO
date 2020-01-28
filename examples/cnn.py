import numpy as np
import sys
sys.path.append('..')
import core.solver  as solver
from core.eig_solver import compute_eigenvalue_bound
import torch

def alltogether_matsum(mat):
    return solver.genop(mat.flatten(), np.sum)

def convolution(image, filt, s=1, alltogether=False):
    '''
    Confolves `filt` over `image` using stride `s`
    '''
    (n_f, n_c_f, f, _) = filt.shape # filter dimensions
    n_c, in_dim, _ = image.shape # image dimensions
    
    out_dim = int((in_dim - f)/s)+1 # calculate output dimensions
    
    assert n_c == n_c_f, "Dimensions of filter must match dimensions of input image"
    
    out = []
    
    # convolve the filter over every part of the image, adding the bias at each step. 
    for curr_f in range(n_f):
        curr_y = out_y = 0
        while curr_y + f <= in_dim:
            curr_x = out_x = 0
            while curr_x + f <= in_dim:
                current_filter = filt[curr_f]
                image_slice = image[:,curr_y:curr_y+f, curr_x:curr_x+f]
                if alltogether:
                    out.append(alltogether_matsum(current_filter * image_slice))
                else:
                    out.append(np.sum(current_filter * image_slice))
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
    return out

def conv_test(k, nout, n, nin, s):
    a = np.array(solver.transform_array([1 for i in range(nin*nout*k**2)])).reshape(nout, nin, k,k)
    b = np.array(solver.transform_array([1 for i in range(nin*n**2)])).reshape(nin, n,n)
    convolution(image=b, filt=a, s=s)