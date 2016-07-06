Title: Ooznest CNC Oxbot
Summary: Quick summary of a CNC machine I've been working on
Date: 2016-07-03 15:10
Tags: cnc, spindle, 3dscan
Status: draft

## Overview

Something I picked up a while back was a Ox CNC from [Ooznest](http://ooznest.co.uk/)
My plan at the moment is to set this up initially as a CNC, but then add other parts to it later on for 3D printing etc.

## 3D Printers vs CNC's

Typically with 3D printers they use additive manufacturing where a layer of plastic (usually abs or pla) is placed on top in layers.
With a CNC instead this uses subtractive manufacturing where you remove material from a block of wood or metal to make the part you want.

The different approaches tend to have an influence on the overal design of the machine.
With a 3D printer typically speed is what you're aiming for as well as cheapness in some cases.
With a CNC instead the main focus in on rigidity and strength, instead of placing plastic down in layers you are forcing a milling bit
into a block of material to remove wood, plastic or metal.

So in other words with a CNC you want something which is very strong and beefy where the frame isn't going to flex or bend under tension.
Usually you'll see Nema 17 stepper motor's with a 3D printer, and Nema 23 stepper motors or higher with a CNC, this provides additional force
to push against the part being milled.

Ultimately there are different trade off's with different approaches.
Something which is big and heavy doesn't respond well to rapid changes in speed or acceleration which can lead to overshooting.
Something which is very lightweight responds much better in this situation to high speed movement.
That being said my thoughts are that it should be possible to compensate for the overshoot via the use of more complicated
motion control systems such as machinekit to try and get the best of both worlds.


## Build

### Mechanical

for the CNC itself I'm currently using a ooznest Ox CNC, this is similar to the default CNC but has slight modified plates.
This CNC comes in kit form with an option for black anodized frame. The parts for the kit are all openbuilds related parts (except for the plates).

  * [ooznest Ox CNC](http://ooznest.co.uk/3D-Printer-CNC-Kits-Bundles/OX-CNC-Machine)

### Electronics

For the electronics for now I've decided to use an Arduino Due which is a 32bit processor and a Radds board

  * http://ooznest.co.uk/RADDS-3D-Printer-Controller-Board

Currently I've got no end stops, but I am working on the brackets needed to mount some inductive sensors in the right places, as well as brackets for the cable chain

### Software

For the board firmware I'm using a modified version of TinyG2 for use with the Due / Radds board

  * [Radds Firmware](https://github.com/grbd/GBD.OxBot.FirmwareG2)

For the controlling software I'm currently using Chillipepr

  * ]http://chilipeppr.com/tinyg
  * [Serial Port JSON Server](http://chilipeppr.com/tinyg#com-chilipeppr-widget-serialport-download)

## Setup

TODO add settings / how to build firmware


## Future Goals

At the moment the main focus is to get the device working as a CNC hopefully with a better spindle.
Later on I've got a few different ideas for interchangeable heads.
This should include 3D printing, EDM, UV Exposure via a Blu-ray head for making PCB's, built in inductive calipers for postiional feedback and so on.

For the electronics I'm going to try and move across to a beaglebone green using [Machinekit](http://www.machinekit.io/).
Machinekit is able to use the PRU's (coprocessor's) on a Beaglebone for real-time motion control and support for additional G-Codes.
There's an interesting talk about it here compared to other motion control systems [Link](https://www.youtube.com/watch?v=LdJ8xjCJIGo)

For the front end I'm going to try and use a Rpi3 with a 3D interface.
Some of the more recent kernels now have hardware accelerated 3D support now built in
compared to a lot of other Rpi similar boards which currently lack this at the moment.
