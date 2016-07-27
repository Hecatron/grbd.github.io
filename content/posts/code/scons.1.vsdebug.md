Title: SCons builds with Visual Studio
Summary: SCons builds with Visual Studio 
Date: 2016-07-27 18:53
Tags: code, SCons, build

## Overview

For a while now I've been looking for a decent build system with a language I can easily write and debug.

During the very old days of Linux the main go to for a build system typically was *make* and *configure*.
Configure would check the system to see if a library was present and its location,
Make would use Makefile scripts to handle the actual compilation based on the results from configure.
Surrounding these two was autotools which included autoconf and automake to try and make writing these sorts of scripts a lot easier.
However, over time because of cross compatibility reasons, if you were new to this sort of thing, it could quite quickly become a rat's nest of code.

Then came along CMake, CMake is a meta language in that it generates Make files in a similar fashion to autoconf and automake but all rolled into one
with an easier to use language and syntax.
CMake has now taken over as one of the more popular build systems since it's also windows and cross platform compatible.

However personally I've never been that fond of CMake

  * It has no fixed API for hooking into, forcing you to use the CMake language
  * The CMake language while very cross platform lacks features (such as class's for example)
  * You can't step through the code / build script with a debugger (I could be wrong on this one, but I've not found one)

I should point out there does appear to be an upcoming feature called server mode that may allow for some form of API access in the future

## SCons / Cuppa

This is where SCons and Cuppa comes in.

I've placed an example over on my GitHub account <https://github.com/grbd/GBD.Blog.Examples/tree/master/Source/SconsBuild>

In the past I've dabbled in a large number of different languages.
Currently my two favourites are .Net and python, the reason being they're debuggable via Visual Studio.
I've found that python makes for a very good scripting language, you can also easily debug it, add break points, get auto completion features etc.
In the open source world pycharm is one of the favourites for debugging python code this offers a lot of similar features.
My personal favourite though is the latest Visual Studio 2015 with python tools.
With VS Python tools we can get all the good auto completion features and can debug / step code to our hearts content.

SCons is a python based build system, unlike CMake it doesn't generate make files in that it handles the build itself.
One of the main benefits of python is that it has a vast library of supporting code.
To give an example if I'm planning on writing a VC++ Visual Studio project but want to make it cross platform.
One approach might be to write the code using a VS project file, but for the build process read in the xml using python / SCons, then parse it to generate the build via SCons.
Or I could do it the other way around and have a VS Project file generated from a simple python block of code that lists all the source files.
python gives us a great deal of power to do interesting things not normally possible in other build systems.

### Cuppa

Cuppa is an extension to SCons in that is possess some features that allow easier building of VC++ projects.
I haven't gotten around to exploring Cuppa just yet, but to install it under windows.

First you'll need to install lxml, this doesn't seem to be installable via pip directly under windows.
But we can get a pre-packaged whl file from this site <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>

In my case since I'm using python 2.7 64bit, so I downloaded the *lxml-3.6.1-cp27-cp27m-win_amd64.whl* file. <br>
After downloading it should just be a case of using pip from a command prompt to install the lxml package.

``` sh
pip install lxml-3.6.1-cp27-cp27m-win_amd64.whl
```

Next we can install cuppa using pip

``` sh
pip install cuppa
```

I've included some links below for some more information. <br>
The below example does not use Cuppa, as I'm just focusing on debugging the build script with Visual Studio for the below.

  * <https://github.com/ja11sop/cuppa>
  * <https://www.youtube.com/watch?v=h_HhBT6xGeE>


## Code Example

In the below example I'm going to show how I managed to debug a SCons python file (SConstruct) within Visual Studio using Python Tools

### hello1.c

First let's create a very simple hello world program called **hello1.c**

``` c
#include<stdio.h>

int main()
{
	printf("Hello, world!\n");
	return 0;
}
```

### SConstruct files

Visual Studio recognises python files based on the extension of .py
The SConstruct python script files that SCons looks for lacks this extension which creates a problem.
One way around this is to use two files

**SConstruct**
```python
execfile('SConstruct.py')
```

**SConstruct.py**
```python
#!python

# These import lines are not really needed, but it helps intellisense within VS when editing the script
import SCons.Script
from SCons.Environment import Environment

# For a more detailed / cross platform build script see
# https://bitbucket.org/scons/scons/wiki/AllInSConstruct

print "Building Hello1.c"
env = Environment()

# Add the Debug Flags if debug=1 is specified on the command line, this tends to be compiler specific
if ARGUMENTS.get('debug', 0):
    env.Append(CPPDEFINES = ['DEBUG', '_DEBUG'])
    env.Append(CCFLAGS='/MDd')
    env.Append(CCFLAGS=Split('/Zi /Fd${TARGET}.pdb'))
    env.Append(LINKFLAGS = ['/DEBUG'])
    variant = 'Debug'
else:
    env.Append(CPPDEFINES = ['NDEBUG'])
    variant = 'Release'

print "Building: " + variant

# Create a hello1.exe from the c file
t = env.Program(target='src/hello1', source=['src/hello1.c'])
Default(t)
```

