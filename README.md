Python BioImage Analysis Tutorial
=================================

*originally created in 2016*    
*updated and converted to a Jupyter notebook in 2017*    
*updated and converted to python 3 in 2018*    
*by Jonas Hartmann (Gilmour group, EMBL Heidelberg)*    

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/WhoIsJack/python-bioimage-analysis-tutorial/master)

## Aims and Overview

This tutorial teaches the basics of bio-image processing, segmentation and analysis in python. It integrates explanations and exercises in a (hopefully) self-explanatory fashion, enabling participants to build their own image analysis pipelines step by step.

The tutorial uses single-cell segmentation of 2D confocal fluorescence microscopy images to illustrate key concepts from preprocessing to segmentation to (very basic) data analysis. It concludes with a small section on how to apply such a pipeline to multiple images at once (batch processing).

Everything you need to know to get started can be found in the jupyter notebook [`image_analysis_tutorial.ipynb`](image_analysis_tutorial.ipynb). To find out more about how to run these materials interactively, see the [Jupyter documentation](https://jupyter.readthedocs.io/en/latest/index.html).

Note that this tutorial was part of a course aimed at people with basic knowledge of python. The course included introductory sessions/lectures on scientific python (in particular `numpy` and `matplotlib`) as well as on image analysis (see the slides in this repository). For those tackling this tutorial on their own, it is therefore recommended to first acquire basic scientific python knowledge elsewhere (e.g. at [python-course.eu](https://www.python-course.eu)).


## Content Overview

- Lecture
    - Working with digital images
        - Images as arrays of numbers
        - Look-up tables (LUTs)
        - Dimensions
        - Bit-depth
    - Image analysis pipelines
        - Preprocessing: filters, kernels, convolution, background subtraction
        - Foreground detection: thresholding, morphological operations
        - Segmentation: labels, seeds, watershed
        - Postprocessing: object filtering
        - Making measurements


- Tutorial
    - Importing Modules & Packages
    - Loading & Handling Image Data
    - Preprocessing
    - Manual Thresholding & Threshold Detection
    - Adaptive Thresholding
    - Improving Masks with Binary Morphology
    - Connected Components Labeling
    - Cell Segmentation by Seeding & Expansion
    - Postprocessing: Removing Cells at the Image Border
    - Identifying Cell Edges
    - Extracting Quantitative Measurements
    - Simple Analysis & Visualization
    - Writing Output to Files
    - Batch Processing


## Old Versions and Other Sources

This was part of the EMBL Bio-IT/ALMF `Image Analysis with Python 2018` course (see the [EMBL Gitlab repo](https://git.embl.de/grp-bio-it/image-analysis-with-python-2018)).

If you are looking for the python 2 version from 2017, see the `2017_legacy_python_version` branch or the corresponding [EMBL GitLab repo](https://git.embl.de/grp-bio-it/python-workshop-image-processing).

The original 2016 materials can be found in Karin Sasaki's corresponding Github [repo](https://github.com/karinsasaki/python-workshop-image-processing).


## Acknowledgements

The first version of this tutorial was created for the `EMBL Python Workshop - Image Processing` course organized by Karin Sasaki and Jonas Hartmann in 2016. Additional lecturers and TAs contributing to this course were Kota Miura, Volker Hilsenstein, Aliaksandr Halavatyi, Imre Gaspar, and Toby Hodges.

The second installment (the `EMBL Bio-IT Image Processing Course`, 2017) was organized and taught by Jonas Hartmann and Toby Hodges.

The third version of this tutorial was part of the `EMBL Bio-IT/ALMF Image Analysis with Python 2018` course, organized by Jonas Hartmann and Toby Hodges in collaboration with Tobias Rasse and Volker Hilsenstein. Additional organizational help came from Christian Tischer and Malvika Sharan.

Many thanks to all the helpful collaborators and the interested students who were instrumental in making these courses a success.


## Feedback

Feedback on this tutorial is always welcome! Please open an issue on GitHub or write to *jonas.hartmann_at_embl.de*.
