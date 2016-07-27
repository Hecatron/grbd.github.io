Title: GtkSharp - Part 1 - Cross Platform Toolkits
Summary: Exploring the different GUI toolkits available for .Net across different platforms
Date: 2016-01-28 19:00
Tags: code, dotnet, GtkSharp, toolkits

## Overview

I decided to have a look into the different toolkit's available for writing .Net code with a GUI that can be used across
multiple platforms. Some of these platforms would include Microsoft Windows 10, Linux and embedded devices such as the Raspberry Pi

I've posted some example code here for GtkSharp

  * <https://github.com/grbd/GBD.Blog.Examples>

There were four main options I looked into

  * WinForms
  * QtSharp
  * Eto.Forms
  * GtkSharp

## WinForms

![winformsimg]({filename}/static/code/gtksharp.1.toolkits/WinForms1.png)

Winforms is traditionally the toolkit used by Microsoft for .Net / with Visual Studio, it dates back to the good old VB6 days.
The Xamarin and mono team have put a lot of work into making sure that that this toolkit can run on both windows and Linux via mono.
However, when you google Winforms and cross compatibility it looks as if the main focus is now on GTK instead as the main alternative.
The one main advantage to Winforms is that it's designable via Visual Studio's inbuilt GUI. Upon googling most of the opinions online, the code base has been largely untouched for a long while on the mono side.

## QtSharp

![QtFormImage]({filename}/static/code/gtksharp.1.toolkits/QtForm1.png)

Qt for me has the best looking toolkit, also it has QML which is a form of descriptive language for describing the layout of forms similar in some respects to Xaml.
There's been a few different attempts at a .Net binding for Qt, first there was a very old project called QtSharp, then another project
to replace that one called Qyoto which seems to have now been abandoned, and finally the latest incarnation which has re-used the name of QtSharp.

QtSharp uses the CppSharp library as a way of generating the bindings from the c++ Qt libraries into the .Net space.
At this stage it's still very new and in alpha state, after testing it myself it does appear to actually be able to create and show windows, however there are a couple of gotcha's still.

  * The code is still in Alpha state, which means it may be a while before it's ready for production
  * Currently CppSharp doesn't support templated functions (c++ generics) so certain function calls and properties are currently unavailable (such as iterating over the child controls within a form or container)
  * QML based apps are going to require some special coding before they can be used from .Net

I'm still hopeful this will be useful in the future since I'm quite keen on Qt. Looking at some of the c++ projects online there seems to have been a lot of talk of projects moving from Gtk to Qt due to issues with the newer versions of Gtk and it being largely Gnome focused.
For now, it still needs a lot of work however.

For some example code to experiment with QtSharp

  * <https://github.com/grbd/QtSharp.TestApps>

You may also want to check out the official repositories
(the gitlab repo is the most up-to-date one)

  * <https://github.com/mono/CppSharp>
  * <https://gitlab.com/ddobrev/QtSharp>
  * <https://github.com/ddobrev/QtSharp>

## Eto.Forms

![EtoFormsImg]({filename}/static/code/gtksharp.1.toolkits/EtoForm1.png)

Eto.Forms was the next toolkit I looked into.
It's basically a wrapper that sits on top of other toolkits such as windows forms, GtkSharp, WPF, etc.
It's one advantage is that it has the ability to create forms based on Xaml similar to WPF Forms

There are a couple of downsides though


  * The range of controls for containers is still a bit limited
  * Currently there's no GUI / drag and drop designer, but there is a window to preview the rendered Xaml

## GtkSharp

![GtkSharpImg]({filename}/static/code/gtksharp.1.toolkits/GtkSharp1.png)

The final toolkit I tried looking into was GtkSharp. This seems to be a lot more mature than the other toolkits in relation to .Net with bug fixes and patches.
There does seem to be a bit of confusion over which version to use and how to set it up.
After a fair bit of digging around online I finally managed to figure out how to get a basic GTK3 based GtkSharp Application up and running
under .Net. Given that some of the documentation is still a bit sparse when it comes to the GTK3 version I figured I'd put some information
up on how to get it going with Visual Studio.

One advantage to GtkSharp which I'm also interested in is the use of cairo for vector graphics, there's also some unofficial methods of getting it to work with Monogame which is a cross platform 3D library originally based on XNA.

  * [GTK-Sharp](http://www.mono-project.com/docs/gui/gtksharp/) - The Main .Net library for creating GTK based GUI Applications
  * [GLIB-Sharp](https://developer.gnome.org/glib/2.46/) - Glib Sharp is a library used by GTK for Core Functionality such as memory management
  * [GDK-Sharp](https://en.wikipedia.org/wiki/GDK) - Gimp Drawing Kit, this is a low level drawing library used by GTK for graphics rendering
  * [GIO-Sharp](https://developer.gnome.org/gio/2.47/) - The Gio library deals with low level Gnome IO for File system / Network / Process Handling / DBUS / Application Settings

  * [Cairo-Sharp](http://www.mono-project.com/docs/tools+libraries/libraries/Mono.Cairo/) - Cairo can be used for 2D Vector graphics
  * [Pango-Sharp](http://www.mono-project.com/archived/pangobeginners/) - pango handles all of the font and text related functions for GTK
  * ATK-Sharp - atk deals with accessibility
  * [Open-GL with Cairo](http://cairographics.org/OpenGL/)

## GTK Versions

After a bit of digging around online there appears to be two versions of GtkSharp available at the moment.
One for GTK2 and one for GTK3

### GTK2

The one for GTK2 is probably more stable and widely used, but the one I'm interested in here is the GTK3 version.
If you look for the default windows .msi installer on the mono site

  * [MSI Instaler](http://www.mono-project.com/docs/gui/gtksharp/installer-for-net-framework/)
  * [Main Download URL](http://www.mono-project.com/download/#download-win)

This is actually the older GTK2 version which installs under "C:\Program Files (x86)\GtkSharp\2.12\" on Windows.
The official GitHub account for GtkSharp seems to mirror this (latest version 2.12.30)

  * <https://github.com/mono/gtk-sharp/>

### GTK3

If you look for the NuGet packages online [NuGet Link](https://www.nuget.org/packages?q=gtk-sharp).
As far as I can tell I think these versions are unofficial (although quite useful)

  * GtkSharp (3.1.3) - GTK3 .Net libraries
  * GtkSharp.Win32 - GTK3 C libraries for Windows
  * GtkSharp.Linux - GTK3 C libraries for Linux

This is the version I'll be using in the following articles.
I suspect although I'm not entirely sure that the source code for this version is based on the below GitHub Link.

  * <https://github.com/openmedicus/gtk-sharp>

<br>
[Part 2 - Setting up Glade]({filename}./gtksharp.2.glade.md)
