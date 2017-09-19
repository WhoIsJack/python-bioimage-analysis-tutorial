# coding: utf-8
"""
@author:    Jonas Hartmann @ Gilmour group @ EMBL Heidelberg

@descript:  This is the 'batch' version of the tutorial pipeline solutions.
            It was exported from the jupyter notebook and then modified so it
            can be used for batch processing.
"""

# SETUP AND IMPORTS
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi


#------------------------------------------------------------------------------

# PIPELINE FUNCTION

def run_pipeline(filename):

    # Report
    print '\nWORKING ON IMAGE:', filename

    #--------------------------------------------------------------------------


    # IMPORTING & HANDLING IMAGE DATA

    ## (i) Specify the filename
    #filename = r'/home/jack/data/example_cells_1.tif'
    #filename = 'example_cells_1.tif'   # XXX: DELETME!

    # (ii) Load the image
    from tifffile import imread
    img = imread(filename)

    # (iii) Check that everything is in order
    print "Loaded array is of type:", type(img)
    print "Loaded array has shape:", img.shape
    print "Loaded values are of type:", img.dtype

    # (iv) Allocate the green channel to a separate new variable
    green = img[0,:,:]

    ## (v) Look at the image to confirm that everything worked as intended
    #plt.figure(figsize=(7,7))
    #plt.imshow(green,interpolation='none',cmap='gray')
    #plt.show()


    # PREPROCESSING: GAUSSIAN SMOOTHING

    # (i) Create a variable for the smoothing factor sigma, which should be an integer value
    sigma = 3

    # (ii) Perform the smoothing on the image
    green_smooth = ndi.filters.gaussian_filter(green,sigma)

    ## (iii) Visualize the result using plt.imshow and plt.show
    #plt.figure(figsize=(7,7))
    #plt.imshow(green_smooth,interpolation='none',cmap='gray')
    #plt.show()


    # PREPROCESSING: ADAPTIVE THRESHOLDING - STEP 1

    # (i) Create a disk-shaped structuring element and asign it to a new variable.
    i = 31
    struct = (np.mgrid[:i,:i][0] - np.floor(i/2))**2 + (np.mgrid[:i,:i][1] - np.floor(i/2))**2 <= np.floor(i/2)**2
    #plt.imshow(struct,interpolation='none')
    #plt.show()

    # (ii) Create the background
    from skimage.filters import rank
    bg = rank.mean(green_smooth, selem=struct)

    ## (iii) Visualize the resulting background image
    #plt.figure(figsize=(7,7))
    #plt.imshow(green_smooth,interpolation='none',cmap='gray')
    #plt.show()


    # PREPROCESSING: ADAPTIVE THRESHOLDING - STEP 1

    # (iv) Threshold the Gaussian-smoothed original image using the background
    #      image created in step 1 to obtain the cell membrane segmentation
    green_mem = green_smooth >= bg

    ## (v) Visualize and understand the output.
    #plt.figure(figsize=(7,7))
    #plt.imshow(green_mem,interpolation='none',cmap='gray')
    #plt.show()


    # IMPROVING MASKS WITH BINARY MORPHOLOGY

    # (i) Get rid of speckles using binary hole filling
    green_mem_holes_filled = ndi.binary_fill_holes(np.logical_not(green_mem))

    # (ii) Try out other morphological operations to further improve the membrane mask
    i = 15
    struct = (np.mgrid[:i,:i][0] - np.floor(i/2))**2 + (np.mgrid[:i,:i][1] - np.floor(i/2))**2 <= np.floor(i/2)**2
    pad_size = i+1
    padded_mem = np.pad(green_mem_holes_filled,pad_size,mode='reflect')
    mem_final = ndi.binary_closing(np.logical_not(padded_mem),structure=struct)
    mem_final = mem_final[pad_size:-pad_size,pad_size:-pad_size]

    ## (iii) Visualize the final result
    #plt.figure(figsize=(7,7))
    #plt.imshow(mem_final,interpolation='none',cmap='gray')
    #plt.show()


    # CONNECTED COMPONENTS LABELING

    # (i) Label connected components
    mem_final = np.logical_not(mem_final)
    cell_labels,_ = ndi.label(mem_final)

    ## (ii) Visualize the output
    #plt.figure(figsize=(7,7))
    #plt.imshow(np.zeros_like(cell_labels))
    #plt.imshow(cell_labels,interpolation='none',cmap='inferno')
    #plt.show()


    # CELL SEGMENTATION BY SEEDING & EXPANSION - SEEDING BY DISTANCE TRANSFORM

    # (i) Distance transform on thresholded membranes
    dist_trans = ndi.distance_transform_edt(mem_final)

    ## (ii) Visualize the output and understand what you are seeing.
    #plt.figure(figsize=(7,7))
    #plt.imshow(dist_trans,interpolation='none',cmap='viridis')
    #plt.show()

    # (iii) Dilate the distance threshold
    i = 10
    struct = (np.mgrid[:i,:i][0] - np.floor(i/2))**2 + (np.mgrid[:i,:i][1] - np.floor(i/2))**2 <= np.floor(i/2)**2
    dist_trans_dil = ndi.filters.maximum_filter(dist_trans, footprint=struct)

    # (iv) Retrieve the local maxima (the 'peaks') in the distance transform
    from skimage.feature import peak_local_max
    seeds = peak_local_max(dist_trans_dil, indices=False, min_distance=10)

    ## (v) Visualize the output as an overlay on the original (smoothed) image
    #plt.figure(figsize=(7,7))
    #plt.imshow(green_smooth, interpolation='none', cmap='gray')
    #plt.imshow(np.ma.array(seeds,mask=seeds==0),interpolation='none',cmap='autumn')
    #plt.show()

    # (vi) Optimize the seeding

    # (vii) Label the seeds
    seeds_labeled = ndi.label(seeds)[0]


    # CELL SEGMENTATION BY SEEDING & EXPANSION - EXPANSION BY WATERSHED

    # (i) Perform watershed
    from skimage.morphology import watershed
    ws = watershed(green_smooth,seeds_labeled)

    ## (ii) Show the result as transparent overlay over the smoothed input image
    #plt.figure(figsize=(7,7))
    #plt.imshow(green_smooth, interpolation='none', cmap='gray')
    #plt.imshow(ws,interpolation='none',cmap='prism',alpha=0.4)
    #plt.show()


    # POSTPROCESSING: REMOVING CELLS AT THE IMAGE BORDER

    # (i) Create image border mask
    boundary_mask = np.ones(ws.shape,dtype=np.bool)
    boundary_mask = np.logical_not(ndi.binary_erosion(boundary_mask,border_value=0))

    # (ii) 'Delete' the cells at the border:
    clean_ws = np.copy(ws)

    # Iterate over all cells in the segmentation
    for cell_ID in np.unique(ws):

        # Create a mask that contains only the 'current' cell in the iteration
        cell_mask = ws==cell_ID

        # Using the cell mask and the border mask from above, test if the cell has pixels touching
        cell_boundary_overlap = np.logical_and(cell_mask,boundary_mask)   # Overlap of cell mask and boundary mask
        total_overlapping_pixels = np.sum(cell_boundary_overlap)          # Sum overlapping pixels

        # If a cell touches the image boundary, delete it by setting its pixels in the segmentation to 0.
        if total_overlapping_pixels > 0:
            clean_ws[cell_mask] = 0

    # OPTIONAL: re-label the remaining cells to keep the numbering consistant from 1 to N (with 0 as background).
    for new_ID,cell_ID in enumerate(np.unique(clean_ws)[1:]):  # The [1:] excludes 0 from the list (background)!
        clean_ws[clean_ws==cell_ID] = new_ID+1                 # The same here for the +1

    ## (iii) Visualize the result
    #plt.figure(figsize=(7,7))
    #plt.imshow(green_smooth, interpolation='none', cmap='gray')
    #plt.imshow(np.ma.array(clean_ws,mask=clean_ws==0),interpolation='none',cmap='prism',alpha=0.4)
    #plt.show()


    # IDENTIFYING CELL EDGES

    # (i) Create an empty array of the same size and data type as the segmentation
    edges = np.zeros_like(clean_ws)


    # (ii) Iterate over the cells
    for cell_ID in np.unique(clean_ws)[1:]:

        # (iii) Erode the cell's mask by 1 pixel
        cell_mask = clean_ws==cell_ID
        eroded_cell_mask = ndi.binary_erosion(cell_mask)

        # (iv) Create cell edge mask
        edge_mask = np.logical_xor(cell_mask,eroded_cell_mask)

        # (v) Add the cell edge mask to the empty array generated above,
        # labeling it with the cell's ID
        edges[edge_mask] = cell_ID

    ## (vi) Visualize the result
    #plt.figure(figsize=(7,7))
    #plt.imshow(np.zeros_like(edges),cmap='gray',vmin=0,vmax=1)  # Black background
    #plt.imshow(np.ma.array(edges,mask=edges==0),interpolation='none',cmap='prism')
    #plt.xlim((300,500))
    #plt.ylim((300,500))
    #plt.show()


    # EXTRACTING QUANTITATIVE MEASUREMENTS

    # (i) Create a dictionary that contains a key-value pairing for each measurement
    results = {"cell_id":[],
               "green_mean":[],
               "red_mean":[],
               "green_mem_mean":[],
               "red_mem_mean":[],
               "cell_area":[],
               "cell_edge":[]}

    # (ii) Record the measurements for each cell

    # Iterate over cell IDs
    for cell_id in np.unique(clean_ws)[1:]:

        # Mask the current cell and cell edge
        cell_mask = clean_ws==cell_id
        edge_mask = edges==cell_id

        # Get the measurements
        results["cell_id"].append(cell_id)
        results["green_mean"].append(np.mean(img[0,cell_mask]))
        results["red_mean"  ].append(np.mean(img[1,cell_mask]))
        results["green_mem_mean"].append(np.mean(img[0,edge_mask]))
        results["red_mem_mean"  ].append(np.mean(img[1,edge_mask]))
        results["cell_area"].append(np.sum(cell_mask))
        results["cell_edge"].append(np.sum(edge_mask))

    ## (iii) Print the results and check that they make sense
    #for key in results.keys(): print key, '\n', results[key], '\n'


    #--------------------------------------------------------------------------

    # RETURN OUTPUT

    return clean_ws, results

#------------------------------------------------------------------------------




