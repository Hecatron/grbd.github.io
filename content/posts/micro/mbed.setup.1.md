Title: Using the Mbed CLI
Summary: Building mbed projects
Date: 2016-11-06 18:00
Tags: micro, mbed, mbed-cli

## Overview

I've recently been looking into the use of mbed for building embedded related projects.
It turns out they've made building code against they're library very easy with a small tool called the mbed-cli.
Mbed-cli is a python script that can be used to handle compiling / library dependency resolution / settings etc. for building projects.

I'm hoping that I might be able to get this working with Visual Micro at some stage so that I can single step / debug a board using GDB and a J-Link Segger or OpenOCD.
For now, I've attempted to summarise most of the important bits when setting up and using the mbed-cli tool.


## Installation

To get everything needed installed, we need to install the following.

  * Install the latest python 2.x version and make sure python is in your path - <https://www.python.org/downloads/>
  * Install the latest git and make sure git is in your path - <https://git-scm.com/download/win>
  * Install the latest mercurial and make sure the hg command is in your path - <https://www.mercurial-scm.org/downloads> <br>
    (some mbed libs use Mercurial)
  * Install gcc for arm, towards the end of the install make sure to select to add the tools to the path via the tick box - <https://launchpad.net/gcc-arm-embedded>
  * Finally install the python script mbed-cli via "pip install mbed-cli"

They recommend using a gcc version of around 4.9 or so (although I've been trying stuff out with the latest one)

These are some of the links that relate to the install

  * <https://docs.mbed.com/docs/mbed-os-handbook/en/5.1/getting_started/blinky_cli/)>
  * <https://docs.mbed.com/docs/mbed-os-handbook/en/5.1/dev_tools/cli/>
  * <https://www.youtube.com/watch?v=cM0dFoTuU14>


## Project system

Mbed has a concept of it's own project system that it uses via the mbed-cli tool

To create a new directory and set it up as an mbed project
```
mbed new mbed-os-program
```

To turn the existing current directory into an mbed project
```
mbed new .
```

Under the hood I think "mbed new" changes the directory into a git repository with "git init", then uses "mbed add" to add the mbed-os as the base library
and I think a couple of other things.

To download and setup the example project blinky
```
mbed import https://github.com/ARMmbed/mbed-os-example-blinky
```
This is the same as a "git clone", followed by a "mbed deploy", followed by a "mbed new ."



## Libraries

When using libraries within mbed there's two parts

  * A **.lib** file that registers that a library has been used within the project
  * A **directory** that contains the library files / code etc.

When checking code into git / source control the library directory is not checked in (just the .lib file).
This way for a new user that downloads the source code they can run "mbed deploy" which is similar to Nuget restore.
This reads in the .lib files downloads the library content and also resolves any dependencies for other libs that also have to be downloaded.
This avoids having the actual library content sitting in your git repository, and allows you to use custom versions of the library

  * **mbed add** checks for library dependencies and downloads any other libs required.
  * **mbed remove** cleans up any .lib files left over when a library is removed

Example
```
mbed add https://developer.mbed.org/users/wim/code/TextLCD/
mbed remove TextLCD
```

Listing libraries installed
```
mbed ls -a
```


## Configuration

Mbed has several different ways of storing it's configuration which are just key value pairs

  * **Global Settings** (mbed config --global)
  * **Local Settings** (mbed config) - stored in the .lib files
  * **mbed_settings.py** file
  * options passed to **mbed compile**

There's also a mbed_app.json application configuration file which gets expanded into a set of Macros for the compiled application

The three important ones to be aware of are

  * **Target** - this defines a mbed board such as "LPC1768"
  * **Toolchain** - this can be GCC_ARM, ARM, IAR and is just which compiler to use (set to GCC_ARM typically)
  * **Toolchain Path** - this is just the path to the compiler tools
  * <https://docs.mbed.com/docs/mbed-os-handbook/en/5.1/dev_tools/cli/#mbed-cli-configuration>

For example
```
mbed config target LPC1768
mbed toolchain GCC_ARM
mbed config GCC_ARM_PATH "C:\Program Files (x86)\GNU Tools ARM Embedded\5.4 2016q3\bin"
```

To list all settings
```
mbed config --list
```

To set a value
```
mbed config ARM_PATH "C:\Program Files\ARM"
```

To unset a value
```
mbed config --unset ARM_PATH
```


## Compiling

When compiling most of the options can be set via the configuration values above <br>

it's also possible to override some of those settings such as

```
mbed compile -t LPC1768 -t GCC_ARM
```
Which triggers the compile but also overrides the target and compiler to use

  * Macros can be set with the -D option such as "-DUVISOR_PRESENT"
  * A build profile can be set with the --profile option such as "--profile mbed-os/tools/profiles/debug.json"

There are currently 3 build profiles Default, Debug and Small

  * <https://github.com/ARMmbed/mbed-os/blob/master/docs/build_profiles.md>
  * <https://github.com/ARMmbed/mbed-os/blob/master/docs/Toolchain_Profiles.md>

### Compile Options

  * **-m**	Override the target board to use, such as LPC1768
  * **-t**	Override which toolchain target to use, this can be GCC_ARM, ARM, IAR
  * **--source**	Specify the source directory, the default is the current directory.
  * **--build**		Specify the build directory, the default is **BUILD/**
  * **--profile**	This selects the build profile / options to use for the compiler.
  * **--library**	Compile as a static library, .a or .ar
  * **-c**		Do a clean build / rebuild to build from scratch
  * **-j**		Control the number of threads for compiling, default is 0 which uses the number of cores on the machine
  * **--app-config**	Override the path to the application configuration file
  * **--config**	Show the compile time configurations
  * **--prefix**	Filters the output from --config
  * **--supported**	Show list of supported platforms, toolchains
  * **-v -vv**		Verbose Output


## Example Build

```
mbed import https://github.com/ARMmbed/mbed-os-example-blinky
cd mbed-os-example-blinky

mbed config target LPC1768
mbed toolchain GCC_ARM
mbed config GCC_ARM_PATH "C:\Program Files (x86)\GNU Tools ARM Embedded\5.4 2016q3\bin"

# Example of setting for debugging and overriding the target
mbed compile -c -m LPC1768 --profile mbed-os/tools/profiles/debug.json

# End result will be in .\BUILD\LPC1768\GCC_ARM\mbed-os-example-blinky.bin
```
