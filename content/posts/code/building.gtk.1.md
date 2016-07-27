Title: Building GTK3 / GtkSharp under Windows - Manual Build
Summary: Building GTK3 under Windows
Date: 2016-06-30 12:00
Tags: code, dotnet, GtkSharp, gtk

## Overview

Looking at the current NuGet packages for GtkSharp and the gtk3 binaries within GtkSharp.Win32.
These are not for the most recent version of Gtk3.
I decided to look into the process for building GTK3 and the latest version of GtkSharp under windows.
This also has the advantage of possibly using 64bit versions of GTK3.

The first links I looked into were

  * <http://www.gtk.org/download/windows.php>
  * <https://github.com/wingtk/gtk-win32>

The problem with the gtk-win32 build though is that the Dll's lack the "lib" prefix to the Dll names.
This is something that's expected by GtkSharp for cross compatibility with Linux.
Since there is interdependence between the different Dll's, simply renaming them wouldn't be enough.

## Native Libs

Fortunately, there's a very easy way to get the Dll's we need prebuilt, and that is to just copy them out of MSYS2 <br>
First we need to install MSYS2 from <https://msys2.github.io/>

Next open up a MSYS2 prompt then run the following to update the package database
``` sh
pacman -Syuu
```

To search for a package
``` sh
pacman -Ss gtk3
```

### Installing the 32Bit Dll's

Let's now open a MinGW **32bit** console window (bundled with MSYS2). <br>
We can use the following to install the Dll's we want.

``` sh
pacman -S mingw-w64-i686-gcc mingw-w64-i686-glib2
pacman -S mingw-w64-i686-pango mingw-w64-i686-atk mingw-w64-i686-gtk3
pacman -S mingw-w64-i686-zlib mingw-w64-i686-libiconv
```

If we now look within **C:\msys64\mingw32\bin**, we can harvest the native library Dll's we want to use with GtkSharp <br>
Using PE Explorer to look at the Dll depends to pick out what I need for GTK3, I came up with the below list for gtk3 3.20.4-1

**GTK Libs:**
``` sh
libatk-1.0-0.dll
libcairo-2.dll
libcairo-gobject-2.dll
libgdk_pixbuf-2.0-0.dll
libgdk-3-0.dll
libgio-2.0-0.dll
libglib-2.0-0.dll
libgmodule-2.0-0.dll
libgobject-2.0-0.dll
libgtk-3-0.dll
libpango-1.0-0.dll
libpangocairo-1.0-0.dll
libpangoft2-1.0-0.dll
libpangowin32-1.0-0.dll
```

**Dependencies:**
``` sh
libbz2-1.dll
libepoxy-0.dll
libexpat-1.dll
libffi-6.dll
libfontconfig-1.dll
libfreetype-6.dll
libgcc_s_dw2-1.dll
libgraphite2.dll
libharfbuzz-0.dll
libiconv-2.dll
libintl-8.dll
liblzma-5.dll
libpcre-1.dll
libpixman-1-0.dll
libpng16-16.dll
libstdc++-6.dll
libwinpthread-1.dll
libxml2-2.dll
zlib1.dll
```

### Installing the 64Bit Dll's

For the 64bit Dll's we can do something very similar to the above <br>
Under a MinGw 64bit console window

``` sh
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-glib2
pacman -S mingw-w64-x86_64-pango mingw-w64-x86_64-atk mingw-w64-x86_64-gtk3
pacman -S mingw-w64-x86_64-zlib mingw-w64-x86_64-libiconv
```

This should result in the equivalent 64bit files to show up under **C:\msys64\mingw64\bin**


## GtkSharp .Net Libs

### The Build process

Next we're going to need to build the GtkSharp sources into .Net Dll's

Just to explain a bit about how the build process works. <br>
The build process can be described as a 2 stage process

  - **gapi-parser** - generate xml files from original gtk source code libraries
  - **configure / make** - generate some of the .cs files from the xml files from stage 1
    and create the compiled Dll's we need to run GtkSharp

The first stage is usually done already for us by the person maintaining the source repo. <br>
Looking at the git repo <https://github.com/openmedicus/gtk-sharp.git> this seems to match the version of gtk3 within MSYS2 <br>
so we should be able to skip over this stage

From what I can gather the above step involves

  * extracting the source code for the different gtk libraries into the sources directory located within gtk-sharp.
  * running *make api* to generate the .raw files located within each of the source directories such as gdk-api.raw.
  * The input file for this process is sources.xml
  * under the hood the Makefile calls *..\parser\gapi-parser sources.xml* <br>
  * The parsing is actually handled via <http://www.mono-project.com/GAPI>

The second stage is the part we're interested in; this involves the make build system.
I've found the easiest way to do this is via the use of MSYS2 / MinGW Console.


### Setting up MSYS2

First we need to setup MSYS2 to handle the build process for gtksharp <br>
Let's start a "MinGw-w64 Win32 Shell" <br>
One of the first packages we need is gcc so let's install that first

``` sh
pacman -S mingw-w64-i686-gcc mingw-w64-i686-glib2
pacman -S mingw-w64-i686-pango mingw-w64-i686-atk mingw-w64-i686-gtk3
```

Let's install a couple more packages to help out
``` sh
pacman -S gzip nasm patch tar xz gettext make coreutils diffutils wget
```

### Downloading the Source

Next we need to download the source for gtk-sharp. <br>
Let's create a new directory called **C:\gtk-build** and download the gtk-sharp source into that directory

Using a Visual Studio Developer command prompt:
``` bat
cd C:\gtk-build
git clone https://github.com/openmedicus/gtk-sharp.git
```

Note I had to make a small change to the source to get it to build, the fork is located here <https://github.com/grbd/gtk-sharp.git><br>
I've submitted a pull request for this to be submitted to the main tree

### Running the Build Scripts

Next we need to run the build scripts from within MSYS2<br>
The link below is a bit out of date but it was useful for me to figure out how to handle the build process

  * <http://www.mono-project.com/archived/compiling_gtksharp/>

To start the build switch back to the MinGW Prompt we opened earlier and run the following
``` sh
PATH=$PATH:/c/Program\ Files\ \(x86\)/Microsoft\ SDKs/Windows/v10.0A/bin/NETFX\ 4.6\ Tools/
PATH=$PATH:/c/Windows/Microsoft.NET/Framework/v4.0.30319/

cd /c/gtk-build/gtk-sharp/
./autogen.sh --prefix=/tmp/install
make
```

### End Result

The end result should be a series of .Net Dll files located within subdirectories of the gtk-sharp directory. <br>
I avoided running *make install* as that seems to try copying / registering the Dll's into the GAC of the local system. <br>
Instead I'm more interested in using these files along with the native Dll libs above for the bundling into NuGet Packages. <br>
In order to test this out manually

  * Create a simple test app within Visual Studio
  * Copy and paste all the native Dll's mentioned above, along with the .net Dll's from GtkSharp into the Debug/bin directory
    (the destination where everything is compiled to for the test application)
  * Manually add references within the test application to the copied .Net Dll's

This should allow you to get an application up and running for testing

## Next Step

For the next step I'll probably look into a way of building this more automatically perhaps via a python script.
With any luck I might be able to get some of my own custom NuGet packages uploaded.

Many thanks to those that are maintaining a GtkSharp for gtk3,
This seems to be currently one of the few libraries that is production ready for use as a cross platform Desktop GUI at the moment.
