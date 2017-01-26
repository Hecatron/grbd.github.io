Title: Logging with LibLog and SeriLog
Summary: Logging with LibLog and SeriLog
Date: 2017-01-25 23:00
Tags: code, dotnet, liblog, serilog


## Overview

For a while now I have been looking into the best way to implement logging within C# Projects.
A while back, I used to be a big fan of NLog, but more recently, I've moved to using LibLog and Serilog

  * <https://serilog.net/>
  * <https://github.com/damianh/LibLog/wiki>

I've put some examples in the below link on github

  * <https://github.com/grbd/GBD.Blog.Examples/tree/master/Source/LibLog>


## LibLog

When it comes to libraries, you do not always know who is going to be using the library, if it's part of a large team or open to the world.
So ideally, you want to avoid a dependency on a specific Logging library in case someone wants to use a different Logging implementation
Alternatively, if it needs to change later to a different logging framework.

One of the first abstractions in use was Common.Logging, however it lacks support for outputting structured data such as Serilog.
Next is liblog, with liblog you actually embed a blob of code into the library.
This code then picks up which logging abstraction is in use by the application and writes to it via some clever reflection code.
Below are some links that also explore using liblog with Serilog

  * <https://tonytalks.technology/logging-with-serilog-liblog-and-seq-a68f9fca7301#.e40211sux>
  * <http://lunarfrog.com/blog/net-open-source-netstandard-logging-using-liblog>

From what I can gather, the reason for including the liblog code directly into the library instead of as an external reference is to avoid dependencies on different versions of liblog between different libraries that might be part of a larger project.


### Setup .Net

With traditional .csproj projects, we can use a NuGet package to incorporate the code into the project
This uses a feature of NuGet called ContentFiles to copy the code.
This method seems to be the simplest way to set things up, also it allows for the code to be auto namespaced and be upgradable via NuGet.

  * <https://www.nuget.org/packages/LibLog/>

### Setup .Net Core

For .xproj type projects, the setup is a little more involved.
Currently there is no support for NuGet ContentFiles with .xproj / project.json based projects at the moment so we need to copy in the code manually.
Once Visual Studio 2017 comes out and everything moves back to .csproj type projects this might change.

  * <https://github.com/damianh/LibLog/issues/35>

First, we need to add a definition to out project.json file to allow LibLog to work with this type of framework

``` json
  "buildOptions": {
    "define": [ "LIBLOG_PORTABLE" ]
  },
```

Next, we need to copy in the liblog source code manually into the project. <br>
The latest version of the liblog source can be located here

  * <https://github.com/damianh/LibLog/blob/v4.2.6/src/LibLog/LibLog.cs>

Copy this file into a location within the project; typically, Nuget installs it into <br>
**App_Packages/LibLog.4.2/LibLog.cs**


Next, we need to make some modifications to the namespace within the Liblog.cs file. <br>
Replace **YourRootNamespace** with the namespace of the library / application.

At the top of the file
``` csharp
// If you copied this file manually, you need to change all "YourRootNameSpace" so not to clash with other libraries
// that use LibLog
#if LIBLOG_PROVIDERS_ONLY
namespace YourRootNamespace.LibLog
#else
namespace YourRootNamespace.Logging
#endif
{
    using System.Collections.Generic;
    using System.Diagnostics.CodeAnalysis;
#if LIBLOG_PROVIDERS_ONLY
    using YourRootNamespace.LibLog.LogProviders;
#else
    using YourRootNamespace.Logging.LogProviders;
#endif
```

Mid way down the file as well
``` csharp
#if LIBLOG_PROVIDERS_ONLY
namespace YourRootNamespace.LibLog.LogProviders
#else
namespace YourRootNamespace.Logging.LogProviders
#endif
```


### Example

For an example of how to call LibLog within code.

``` csharp
public class MyClass
    {
        private static readonly ILog Logger = LogProvider.GetCurrentClassLogger();
 
        public void DoSomething()
        {
	    // Basic Logging
            Logger.Info("Method 'DoSomething' in progress");

            // To take advantage of Serilog's Structured data logging
            var position = new { Latitude = 25, Longitude = 134 };
            var elapsedMs = 34;
            Logger.InfoFormat("Liblog {MethodName} Entry", nameof(Program));
            Logger.InfoFormat("Liblog: {@Position} .. {Elapsed:000}", position, elapsedMs);
        }
    }
```

One thing to be aware of when using LibLog is that when calling

``` csharp
private static readonly ILog LibLogger = LogProvider.GetCurrentClassLogger();
```

It is important that the Serilog Configuration is setup before this is called.
Therefore, if the above property is located within the main Program class and Serilog has not yet been setup then no logging can be done via the LibLogger property.


## Serilog

When it comes to outputting the logs to the outside world, we need some sort of logging framework to handle this.
Liblog is setup in such a way that the library it is a part of does not need to care which logging system the end user is using.
So the general gist of it is, is that you reference Serilog (or another logging framework) within the Application or website that is actually using the library.
This way Serilog handles the actual output to the outside world.


### Structured Data

There is a few different logging environments available.
Serilog is a new contender in that it has the advantage of logging fields instead of just a string; they tend to refer to this as Structured Data.

``` csharp
var position = new { Latitude = 25, Longitude = 134 };
var elapsedMs = 34;
log.Information("Processed {@Position} in {Elapsed:000} ms.", position, elapsedMs);
```

At a later stage, we can capture the fields such as Elapsed or Position and insert them into a database table as one example.
This can come in handy as it avoids the need to manipulate strings when extracting information from a single log entry.


### Sinks

Serilog has the concept of sinks; a Sink is a destination for the logged output. One example might be a coloured console output, another a database table or a syslog server.

For console output the two main ones are

  * **Serilog.Sinks.Literate**
  * **Serilog.Sinks.ColoredConsole**

(My preference tends to be the literate one)

### Example

This is an example of logging directly via Serilog, although any log entries generated by liblog should also pick up on the Serilog logger that's been setup.

``` csharp
using System;
using Serilog;
 
namespace TestApp1 {
    class Program {
        static void Main(string[] args) {
 
            Log.Logger = new LoggerConfiguration()
                .MinimumLevel.Verbose()
                .WriteTo.LiterateConsole()
                .CreateLogger();
 
            Log.Logger.Verbose("Test Verbose Message...");
            Log.Logger.Information("Test Info Message...");
            Log.Logger.Debug("Test Debug Message...");
            Log.Logger.Warning("Test Warning Message...");
            Log.Logger.Error("Test Error Message...");
            Log.Logger.Fatal("Test Fatal Message...");
 
            Console.ReadKey();
        }
    }
}
```

## Capturing Logs

I haven't really explored this one yet but one way to capture log entries in a nice GUI is the use of GetSeq


  * <https://getseq.net/>

