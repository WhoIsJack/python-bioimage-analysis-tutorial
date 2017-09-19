Python Workshop - Image Processing
==================================

*(This is a clone of the corresponding [EMBL GitLab repo](https://git.embl.de/grp-bio-it/python-workshop-image-processing))*


## Course Aims and Overview

This course teaches the basics of bio-image processing, segmentation and analysis in python. It is based on tutorials that integrate explanations and exercises, enabling participants to build their own image analysis pipeline step by step.

All material is provided as Jupyter notebooks. To find out more about how to run these materials interactively, see the [Jupyter documentation](https://jupyter.readthedocs.io/en/latest/index.html).

The [`main_tutorial`](./main_tutorial/) uses single-cell segmentation of a confocal fluorescence microscopy image to illustrate key concepts from preprocessing to segmentation to data analysis. It includes a tutorial on how to apply such a pipeline to multiple images at once (batch processing).

The main tutorial is complemented by the [`pre_tutorial`](./pre_tutorial/) content, which provides some basics of Jupyter, `matplotlib` and an introduction to `numpy` and working with arrays.

This course is aimed at people with basic to intermediate knowledge of python and basic knowledge of microscopy. For people with basic knowledge of image processing, the tutorials can be followed without attending the lectures.


## Instructions on following this course

- If you have only very basic knowledge of python or if you are feeling a little rusty, you should start with the `pre_tutorial`, which includes two notebooks: one on `numpy` arrays and one on the basics of Jupyter and `matplotlib`. If you are more experienced, you may want to skim or skip the pre-tutorial.


- In the `main_tutorial`, it is recommended to follow the `tutorial_pipeline` first. By following the exercises, you should be able to implement your own segmentation pipeline. If you run into trouble, you can use the provided solutions as inspiration - however, it is *highly* recommended to spend a lot of time figuring things out yourself, as this is an important part of any programming exercise.


## Concepts discussed in course lectures

1. **Introductory Material**
   	* Working with the Jupyter Notebook
	* Importing packages and modules
	* Reading data from files
	* A brief introduction to `matplotlib`
	* Data and variable types
	* An introduction to `numpy`
	* Arrays, indexing, slicing
	* Using the documentation


2. **Basics of Bio-Image Processing**
	* Digital images
		* Images as arrays of numbers
		* Look-up tables (LUTs)
		* Dimensions
		* Bit-depth
	* Image analysis pipelines
		* Preprocessing: filters, kernels, convolution, background subtraction
		* Foreground detection: thresholding, morphological operations
		* Segmentation: labels, seeds, watershed
		* Postprocessing: object filtering
		* Making measurements


3. **Introduction to the Tutorial Pipeline**
	* Automated Single-Cell Segmentation
		* Why? (advantages of single-cell approaches)
		* How? (segmentation pipeline)
		* What? (2D spinning disc confocal fluorescence microscopy images of Zebrafish embryonic cells)
		* Who? (YOU!)


3. **Advanced materials** *[not yet available; may be added later]*
	* What comes after segmentation: downstream data further analysis
	* Code Optimisation (vectorisation, multiprocessing, cluster processing)


## Instructors

- Jonas Hartmann (Gilmour Lab, CBB, EMBL)
- Toby Hodges (Bio-IT, Zeller Team, SCB, EMBL)


## Inspiration

This repository was forked from [Karin Sasaki's materials on GitHub](https://github.com/karinsasaki/python-workshop-image-processing). These materials have been adapted from the original version, written and taught by Karin Sasaki, Jonas Hartmann, Kota Miura, Volker Hinsenstein, Aliaksandr Halavatyi, Imre Gaspar, and Toby Hodges.

## Feedback 

We welcome any feedback on this course! 

Feel free to contact us at *jonas.hartmann@embl.de* or *toby.hodges@embl.de*.
