Title: todo1
Summary: Uploading firmware with Openocd and a JLink or CMSIS-DAP Interface
Date: 2016-11-23 18:00
Tags: micro, mbed, mbed-cli
Status: draft

## Overview

I've recently been looking into programming ARM based boards using Jtag / SWD and Openocd

TODO add image

  * https://www.embeddedartists.com/products/lpcxpresso/lpc1769_cmsis_xpr.php

The above board is a LPC1769 xpresso, this appears to be a new version of the board with a CMSIS-DAP USB to SWD Adapter instead of the original LPC-Link.
One of the problems with LPC-Link is that its not supported by the open source openocd app for programming.
CMSIS-DAP is a new cross platform standard for connecting a USB cable to a SWD port for programming.
it makes the device appear as a HID Input device which means it doesn't need special hardware or drivers to program or debug any ARM based IC.

I'm going to go through the process of programming this board 3 different ways

  * Using openocd and the USB / CMSIS-DAP connection
  * Using openocd and a JLink Segger
  * Using the JLink Segger JFlash Lite software and a JLink Segger

A couple of reasons as to why I'm interested in using the JLink adapter instead of the inbuilt CMSIS-DAP adapter includes

  * JLink software has the ability to use unlimited breakpoints using GDB via some fancy messing with break instructions and logging instructions in flash.
    https://www.segger.com/jlink-unlimited-flash-breakpoints.html
  * You can get the educational version of the JLink (the white one) reasonably cheap at around 60 Pounds plus delivery
    http://uk.farnell.com/segger/8-08-90-j-link-edu/jtag-emulator-j-link-edu-usb/dp/2098545
  * The number of supported ARM chips is likley to be much greater than openocd (the drivers and firmware are constantly being updated)

From a speed point of view I managed to get around 2.3 seconds with the frequency set to 500Khz in the config for both the Segger and the CMSIS-DAP Inteface

One word of warning with this board, there's a small jumper to disable the CMSIS-DAP Programmer.
This jumper is not soldered via a thru-hole, instead it's just surface mounted soldered to the board (strange considering all the other jumpers have through hole pads).
This makes it very easy to break off the jumper pins from the top of the board (which is what happened to mine).
Fortunatley I've found that I don't need to disable the CMSIS-DAP adapter in order to use the JLink on the SWD Pins, both seem to co-exist quite happily


## CMSIS-DAP Interface / Openocd Software

First I'm going to cover the simplest option which is just a USB cable between the board and the PC

TODO add image

First we need to download a copy of openocd, the latest version (which is quite old but working) is 0.9.0 <br>
In my case I just downloaded the zip file and extracted it to **C:\Apps\OpenOCD-20160901**

  * https://sourceforge.net/projects/openocd/files/openocd/0.9.0/

Usualy openocd reads in ether one or multiple config files, each config file is just a list of commands run in the software.
The default is to read in openocd.cfg although you can specify which config files to load in with the -f option


### Main.cpp

First I've included a very simple block of code compiled in mbed via the LPC1768 target to flash the led different colours

**main.cpp**
```
#include "mbed.h"

DigitalOut led1(P0_22);
DigitalOut led2(P3_26);
DigitalOut led3(P3_25);

void blink(DigitalOut ledval);

// main() runs in its own thread in the OS
// (note the calls to Thread::wait below for delays)
int main() {
  led1 = true;
  led2 = true;
  led3 = true;

  while (true) {
    blink(led1);
    blink(led2);
    blink(led3);
  }
}

void blink(DigitalOut ledval)
{
	ledval = false;
	Thread::wait(500);
	ledval = true;
	Thread::wait(500);
}
```



### Adapter / CPU Config file

First lets create a config file to specify the interface, the cpu and the speed / options we want to use for connecting to the board

**boardconf.cfg**
```
# Note reference one of the configuration files for the physical interface to connect to the board
# https://github.com/ntfreak/openocd/tree/master/tcl/interface

# ARM CMSIS-DAP compliant adapter
# http://www.keil.com/support/man/docs/dapdebug/
source [find interface/cmsis-dap.cfg]

# Add the cpu
source [find target/lpc17xx.cfg]

# Set the Speed
adapter_khz 500
```

I've found it's best to set the interface first, then the cpu type then the speed.

  * Sometimes the cpu configuration (lpc17xx.cfg) will override the speed setting so it's best to set the speed after this option
  * Sometimes before sourcing the cpu configuration file you need to set the CPU with **set chipname**. in this case the lpc17xx.cfg already does this for us.
  * see https://github.com/ntfreak/openocd/tree/master/tcl/interface for interfaces
  * see https://github.com/ntfreak/openocd/tree/master/tcl/target for target devices

