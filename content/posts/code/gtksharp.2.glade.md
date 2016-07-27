Title: GTKSharp - Part 2 - Setting up Glade
Summary: Getting glade up and running under windows using Msys2 for designing gui's with drag and drop
Date: 2016-01-29 21:00
Tags: code, dotnet, gtksharp, glade

## Overview

The first step in getting GTKSharp to work is to get glade up and running.
Glade is an application written to design and create GTK forms via drag and drop.
This means we can drag and drop controls onto a form then finally export / save an xml file to be used later by Visual Studio.

From what I've seen there are two different GUI's available for designing GTK Forms with drag and drop controls
(Similar to WinForms under Visual Studio)

  * Stetic - this is an editor included / embedded into the Monodevelop application, it appears to be limited to GTK2 Applications
  * Glade - this is standalone editor which supports both GTK2 and GTK3

For Glade there are two main branches

  * Version 3.8 - Which is used for GTK2 Forms
  * Version 3.19 and above - Which is used for the newer GTK3 Forms

Since I'm looking at using GTK3 and Visual Studio instead of Monodevelop, I'm going to use glade here.
It is possible to download a version of glade from the website <https://glade.gnome.org/>
However, the versions for windows don't appear to be maintained on a regular basis, so seem to be fairly old.
The MSYS2 versions of glade however seem to be fairly up to date, and it's a lot easier than building from source.

## Installing MSYS2

The first step is to make sure we have MSYS2 installed. MSYS2 is a newer replacement for Mingw under windows.
It's just something that makes running linux applications natively under windows a lot easier.
So install this first

  * <http://sourceforge.net/projects/msys2/>
  * <http://sourceforge.net/p/msys2/wiki/MSYS2%20installation/>

After the initial install open up a MSYS2 console window.

![msys1img]({filename}/static/code/gtksharp.2.glade/Msys1.png)

The first thing we want to do is update the core packages for MSYS

```
update-core
```

Next update any installed packages for MSYS
```
pacman -Su
```

## Installing Glade

Next we're going to install glade, make sure you have a MSYS console open 

To search for the glade packages
```
pacman -Ss glade
```

To install for 64Bit Windows
```
pacman -S mingw64/mingw-w64-x86_64-glade
```

To install for 32Bit Windows
```
pacman -S mingw32/mingw-w64-i686-glade
```

## Running Glade

We can now run glade via the exe C:\msys64\mingw64\bin\glade.exe

![gladeform1img]({filename}/static/code/gtksharp.2.glade/GladeForm1.png)

  * Select File -> New
  * Drag and drop a Window from the TopLevels section into the viewing area
  * Drag and drop a fixed control inside the Window Control
  * Drag and drop a button and TextEntry control into the fixed area

One important thing to note for the current version of GTKSharp pulled from Nuget (3.1.3)
This requires the GTK+ version of the glade file to be set to 3.14

  * Select File -> Properties
  * Under Toolkit version required: change this from 3.16 to 3.14

At this point you can save your new glade file to anywhere you want.
Later on we'll be using this with GTKSharp and Visual Studio

## Copying Across MSYS Files

One of the things I noticed when running glade files from .Net is that the application can have problems finding schema and icon files
normally associated with GLib when using for example a FileChooserButton

There's some more information over at this github link: <https://github.com/openmedicus/gtk-sharp/issues/6>

The quick fix to this is just to copy and paste some directories from MSYS into ProgamData under windows

| Source | Destination |
| ------ | ----------- |
| C:\msys64\mingw64\share\glib-2.0\schemas | C:\ProgramData\glib-2.0\schemas |
| C:\msys64\mingw64\share\icons | C:\ProgramData\icons |
| C:\msys64\mingw64\share\themes | C:\ProgramData\themes |

<br>
[GTKSharp - Part 1 - Cross Platform Toolkits]({filename}./gtksharp.1.toolkits.md) <br>
[GTKSharp - Part 3 - Basic Example with VS and Glade]({filename}./gtksharp.3.example1.md)