The first file SConstruct is read in by the SCons tool initially, this just has a single line of code which basically says read in and process SConstruct.py.
The SConstruct.py file is where all of our build logic is stored, this is the file we'll be editing and using within Visual Studio

Note that SCons automatically imports SCons.Script before running the script, I've included it anyway just to help out with VS Intellisense


## Setting up the Visual Studio files for the Build

Next we're going to setup a VS Solution and Project file to debug the build script

  * Create a sub directory of **vs**
  * Create a new Solution, call it something like **BuildSolution**
  * Create a new Python Application project, call it something like **SConsBuild**
  * Right click on the project, and select Project Properties

### General Tab

Next we're going to set a couple of options under the **General Tab**

  * Set the start-up script to **C:\Python27\Scripts\scons.py**, this path may be different based on your python install.<br>
    Visual Studio needs to use absolute paths for this option.
  * Set the working directory to the location of the SConstruct file / root of the source project, this can be a relative path such as **..\\..** <br>
    The path should be relative to the location of the project file.
  * Make sure to set the python interpreter to Python2, such as **Python 64-bit 2.7** <br>
    SCons does not yet support python3

![GeneralProps1]({filename}/static/code/scons.1.vsdebug/GeneralProps1.png)

### Debug Tab


Next looking at the **Debug Tab**

  * Set the search paths ..\\..\\;C:\Python27\Lib\site-packages\scons-2.5.0

The search path needs to include the relative path to where the SConstruct file is located.
Also it needs to include the directory for the SCons installation, I found this is needed to get Intellisense working with the script.
It looks as if SCons has deliberately put the library files within a SCons subdirectory in the site-packages install directory for python.
I suspect this has been done to avoid users from calling the SCons library directly without first going via the main scons.py script.

![DebugProps1]({filename}/static/code/scons.1.vsdebug/DebugProps1.png)

### Build file link

Finally, we just need to add in the **SConsBuild.py** file as a Link to the project.
By adding it as a link we avoid creating a 2nd copy under the VS Project directory, and when we edit the file we'll be editing the one in the original location.

![AddLink1]({filename}/static/code/scons.1.vsdebug/AddLink1.png)

### Note about Intellisense

Just a quick note, sometimes after creating a new project, you need to right click unload, then re-load the project within Visual Studio to get the Intellisense working correctly


## Setting up the Visual Studio files for the hello code

For the **hello1.c** file within the blog example code I also setup a Visual Studio Project.
This allowed me to edit the code from within Visual Studio and trigger the build process from there as well.

In order to do this, you're going to want to use a *Makefile* style Visual Studio Project. These types of projects allow for custom build tools to be specified instead of using the inbuilt MS build tools. In this case we're going to set it to use the SCons tool to handle the building and cleaning of the project.

After creating one of these types of Project, if you open up the project properties you'll notice the Configuration Type is listed as *Makefile*

![Hello1_General]({filename}/static/code/scons.1.vsdebug/Hello1_General.png)

The import part that we need to alter is located under the NMake tab.
The debug=1 is just an option we can pass to the SCons script to indicate if it's a Release or Debug Build

  * **Build: scons -C ..\\.. debug=1**
  * **Rebuild All: scons -C ..\\.. -c && scons -C ..\\.. debug=1**
  * **Clean: scons -C ..\\.. -c**
  * **Destination exe: ..\\..\\src\\hello1.exe**

![Hello1_NMake]({filename}/static/code/scons.1.vsdebug/Hello1_NMake.png)


## Debugging the build script

I've not really covered any of the details on using the SCons API at this stage simply because I'm still learning it myself.
But if everything has been setup correctly we should now be able to run / debug the SCons build script within Visual Studio.
For a script as simple as this one it's probably not worth the time and effort to set something like this up, but for a much more complex project
finding problems and issues with the build scripts can be a made a lot easier when you can single step the code within the build script itself.

This is really more of a convenience than anything else, you can still edit the build scripts independently of Visual Studio,
and it's likely you could setup something very similar using pycharm (the free open source equivalent to VS Python Tools).
But for me at least this should make life a lot easier for cross platform or even cross compiling complex builds.

