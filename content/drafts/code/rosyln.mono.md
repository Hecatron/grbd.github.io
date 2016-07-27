Title: Using roslyn
Date: 2016-01-28 21:00
Status: draft

### Testing under Linux

#### Prepring the Sources

first git clone
next remove the line from packages.config within Examples.Process1 for GTK.Win32

Next lets get nuget
wget http://dist.nuget.org/win-x86-commandline/latest/nuget.exe
chmod +x Nuget.exe

Import the mozilla certs
mozroots --import --sync

Next lets restore the dependencies for the solution
mono ./nuget.exe restore solution.sln

#### Building using xbuild

##### Building Project

1. Within Visual Studio remove System.Deployment reference since this isn't present in Mono
2. Within the Project File change ToolsVersion="4.0"
3. move obj and bin to x_obj and x_bin

Next build the project
xbuild
# Override the framework version
xbuild /p:TargetFrameworkVersion="v4.5" GtkSharp3.sln
mono ./whatever.exe

TODO GtkSharp works with C#, but for VB the glade file couldn't be found

##### Depends

http://dlafferty.blogspot.co.uk/2013/08/building-your-microsoft-solution-with.html

1. there seems to be some issues with Nuget in some cases running under linux
https://github.com/NuGet/Home/issues/1448
downloading the deps under windows seems to be the way to go for now at least
also I think the sources section needs to be removed from Nuget.config for roslyn

2. need to make sure mono-basic is installed under gentoo, although is needs to be the newest version (4.0.1)
http://download.mono-project.com/sources/mono-basic/
copying and pasting the ebuild seems to do the trick, this gives us the VB compiler vbnc which can be called during xbuild

3. use layman -a dotnet for latest mono
http://download.mono-project.com/sources/

##### Roslyn

1. based on the roslyn instructions from
https://github.com/mono/roslyn
I've created a package called mono-pcl for the pcl libraries
install this first

It looks like there's a branch in the roslyn mainline called "MonoGac", but I can't get it to work
trying the mono version of roslyn instead
2. download roslyn under windows with
git clone https://github.com/grbd/roslyn.git
cd roslyn

3. if running nuget for the first time
mozroots --import --sync

4. restore packages via Nuget
mono src/.nuget/NuGet.exe restore src/Roslyn.sln
This should download the required packages to the ./packages subdirectory

5. edit the props file as mentioned in the mono roslyn readme, also edit props for vb entries in addition
cp patches/Microsoft.Net.ToolsetCompilers.props packages/Microsoft.Net.ToolsetCompilers.1.0.0-rc1-20150122-03/build/

4. copy to linux
xbuild as in the readme
xbuild src/Tools/Source/FakeSign/FakeSign.csproj
xbuild src/Compilers/CSharp/csc/csc.csproj

5. for vbnc it doesnt appear to support linq
only VB8 not VB9
http://stackoverflow.com/questions/26179560/mac-mono-vb-linq-not-compiling

xbuild src/Compilers/VisualBasic/vbc/vbc.vbproj

src/Tools/Source/CompilerGeneratorTools/Source/VisualBasicSyntaxGenerator/VisualBasicSyntaxGenerator.vbproj
src/Tools/Source/CompilerGeneratorTools/Source/VisualBasicErrorFactsGenerator/VisualBasicErrorFactsGenerator.vbproj



New method

1. emerge clang-3.7.1-r100
make sure the clang, lldb, xml use flags are enabled for llvm
lldb is part of the llvm package

2. emerge dev-util/lttng-tools dev-util/lttng-ust

3. get coreclr
git clone https://github.com/dotnet/coreclr.git

4. run cmake
cd coreclr
mkdir build
cd build
cmake ../ -DCMAKE_BUILD_TYPE:=RELEASE






3. run ./build.sh




1. get latest roslyn source
2. within the Makefile replace the MONO_PATH with
MONO_PATH= /usr/bin/mono

3. install coreclr for arm
mono ./nuget.exe install Microsoft.NETCore.Runtime.CoreCLR-arm -Pre

4. edit build/scripts/crossgen.sh set CROSSGEN_UTIL to
CROSSGEN_UTIL=$HOME/.nuget/packages/Microsoft.NETCore.Runtime.CoreCLR-arm/1.0.1-beta-23504/tools/crossgen



RuntimeIndentifier = x64
BaseNuGetRuntimeIdentifier = ubuntu.14.04
$(BaseNuGetRuntimeIdentifier)-$(RuntimeIndentifier)
ubuntu.14.04-x64


x. run the build script
./cibuild.sh


TODO for kernel may need to replace bootcode.bin on the Noobs partition, and perhaps update the Noobs partition

