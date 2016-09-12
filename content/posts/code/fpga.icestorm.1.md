Title: Setting up the IceStorm FPGA tools for Windows
Summary: Setting up the IceStorm FPGA tools for Windows
Date: 2016-09-12 21:30
Tags: code, fpga, icestorm

## Overview

There was recently a presentation by the team running the icestorm project over at the Manchester Hackspace. <br>
Icestorm is a project that provides a fpga board for under $30 (about 25 Pounds in British money) 

  * <https://hackaday.com/2016/08/03/the-perfect-storm-open-arm-fpga-board/>
  * <http://www.clifford.at/icestorm/>
  * <http://www.clifford.at/yosys/>

Typically, the two largest vendors of fpga's tend to be Altera and Zynq.
However, both of these vendors require closed source tools which tend to be very large to compile down from Verilog or VHDL
into code that can be used on the FPGA.

With this board a **[iCE40HX4K](http://www.farnell.com/datasheets/1673535.pdf)** from Lattice Semiconductor is used instead. <br>
The team behind this project have built up a full open source toolchain for it.

I don't have a board yet (I'm thinking of building a modified one)
But I decided to see if I could build out the initial tools needed to compile Verilog.
With the eventual plan to use [Myhdl](http://www.myhdl.org/) which would compile down to ether Verilog / VHDL for use on the board


## Installation

### MSYS2

First for windows you'll need a copy of MSYS2 installed if you haven't already got it

  * <https://msys2.github.io/>

Once it's installed you can update the package database / packages via

``` sh
pacman -Syuu
```

There are 3 shells available in total

  * MSYS2
  * MinGW 32Bit
  * MinGW 64bit

For building some of the below sources I use MSYS2 and for others I use MinGW.
Strictly speaking the only real difference is the C library that they link against.
Based on this Link <https://sourceforge.net/p/msys2/discussion/general/thread/dcf8f4d3/>

MSYS2 Better understands POSIX conventions like paths, it does have a performance penalty compared to MinGW
since it funnels everything via msys-2.0.dll. But it can work sometimes better than MinGW when trying to compile Linux apps under Windows.

MinGW does not depend on msys-2.0.dll and instead uses the MSVC runtime. <br>
For the below I'm only really interested it getting things to work, so I've just used whichever one works best for each source package.


### MSYS2 - Depends

Next we need to install some dependencies, open up a MSYS2 shell and install the following

```sh
pacman -S mingw64/mingw-w64-x86_64-clang
pacman -S msys/bison
pacman -S msys/flex
pacman -S msys/libreadline-devel
pacman -S msys/gawk
pacman -S msys/tcl
pacman -S msys/libffi-devel
pacman -S git
pacman -S cmake
pacman -S mercurial
pacman -S msys/pkg-config
pacman -S python
pacman -S python3
pacman -S mingw64/mingw-w64-x86_64-libftdi
pacman -S mingw64/mingw-w64-x86_64-python3-pip
pacman -S mingw64/mingw-w64-x86_64-python2-pip
pacman -S mingw64/mingw-w64-x86_64-dlfcn
```


### Xdot - Python

Let's install xdot next, there currently isn't a pacman package for it, so I've used python / pip since it's a python based library <br>
Within a **MinGW x64** window
```
pip2 install xdot
pip3 install xdot
```


### Icestorm Tools

Next let's build and install icestorm
I've found this doesn't work under MSYS2, but does work under **MinGW x64**

```
git clone https://github.com/cliffordwolf/icestorm.git icestorm
cd icestorm
make PREFIX=/usr -j$(nproc)
make PREFIX=/usr install
cd ..
```
This should install the icebox tools to /usr/bin/


### Arachne-pnr (The place and route tool)

Next let's build and install Arachne-pnr for the place and route tools <br>
I'm running this build within a MinGW x64 window as above
```
git clone https://github.com/cseed/arachne-pnr.git arachne-pnr
cd arachne-pnr
make DESTDIR=/usr ICEBOX=/usr/share/icebox -j$(nproc)
make DESTDIR=/usr ICEBOX=/usr/share/icebox install
cd ..
```
This should install arachne-pnr to /usr/bin/


### Yosys (Verilog synthesis)

For Yosys there is the pre-compiled version 0.6 available here

  * <http://www.clifford.at/yosys/download.html>

Although I think ideally we need the latest version from git for the iCE FPGA's <br>
From what I've discovered trying to build this under the MinGW console will not work. <br>
However, building under the MSYS2 Console does work, with a little tweaking of the Makefile.

First let's download a copy of yosys
```sh
git clone https://github.com/cliffordwolf/yosys.git yosys
cd yosys
```

Next we're going to configure make for MSYS2
```sh
make config-msys2
```

Next we need to patch the Makefile
```sh
wget TODO Link
patch -p1 < ../patch1.patch
```

Next we can start the build
```sh
make PREFIX=/usr
```

Finally, we can install the files into /usr/
```sh
make PREFIX=/usr install
```
