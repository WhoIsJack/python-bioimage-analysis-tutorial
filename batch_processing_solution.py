
# coding: utf-8

# Image Analysis with Python - Solution for Batch Processing

# The following is the script version of the tutorial's solution pipeline, where all the code
# has been wrapped in a single function that can be called many times for many images.
# Please refer to the jupyter notebooks ('image_analysis_tutorial[_solutions].ipynb') for 
# more information, including detailed comments on every step.


## Importing Modules & Packages

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi


## Defining the pipeline function
def run_pipeline(dirpath, filename):
    """Run 2D single-cell segmentation pipeline optimized for membrane-labeled
    spinning-disk confocal images of membrane markers in zebrafish early embryos.
    
    Parameters
    ----------
    dirpath : string
        Path to the directory containing the input image.
    filename : string
        Name of the input file, including file ending (should be .tif).
    
    Returns
    -------
    clean_ws : 3D numpy array of same shape as input image
        The single-cell segmentation. Every cell is labeled with a unique
        integer ID. Background is 0.
    results : dict
        A number of measurements extracted from each cell. The dict keys 
        name the type of measurement. The dict values are lists containing
        the measured values. The order of all lists is the same and relates
        to the segmentation IDs through the list in results['cell_id'].
    """


    ## Importing & Handling Image Data

    from os.path import join
    filepath = join(dirpath, filename)

    from skimage.io import imread
    img = imread(filepath)


    ## Preprocessing

    sigma = 3
    img_smooth = ndi.filters.gaussian_filter(img, sigma)


    ## Adaptive Thresholding

    i = 31
    SE = (np.mgrid[:i,:i][0] - np.floor(i/2))**2 + (np.mgrid[:i,:i][1] - np.floor(i/2))**2 <= np.floor(i/2)**2

    from skimage.filters import rank 
    bg = rank.mean(img_smooth, selem=SE)

    mem = img_smooth > bg


    ## Improving Masks with Binary Morphology

    mem_holefilled = ~ndi.binary_fill_holes(~mem) # Short form

    i = 15
    SE = (np.mgrid[:i,:i][0] - np.floor(i/2))**2 + (np.mgrid[:i,:i][1] - np.floor(i/2))**2 <= np.floor(i/2)**2

    pad_size = i+1
    mem_padded = np.pad(mem_holefilled, pad_size, mode='reflect')
    mem_final = ndi.binary_closing(mem_padded, structure=SE)
    mem_final = mem_final[pad_size:-pad_size, pad_size:-pad_size]


    ## Cell Segmentation by Seeding & Expansion

    ### Seeding by Distance Transform

    dist_trans = ndi.distance_transform_edt(~mem_final)
    dist_trans_smooth = ndi.filters.gaussian_filter(dist_trans, sigma=5)

    from skimage.feature import peak_local_max
    seeds = peak_local_max(dist_trans_smooth, indices=False, min_distance=10)

    seeds_labeled = ndi.label(seeds)[0]

    ### Expansion by Watershed

    from skimage.morphology import watershed
    ws = watershed(img_smooth, seeds_labeled)


    ## Postprocessing: Removing Cells at the Image Border

    border_mask = np.zeros(ws.shape, dtype=np.bool)
    border_mask = ndi.binary_dilation(border_mask, border_value=1)

    clean_ws = np.copy(ws)

    for cell_ID in np.unique(ws):
        cell_mask = ws==cell_ID
        cell_border_overlap = np.logical_and(cell_mask, border_mask)
        total_overlap_pixels = np.sum(cell_border_overlap)
        if total_overlap_pixels > 0: 
            clean_ws[cell_mask] = 0

    for new_ID, cell_ID in enumerate(np.unique(clean_ws)[1:]): 
        clean_ws[clean_ws==cell_ID] = new_ID+1


    ## Identifying Cell Edges

    edges = np.zeros_like(clean_ws)

    for cell_ID in np.unique(clean_ws)[1:]:
        cell_mask = clean_ws==cell_ID
        eroded_cell_mask = ndi.binary_erosion(cell_mask, iterations=1)
        edge_mask = np.logical_xor(cell_mask, eroded_cell_mask)
        edges[edge_mask] = cell_ID


    ## Extracting Quantitative Measurements

    results = {"cell_id"      : [],
               "int_mean"     : [],
               "int_mem_mean" : [],
               "cell_area"    : [],
               "cell_edge"    : []}

    for cell_id in np.unique(clean_ws)[1:]:
        cell_mask = clean_ws==cell_id
        edge_mask = edges==cell_id
        results["cell_id"].append(cell_id)
        results["int_mean"].append(np.mean(img[cell_mask]))
        results["int_mem_mean"].append(np.mean(img[edge_mask]))
        results["cell_area"].append(np.sum(cell_mask))
        results["cell_edge"].append(np.sum(edge_mask))

        
    ## Returning the results
    return clean_ws, results

