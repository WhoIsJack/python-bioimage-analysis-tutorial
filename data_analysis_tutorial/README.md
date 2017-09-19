# Data Analysis Tutorial

### Description

This tutorial provides an introductory overview of how to approach single-cell analysis following image segmentation. It is intended as "advanced content" for those participants of the course that have completed the main tutorial.

For people with limited experience in data analysis, this tutorial is intended as an inspiration and incentive to think about possible advanced analyses downstream of segmentation. Solving the exercises without help may be difficult, so it may be a good idea to have a look at the solutions to get some idea of how the problems should be approached. However, once the principles are understood, it is an important part of the learning experience to build your own implementation and to play around with different possibilities.

People more experienced in data science can use this tutorial as a starting point for exploring the data analysis packages available in python. It also illustrates that python readily allows the construction of complete and consistent analysis pipelines, from image preprocessing to feature extraction to clustering.

**Warning 1:** These materials were put together relatively quickly and have not been thoroughly double-checked and optimized yet! Any feedback that may help to improve these materials is very welcome!

**Warning 2:** These materials use an example image with a quite uniform population of cells (meaning the cells are in general quite similar). As a consequence, there aren't really any interesting patterns that can be uncovered by data analysis, which is a bit unfortunate for a tutorial on this topic. However, the concepts can still be explained - it's just that the outcome won't be too exciting. We are planning to switch to more interesting example images in the future.


### Requirements

- **Already needed for main tutorial**
    - python 2.7 *(or python 3.x, if you don't mind adjusting the solutions)*
    - numpy
    - scikit-image
    - matplotlib
    - scipy
    - tifffile

- **New for this tutorial**
    - scikit-learn 
    - networkx


### Concepts Discussed in this Tutorial

- Feature extraction
    - Specific features of interest
    - General image descriptors

- Feature space standardization

- Dimensionality reduction
    - PCA
    - tSNE

- Clustering by k-means (including Elbow plots)

- Graph/network-based data representation and visualization


### How to Follow this Tutorial

- Files you should have:
	- data_analysis_tutorial.ipynb
	- example_cells_1_* (four files containing various data from the main tutorial's pipeline)

- The tutorial is more or less self-explanatory but unlike the main tutorial it requires you to figure out most things by yourself. For less experienced participants, it is recommended to work closely with the solutiions, as otherwise it will be tough to get anywhere. However, make sure you understand how the solutions work and play around with the code yourself!

- If you are following this tutorial in class, if you have any questions, raise your hand and someone will come to help you. Otherwise, feel free to send your query to one of these two email addresses:
  - *jonas.hartmann@embl.de*
  - *toby.hodges@embl.de*
