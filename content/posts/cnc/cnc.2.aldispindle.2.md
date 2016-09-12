Title: Scanning in of the spindle in 3D - Part 1
Summary: Scanning in of the spindle in 3D - Part 1
Date: 2016-07-05 9:00
Tags: cnc, spindle, 3dscan
Status: draft

## Overview

In order to make a bracket to mount the spindle to the Ox, I decided to try a 3D scan of the outer case of the spindle
so that I could accurately create a bracket that would fit around the outside

To begin with I tried an XBox 360 with some different types of software, but I felt that the end result wasn't accurate enough
so I decided to try something called Photogrammetry instead

The following is based on the following [Youtube clip](https://www.youtube.com/watch?v=D6eqW6yk50k) from Phil Nolan,
many thanks to Phil for putting the time in to detail how perform scans with this software.

TOOD

  * https://hackaday.io/project/9792/instructions

Next step is to build a frame using a couple of Nema 17's and a frame out of mdf, with bearings / wheels and some threaded rod / nuts



## Software

### Options

There's a few different options for the software depending on if you want something free or commercial

  * [Visual SFM](http://ccwu.me/vsfm/) - Seems to be one of the most commonly used free softwares, although techically not open source
  * [OpenDroneMap](https://github.com/OpenDroneMap/OpenDroneMap) - Free / Open Source but Linux only
  * [Python Photogrammetry Toolbox](http://184.106.205.13/arcteam/ppt.php) - Free / Open Source, GUI seems a bit limited

  * [PhotoScan Standard](http://www.agisoft.com/features/standard-edition/) - Commercial
  * [ReCap 360](http://recap360.autodesk.com/) - Free / Commercial
  * [123D Catch](http://www.123dapp.com/catch) - Free / Commercial

Since I'm using Windows 10 x64 with a Nvidia card, and the tutorial already covers it, I decided to go for Visual SFM

If you want to try out the Python Photogrammetry Toolbox instead, then you'll need <br>
Python 2.7 - 64bit, Pillow python module (installed by pip), Qt 4.8.7 (32bit mingw version), PyQt4 - 64bit (for python 2.7 / Qt 4.8.4)
and the Python Photogrammetry Toolbox + GUI

### Install

Next I needed to install the following bits of software

  * [Visual SFM](http://ccwu.me/vsfm/) - I used the Windows x64 Version with Cuda support for Nvidia graphics cards
  * [CMVS For Windows](http://www.di.ens.fr/cmvs/) [Link2](https://github.com/pmoulon/CMVS-PMVS/tree/master/binariesWin-Linux/Win64-VS2010) - This needs to be extracted into the same directory as Visual SFM
  * [Meshlab 1.3.3](http://meshlab.sourceforge.net/)


## Taking Pictures

First I needed to take pictures, lots and lots of pictures from every angle around the device

  * Try to use the highest resolution you can
  * Try to avoid reflective surfaces
  * Placing a grid underneath the object might help (such as a teatowel for example)
  * Make sure the object doesn't move while taking pictures
  * Try to avoid using flash

TODO  try taking picture from further away

![TPicture1]({filename}/static/cnc/cnc.2.aldispindle.2/TPicture1.jpg)

## Using Visual SFM


TODO select match using cuda in the menu

Next I needed to import the images into Visual SFM. <br>
Click the folder with the plus button next to it, then select the directory, and select all images with Ctrl-A.

![VSFM1]({filename}/static/cnc/cnc.2.aldispindle.2/VSFM1.png)

Next we click the X shaped button with an arrow *Compute Missing Matches* <br>
This will attempt to match each image with every other in terms of common points

![VSFM2]({filename}/static/cnc/cnc.2.aldispindle.2/VSFM2.png)

Next we click the double arrow for *Compute 3D Reconstruction*

![VSFM3]({filename}/static/cnc/cnc.2.aldispindle.2/VSFM3.png)

Next we click *Run Dense Reconstruction* <br>
Select a destination for the file to save <br>
This next part can take a long time to run (maybe 20 - 30 mins)

![VSFM4]({filename}/static/cnc/cnc.2.aldispindle.2/VSFM4.png)

Once the last step is complete, we can hit the *TAB* key to get a view of the model so far <br>
At this stage we can now just close Visual SFM and switch to Meshlab

TODO image of model

TODO try using images the right way up

## Meshlab


### Loading into Meshlab

  * Next open Meshlab
  * Open the saved mvm file that Visual SFM saved before

TODO Add images

  * The model / point cloud seems to default to upside down, so we need to rotate it right side up
  * Middle mouse button to pan, scroll wheel to zoom in
  * Select the button to show the layers panel

TODO image of model

  * Select the eye button next to the main layer to hide it

TODO image of icon

  * Select File -> Import Mesh
  * Select the PLY file that Visual SFM exported

TODO image of prompt


### Removing artifacts within Meshlab

Next we need to remove any background parts that are not required

  * Click the Rectangular selection tool icon
  * Highlight any points to be removed
  * Click the delete points icon
  * Rinse and repeat to remove all remaining artifacts

TODO image of model with bits removed

### Generate new Mesh

  * Next select the Filters Menu -> Point Set -> Surface Reconstruction Poisson
  * Set the Octree Depth to 12
  * Set the Solver Divide to 7
  * Leave the other two at 1
  * Click Apply

TODO image of modal

  * We can now hide the ply mesh, this should give us a view of the end result

TODO Image

### Cleanup

Next we need to do a bit of cleanup

  * Select the 3rd layer in the list
  * Select Filter Menu -> Selection -> Select non manifold edges
  * Select Delete

TODO Image

Next we need to create a UV Map

  * Select Filters Menu -> Texture -> Parameterisation _ texturing from registered rasters
  * For texture size we can use 2048
  * Click Apply

TODO image of prompt

### Export Mesh

The final step is just to export the mesh

  * Select File Menu -> Export Mesh As
  * Choose a file format in the drop down (TODO look into best one for Solidworks)
  * Choose a file name to save as

In the next part I'll try and import this into solidworks and parse it into an actual part. <br>
At which point I can then use it to base a bracket around.



TODO I think OpenMVG is better
VisualSFM is taking frinken agaes at the moment

Archeos links
http://www.archeos.eu/
https://github.com/archeos?page=2
http://arc-team-open-research.blogspot.co.uk/2016/05/archeos-hypatia-new-tool-for-3d.html
https://groups.google.com/forum/#!topic/vsfm/VcXGvP1HuMo

There is also a GUI being developed for Archeos
https://github.com/openMVG/openMVG/issues/411
https://github.com/mad-de/openMVG_gui
https://github.com/open-anatomy/SfM_gui_for_openMVG/
https://www.youtube.com/watch?v=Q2_cVN902-M

This GUI seems a bit out of date but is worth investigating
https://github.com/rhiestan/Regard3D

OpenMVG seems to be a lot faster than the PPT 
https://github.com/openMVG/openMVG
http://openmvg.readthedocs.io/en/latest/software/SfM/SfM/
http://openmvg.readthedocs.io/en/latest/software/SfM/SfM/#openmvg-sfm-pipelines-demo
http://arc-team-open-research.blogspot.co.uk/2015/06/openmvg-vs-ppt.html


TODO

for now try CMPMVS for the dense reconstruction instead of VisualSFM
https://www.youtube.com/watch?v=ZRTEMKS3Sw0
http://ptak.felk.cvut.cz/sfmservice/websfm.pl?menu=cmpmvs