The speed defaults to around 10Khz unless specified, this can take anywhere 1 - 2 minuites depending on the interfaces used to upload the firmware.
With a higher setting that can be reduced to around 2 seconds.
Also unless you have the speed set to something higher this can cause timeouts with the JLink with the SWD interface.


### Firmware Program Config file

This configuration file is just a series of commands to send to openocd to flash a binary firmware file to the device

**progconf.cfg**
```
# Make the initial connection and halt the board, Test with this first
init
targets
reset halt

# Upload the firmware
program BlinkyTest1.bin verify

# Reset the Board
reset
# Exit OpenOCD
shutdown
```

### Connecting with Putty

First lets try connecting to the board using a terminal such as putty

```
openocd --search C:\Apps\OpenOCD-20160901\share\openocd\scripts -f boardconf.cfg
```

This should launch openocd, specify the interface, board and speed. <br>
Since there's no shutdown command in this configuration file openocd will continue to run unless you hit Ctrl-C or issue a shutdown from the terminal. <br>
If we now run putty and select localhost / port 4444 we can now connect to openocd's terminal and issue other commands.

TODO add image

It's also possible to use GDB (the exe included with the GCC toolchain you used to compile the code) to connect to openocd on localhost / port 3333

TODO commands for gdb

  * http://openocd.org/doc/html/GDB-and-OpenOCD.html


### Flashing the Binary File

If we add the progconf.cfg file in to the end of the command line.
we can trigger openocd to upload a binary blob to the device.
since the last command in progconf.cfg is **shutdown** openocd will quit once the upload is complete

This assumes BlinkyTest1.bin is in your current directory.

```
openocd --search C:\Apps\OpenOCD-20160901\share\openocd\scripts -f boardconf.cfg -f progconf.cfg
```


## JLink Interface / Openocd Software

Next I'm going to do the same as before using the JLink and openocd


### Setting up JLink for Openocd

In order to use the JLink Segger interface with openocd we first need to switch it's driver with a WinUSB one so that openocd can access the device. <br>

First run C:\Apps\OpenOCD-20160901\drivers\UsbDriverTool.exe <br>
and select the JLink device in the list

TODO image

Select **Change driver type** and change it to **WinUSB**

TODO image

At this point I find it's best to unplug / replug the segger / board into the PC. <br>
If you need to switch the device back to use the JLink software instead of openocd, just do the same as before but select the JLink driver instead in the list.


### Connecting to the board

Next we need to connect the JLink to the board.
the red wire should match up with the small arrow on the board.
If in doubt one side of the 10 pin header is mostly ground pins which you can test with a multimeter

TODO image connected board

TODO image 10 pin header


### SWD Connector

Typically SWD only uses about 2 data pins for connecting to the ARM chip (SWDIO and SWDCLK).

  * SWDIO - Input / Output Data
  * SWCLK - Data clock
  * nRST - Reset device pin
  * GND - device ground pin
  * SWIO - Optional debug output pin (similar to a printf output)
  * VDD - Optional power from the programmer to the device

In this example the JLink defaults to Jtag mode, although it also works in SWD mode as long as the speed is high enough.
Jtag mode seems to need more reset pins typically, although it seems to work with the 10 pin connector without problems.

ST based arm devices have something called STLink which is basically the same thing but with a different pin arrangement.

The closest I've found to a socket for the 10 pin header connection is

  * https://makersify.com/products/dfrobot-gadgeteer-socket-smt-10pcs (pins flat against the board)
  * http://www.digikey.com/product-search/en?x=-1289&y=-73&lang=en&site=us&KeyWords=3220-10-0100-00 (thru hole)

For the JTAG adapter to connect the Segger, I've found the best source is adafuit

  * https://www.adafruit.com/product/1675
  * https://www.adafruit.com/products/2094
  * https://www.adafruit.com/products/2743

I've found with this board that disabling the CMSIS-DAP adapter with a jumper doesn't need to be done for this to work.


### Changing the config

To tell openocd to use a JLink instead of CMSIS-DAP adapter just replace this line in boardconf.cfg
```
source [find interface/cmsis-dap.cfg]
```

With
```
source [find interface/jlink.cfg]
transport select swd
```

### Flashing the firmware

At this point it should be possible to flash the firmware via the JLink exactly the same way as before

```
openocd --search C:\Apps\OpenOCD-20160901\share\openocd\scripts -f boardconf.cfg -f progconf.cfg
```


## JLink Interface / JLink Software

Next I'm going to try using the native JLink software to upload the firmware. <br>
First make sure the driver for the JLink adapter is set back to it's original driver if it's been changed for openocd.

### JFlash Lite

TODO

### JLink Commander

TODO

