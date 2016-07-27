Title: Setup Mono as a .Net Framework in Visual Studio
Summary: Registering the mono framework under windows, and how the different versions of mono compare against the standard .net framework versions
Date: 2016-01-29 18:00
Tags: toolkits, mono
status: draft

I think this might be the easiest way to get cross platform vb apps to run
this way we don't need to compile on the RPI

https://erictummers.wordpress.com/2012/01/25/target-mono-from-visual-studio/

## Install Mono

1. Install latest mono
http://www.mono-project.com/download/#download-win

## Register Mono .Net version 4.0

2. Next we're going to register the mono framework in Visual Studio's list of frameworks

Copy C:\Program Files (x86)\Mono\lib\mono\4.0 -> C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.0\Profile\mono
(Copy and paste the 4.0 directory to Profile, then rename it to mono

Within the directory C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.0\Profile\mono
Create a subdirectory RedistList, within this create a file FrameworkList.xml with the following content
change the version number to whichever version of mono your using

<?xml version="1.0" encoding="UTF-8"?>
<FileList ToolsVersion="4.0" RuntimeVersion="4.0" Name=".NET Framework 4 Mono Profile" Redist="Mono_4.0"> 
</FileList>

Next create a .reg file with the following content
(each entry is for if you run a x32 or x64 app)

[HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\.NETFramework\v4.0.30319\SKUs\.NETFramework,Version=v4.0,Profile=Mono]
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework\v4.0.30319\SKUs\.NETFramework,Version=v4.0,Profile=Mono]


## Register Mono .Net version 4.5

.Net 4.6 appears to be not available for windows xp
but I belive is compatible with mono 4.0 and above

Copy C:\Program Files (x86)\Mono\lib\mono\4.5 -> C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.6.1\Profile\mono
(Copy and paste the 4.5 directory to Profile, then rename it to mono

Within the directory C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.6.1\Profile\mono
Create a subdirectory RedistList, within this create a file FrameworkList.xml with the following content
change the version number to whichever version of mono your using

<?xml version="1.0" encoding="UTF-8"?>
<FileList ToolsVersion="4.0" RuntimeVersion="4.5" Name=".NET Framework 4.5 Mono Profile" Redist="Mono_4.5"> 
</FileList>

Next create a .reg file with the following content
(each entry is for if you run a x32 or x64 app)

[HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\.NETFramework\v4.0.30319\SKUs\.NETFramework,Version=v4.6.1,Profile=Mono]
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework\v4.0.30319\SKUs\.NETFramework,Version=v4.6.1,Profile=Mono]

## Project References

For any warnings about System.Deployment, remove the reference from your list of references since mono doesn't have it


