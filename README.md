       ###########  calculate DICE Coefficient of segmentation results FSL ######

created by wouter van den bos #  woutervdbos@gmail.com

  this script is to perform a quality check between results of fsl probtracks segmentation
  see: http://fsl.fmrib.ox.ac.uk/fsl/fsl-4.1.9/fdt/fdt_probtrackx.html for details
  but can be used on ohter data sets too.
 
  DICE = 2 * A intersection B / |A|+|B|
  http://sve.loni.ucla.edu/instructions/metrics/dice/ for quick summary of DICE
 
  requires installation of nipype, a useful API for several popular imaging toolboxes
  http://nipy.sourceforge.net/nipype/
  also requires Scipy & numpy
  http://www.scipy.org/ & http://www.numpy.org/
 
  This script expects to find all the subject level segmentation results to be in one folder, and that the script is run from
  this folder. Of course it is easy to change that. The subject level segmentation is one file with a number of ROIs which have
  values ranging from 1 to N (where N is total number of targets of segmentation)
 
  for this example the subject file names are ITC###big.nii.gz  (ITC101big.nii.gz)
 
  following Tziortzi et al., 2013: "The DICE coefficient was estimated across subjects as the average overlap
  between a subject's segmentation with the segmentation from each of the other subjects in order to assess
  if the method and underlying connections were reproducible across subjects"
  (individual subjects' scans were non-linearly registered to the MNI template)
 
   Tziortzi et al., 2013: Connectivity-based functional analysis of dopamine release in the striatum using
                          Diffusion Weighted MRI and Positron Emission Tomography
 
  This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
  To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.
 
  Note: I started coding this without reading into nipype so code is long and propably somewhat inefficient :)
 
  VOLUME A : volume of subject VOLUME B: volume of group segment VOLUME I : intersection
  expects all individual segmentation files in one directory.currently script if run form there but can be changed to use other paths
 
NOTE: This code is in beta, may not be the latest version, assurances will not be made as to its quality. Use at your own risk. (and please let me know if you find a bug).
 
 