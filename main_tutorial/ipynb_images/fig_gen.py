# -*- coding: utf-8 -*-
"""
Created on Mon May 01 00:30:59 2017

@author:    Jonas Hartmann @ Gilmour group @ EMBL Heidelberg

@descript:  Quick & dirty script to generate illustrations for the python image
            analysis course's tutorial pipeline.
"""

# IMPORTS

import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt


# GAUSSIAN KERNEL GRID

# Create the Gaussian kernel
a = np.zeros((11,11),dtype=np.uint8)
a[5,5] = 255
a = ndi.gaussian_filter(a,2)

# Generate figure
pig,ax = plt.subplots()
ax.matshow(a,cmap='Blues',vmax=12)

# Add the labels
for (i, j), z in np.ndenumerate(a*10):
    ax.text(j, i, z, ha='center', va='center')

# Cosmetics, saving and showing
plt.axis('off')
#plt.savefig('gaussian_kernel_grid.png')
#plt.show()

# Clean
plt.clf()
plt.close()


# 1D ADAPTIVE THRESHOLDING

# Create 1D 'membrane' data
a = np.zeros(100) + 10
a[35] = 1000
a[65] = 1000
a = ndi.gaussian_filter(a,2)

# Create adaptive background
b = ndi.uniform_filter(a,size=20)

# Plot stuff
plt.plot(a)
plt.plot(b,c='r')
plt.ylim([-10,270])

# Label, save and show
plt.legend(['Raw 1D Membrane Signal','Adaptive Background'])
plt.xlabel('space [pixels]')
plt.ylabel('intensity [a.u.]')
#plt.savefig('adaptive_bg_1D.png')
#plt.show()

# Clean
plt.clf()
plt.close()


# UNIFORM KERNEL WITH STRUCTURING ELEMENT

# Create data
i = 11
a = (np.mgrid[:i+2,:i+2][0] - np.floor(i/2) - 1)**2 + (np.mgrid[:i+2,:i+2][1] - np.floor(i/2) - 1)**2 <= np.floor(i/2)**2

# Generate figure
pig,ax = plt.subplots()
ax.matshow(a,cmap='Blues',vmax=2)

# Add the labels
for (i, j), z in np.ndenumerate(a*1):
    ax.text(j, i, z, ha='center', va='center')

# Cosmetics, saving and showing
plt.axis('off')
#plt.savefig('uniform_filter_SE.png')
#plt.show()

# Clean
plt.clf()
plt.close()


# DISTANCE TRANSFORM

# Create data
a = np.zeros((16,28),dtype=np.uint8)
a[6:10,6:10] = 255
a[6:10,18:22] = 255
a = ndi.gaussian_filter(a,3)
a = a >= 9

# Distance transform
b = ndi.distance_transform_edt(a)

# Generate figure
pig,ax = plt.subplots(1,2)
ax[0].matshow(a,cmap='Blues',vmax=2)
ax[1].matshow(b,cmap='Blues')

# Add the labels
for (i, j), z in np.ndenumerate(a.astype(np.uint8)):
    ax[0].text(j, i, z, ha='center', va='center')
for (i, j), z in np.ndenumerate(b.astype(np.uint8)):
    ax[1].text(j, i, z, ha='center', va='center')

# Cosmetics
ax[0].axis('off')
ax[1].axis('off')
ax[0].set_title('Boolean Mask')
ax[1].set_title('Distance Transform')
plt.tight_layout()

## Saving
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()
#plt.savefig('distance_transform.png')

# Showing
#plt.show()

# Clean
plt.clf()
plt.close()


# WATERSHED 1D ILLUSTRATION

# Create 1D 'membrane' data
a = np.zeros(150,dtype=np.uint8)
a[[25,50,90,125]]  = [150,180,80,120]
a = ndi.gaussian_filter(a,2)
a = (a.astype(np.float) / float(a.max()) * 200.0).astype(np.uint8) + 10

# Create seed data
b = (np.array([10,38,70,110,140]),np.array([10,10,10,10,10]))

# Three watershed steps
w1 = np.ones_like(a) + 70
w2 = np.ones_like(a) + 140
w3 = np.ones_like(a) + 240

# Plotting function
def plot_stuff(ax,l1=None,l2=None):

    # Plot intensity
    ax.plot(a,lw=2,label=l1,color='#6AADD5')
    ax.fill_between(np.arange(a.shape[0]),a,color='#F7FBFF')

    # Plot seeds
    ax.scatter(b[0],b[1],label=l2,color='#C71B11',zorder=3,s=30,marker='D')

    # Cosmetics
    ax.set_ylim([0,255])
    ax.set_xlim([0,149])

    # Done
    return ax

# Make the figure
pig,ax = plt.subplots(2,2,sharex=True,sharey=True)

# Add plot before watershed
ax[0,0] = plot_stuff(ax[0,0],l1='membrane signal',l2='seeds')
ax[0,0].legend()
ax[0,0].set_title("watershed level 0",fontsize=14)

# Add plot with watershed at 70
ax[0,1].fill_between(np.arange(w1.shape[0]),w1,color='#0B559F',
                     label='watershed')
ax[0,1] = plot_stuff(ax[0,1])
ax[0,1].legend()
ax[0,1].set_title("watershed level 70",fontsize=14)

# Add plot with watershed at 140
ax[1,0].fill_between(np.arange(w2.shape[0]),w2,color='#0B559F')
ax[1,0] = plot_stuff(ax[1,0])
ax[1,0].vlines(90,0,255,lw=2,color='#C71B11',zorder=3)
ax[1,0].set_title("watershed level 140",fontsize=14)

# Add plot with watershed at 240
ax[1,1].fill_between(np.arange(w3.shape[0]),w3,color='#0B559F')
ax[1,1] = plot_stuff(ax[1,1])
ax[1,1].vlines([25,50,90,125],0,255,lw=2,color='#C71B11',zorder=3,
               label='final cell boundaries')
ax[1,1].legend()
ax[1,1].set_title("watershed level 240",fontsize=14)

# General labels
pig.text(0.5, 0.02, 'space [pixels]', ha='center', fontsize=14)
pig.text(0.04, 0.5, 'intensity [a.u.]', va='center', rotation='vertical',
         fontsize=14)

## Saving
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()
#plt.savefig('watershed_illustration.png')

# Tighten layout and show
plt.tight_layout()
#plt.show()

# Clean
plt.clf()
plt.close()



