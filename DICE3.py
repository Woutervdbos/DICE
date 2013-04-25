################################  calculate DICE Coefficient of segmentation results FSL
### created by wouter van den bos #  woutervdbos@gmail.com
###
### this script is to perform a quality check between results of fsl probtracks segmentation
### see: http://fsl.fmrib.ox.ac.uk/fsl/fsl-4.1.9/fdt/fdt_probtrackx.html for details
### but can be used on ohter data sets too.
###
### DICE = 2 * A intersection B / |A|+|B|
### http://sve.loni.ucla.edu/instructions/metrics/dice/ for quick summary of DICE
###
### requires installation of nipype, a useful API for several popular imaging toolboxes
### http://nipy.sourceforge.net/nipype/
### also requires Scipy & numpy
### http://www.scipy.org/ & http://www.numpy.org/
###
### This script expects to find all the subject level segmentation results to be in one folder, and that the script is run from
### this folder. Of course it is easy to change that. The subject level segmentation is one file with a number of ROIs which have
### values ranging from 1 to N (where N is total number of targets of segmentation)
###
### for this example the subject file names are ITC###big.nii.gz  (ITC101big.nii.gz)
###
### following Tziortzi et al., 2013: "The DICE coefficient was estimated across subjects as the average overlap
### between a subject's segmentation with the segmentation from each of the other subjects in order to assess
### if the method and underlying connections were reproducible across subjects"
### (individual subjects' scans were non-linearly registered to the MNI template)
###
###  Tziortzi et al., 2013: Connectivity-based functional analysis of dopamine release in the striatum using
###                         Diffusion Weighted MRI and Positron Emission Tomography
###
### This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
### To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.
###
### Note: I started coding this without reading into nipype so code is long and propably somewhat inefficient :)
###
### VOLUME A : volume of subject VOLUME B: volume of group segment VOLUME I : intersection
### expects all individual segmentation files in one directory.currently script if run form there but can be changed to use other paths
###
###

import nipype.interfaces.fsl as fsl
from nipype.interfaces.fsl import ImageStats
from nipype.interfaces.fsl import ImageMaths
import numpy as np
from scipy import stats

sublist = range(101,123) # subject nr list 
seglist = range(1,11) # range(1,11) nr of segments = (1 to 10) in this example there are 10 targets.


# make all the segments first
for i in sublist:
    for j in seglist: 

      #get segment (note out_file contains L because this example is left striatum only)
      ImageMaths(in_file=('ITC%sbig.nii.gz' % i), out_file=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : i}), op_string=('-thr %(1)s -uthr %(2)s' % {"1" : j, "2" : j})).run()
    
      # binarize
      ImageMaths(in_file=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : i}), out_file=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : i}), op_string=("-bin")).run()

# now calc average DICE per segement per Subject
for i in sublist:
    for j in seglist: 
      # get volume A
      stats = ImageStats(in_file=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : i}), op_string='-V').run()
      volume_A = stats.outputs.out_stat[1]
      
      # get for intersection for one area each other subject
      # first make sublist of participants not including self
      sect_list = filter (lambda a: a != i, sublist)
      Dice_list= [0]*(len(sect_list))
      for k in sect_list:
        #mulitply to get inter section
        ImageMaths(in_file=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : i}),in_file2=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : k}), out_file=('intersect_%(1)s_L_%(2)s_%(3)s.nii.gz' % {"1" : j, "2" : i, "3" : k}), op_string=("-mul")).run()
        #get Volume B
        stats2 = ImageStats(in_file=('%(1)s_L_%(2)s_seg.nii.gz' % {"1" : j, "2" : k}), op_string='-V').run()
        volume_B = stats2.outputs.out_stat[1]
        # get volume Intersect
        stats3 = ImageStats(in_file=('intersect_%(1)s_L_%(2)s_%(3)s.nii.gz' % {"1" : j, "2" : i, "3" : k}), op_string='-V').run()
        volume_I = stats3.outputs.out_stat[1]
        #calculate Dice
        N = sect_list.index(k) # find place in list to put in Dice_list
        if (volume_A+volume_B)==0: #in rare case a subject does not have one segment we need to 
            Dice_list[N] = float('nan') # code for non existing segment
        else: 
            Dice_list[N] = 2* volume_I /(volume_A+volume_B)
    
      # store Dice to file
      #Average_Dice = sum(Dice_list) / float(len(Dice_list))# this does not work with NaN
      #Average_Dice= stats.nanmean(Dice_list)
      Average_Dice = np.mean(np.ma.MaskedArray(Dice_list, np.isnan(Dice_list)))
      l = open('DICE_'+str(i)+'.txt', 'a')
      l.write("%s\t" % j)
      l.write("%s\t" % Average_Dice)
      l.write("\n")
      l.close()
