Title: Building GTKSharp 3 under Windows - Python Script
Summary: Building GTKSharp 3 under Windows
Date: 2016-01-27 9:00
Tags: dotnet, gtksharp, gtk
Status: draft


TODO Document the Automated / Python Build approach


## TODO

  * Check opengl support is present
  * do we need libsrvg?
  * also we may be able to use the same approach above for libsox

  * look into generation of NuGet packages using a python script
  * Test both x32 and x64 versions of GtkSharp
  * Ideally we need the native libs to be in seperate x32 / x64 directories
    https://msdn.microsoft.com/en-us/library/windows/desktop/hh310513(v=vs.85).aspx
  * As part of the build script look into a .Net Core Build

## TODO 1

I need to create a patch file for gtk\Plug.cs and submit a merge request
there's a couple of instances of socket_id that need to be wrapped with Convert.ToUInt32(socket_id)

