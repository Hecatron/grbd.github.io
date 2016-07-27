Title: Bossac for the Arduino Due
Summary: Bossac for the Arduino Due
Date: 2016-01-10 21:30
Modified: 2016-01-10 21:30
slug: ArduinoDue.Bossac
Category: tools
Tags: tools, due, arduino, arm
Status: draft
imagefeature: "website-speed.jpg"
mathjax: null

## Arduino Due

One of the development boards I've been using and experimenting with is the Arduino Due.
This is a Arm based arduino board that uses a Atmel SAM3X8E ARM Cortex-M3 CPU.

http://www.atmel.com/Images/Atmel-11057-32-bit-Cortex-M3-Microcontroller-SAM3X-SAM3A_Datasheet.pdf

If you decide to use the stock arduindo software to upload code to the board then everything is pretty much handled for you within the Arduino Due.
However if you want to upload code compiled via other means then things tend to get a little more complicated.
I've put some details together here on how to build and compile the tools needed to upload code to the arduino due without the use of the arduindo gui.
One example would be if you wanted to upload code compiled from cmake / C++ or perhaps Atmel Studio.

## The USB ports

First it's best to look at the USB ports on the back of the arduino due board.
There are 2 usb ports available
  * The programming USB port
  * The native USB port.

The native USB port is wired directly into the ARM CPU and can be made to do anything you want pretty much in code.
The programming USB port is instead first wired to a ATmega16U2 which acts as a USB to Serial adapter / Virtual COM port.
The main advantage the programming port has over the native port (other than freeing up the native port) is that it has a much more reliable method
for resetting and erasing the device from software.

## Building Bossa under Windows

### Install Mingw32

First we need to install mingw, run the setup exe from Link
Then select the following options within the Mingw installation manager

  * Mingw32-base (C Compiler)
  * Mingw32-gcc-g++ (C++ Compiler)
  * Msys-base (for the terminal

### Download Bossa

Next download the arduino bosa sources, and switch to the arduino branch <br>
Run the following in a dos cmd shell

<code>
cd D:\SourceControl\GitExternal\
git clone https://github.com/shumatech/BOSSA.git
git checkout arduino
</code>

### Edit make_package.sh

The make_package.sh file is set to only compile the command line version of bossa (bossac.exe)
To get this to work, remove the -j4 option from the make command in the script

<code>
make bin/bossac.exe
</code>

### Compile Sources

Next open a Msys shell, and compile the sources

<code>
cd /d/SourceControl/GitExternal/BOSSA
./arduino/make_package.sh
</code>

### The Bossa GUI

Unfortunatley I've not managed to get the Bossa GUI to build under windows
as far as I can tell it requires a version of wxWidgets for windows that includes wx-config.exe and is of the 2.8 branch
Since I don't really need the gui anyway I decided to just set the build to skip over that part

TODO .Net Gui for Bossac
