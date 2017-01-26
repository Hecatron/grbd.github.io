Title: Uploading firmware with Openocd and a CMSIS-DAP Interface
Summary: Uploading firmware with Openocd and a JLink or CMSIS-DAP Interface
Date: 2016-11-23 18:00
Tags: micro, mbed, mbed-cli
Status: draft


## Building OpenOCD

During my experimentation with openocd I tried to have a quick go at compiling the latest source code from git.
I've found the 0.9.0 version is actually okay for everything I need but others might find this usefull.

In this example I'm using the MSYS2 environment under Windows

First lets update MSYS2 to the latest version
```
pacman -Syuu
```

Next I wanted to make sure as many dependencies that would be needed would be installed.
So I just installed the binary / package managed version of openocd to try and bring everything in

```
pacman -S mingw64/mingw-w64-x86_64-openocd-git
pacman -S mingw64/mingw-w64-x86_64-hidapi
pacman -S msys/texinfo
pacman -S msys/texinfo-tex
pacman -S msys/autoconf
pacman -S mingw64/mingw-w64-x86_64-libusb
pacman -S mingw64/mingw-w64-x86_64-libftdi
```

Next lets fetch some sources. <br>
I've included the latest pull request for JLink below as well
```
git clone http://openocd.zylin.com/p/openocd.git openocd_master
git fetch http://openocd.zylin.com/openocd refs/changes/86/3886/1 && git checkout FETCH_HEAD
```

Lets build some sources <br>
(replace /home/username/openocd_bin/ with whichever directory you want to install to)
```
cd openocd
./bootstrap
mkdir /home/username/openocd_bin/
./configure --prefix=/home/username/openocd_bin/
make
make install
```

Next lets test
```
cd /home/username/openocd_bin/bin/
openocd --search ../share/openocd/scripts
```
