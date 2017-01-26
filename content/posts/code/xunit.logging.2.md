Title: XUnit Unit Tests and Logging - XProj
Summary: XUnit Unit Tests and Logging - XProj
Date: 2017-01-25 23:40
Tags: code, dotnet, liblog, xunit, serilog


## Overview

Continuing from the last blog entry, I have put here some steps on getting XUnit / .Net Core xproj project and Liblog / Serilog working for a Unit test project.

Typically, these are used with .Net Core, although the next release of Visual Studio 2017 / tooling for Studio 2015 may make some of this obsolete as there are plans to move .Net Core to .csproj based projects

  * <http://xunit.github.io/>

I've put some examples in the below link on github

  * <https://github.com/grbd/GBD.Blog.Examples/tree/master/Source/XUnit>


## Setup of Project

Within Visual Studio, Create a new C# Class Library (.Net Core) Project within a Solution


### project.json

We can make most of the changes we need by directly altering the project.json file

  * The *testRunner* entry tells .net core that we're using XUnit to run the tests
  * The define sections for liblog are required for .Net Core compatibility
  * The framework section specifies that we want to use the .Net Core framework for testing (not the net461 framework)

For the dependencies

For Testing

  * **NETStandard.Library** - Standard Application Library for Core
  * **xunit** - Testing framework
  * **dotnet-test-xunit** - This is the .Net Core equivilent of a runner for the project to run the tests

For Logging

  * **Serilog** - Logging Framework
  * **Serilog.Sinks.Observable** - Needed to wire Serilog into XUnit's output
  * **Serilog.Sinks.Literate** - Coloured Console Output
  * **Serilog.Sinks.ColoredConsole** - Coloured Console Output
  * **System.Reactive** - Needed by the observable class's within Serilog

``` json
{
  "version": "1.0.0-*",
  "testRunner": "xunit",

  "buildOptions": {
    "define": [ "LIBLOG_PORTABLE", "LIBLOG_PUBLIC" ]
  },

  "dependencies": {
    "NETStandard.Library": "1.6.1",
    "dotnet-test-xunit": "2.2.0-preview2-build1029",
    "xunit": "2.2.0-beta5-build3474",
    "Serilog": "2.3.0",
    "Serilog.Sinks.Literate": "2.0.0",
    "Serilog.Sinks.Observable": "2.0.1",
    "Serilog.Sinks.ColoredConsole": "2.0.0",
    "System.Reactive": "3.1.1",
    "System.Reflection.TypeExtensions": "4.3.0"
  },

  "frameworks": {
    "netcoreapp1.1": {
      "dependencies": {
        "Microsoft.NETCore.App": {
          "type": "platform",
          "version": "1.1.0"
        }
      }
    }
  }
}
```


### Liblog

There isn't much point in creating a LoggingHelper class with .Net core since the XUnit output to visual studio isn't currently working yet. But we do need to manually add in LibLog since the NuGet package won't do this for us with project.json based projects.

  * <https://github.com/xunit/xunit/issues/608>

The latest version of the liblog source can be located here

  * <https://github.com/damianh/LibLog/blob/v4.2.6/src/LibLog/LibLog.cs>

Copy this file into a location within the project, typically Nuget installs it into

  * **App_Packages/LibLog.4.2/LibLog.cs**


### Test Base Class

Next, let's create a Base class for our tests to save having to write code when setting up logging. 
Remember to change the namespace and using statements to match up with the name of the class library namespace.

Note this is different from the csproj setup; this is due to a bug with Visual Studio tooling with respect to the Test Explorer. 
To get around this the below just logs to the console instead, but to see the log text output you have to run "dotnet test" at the command line.


**Base/BaseTest.cs**
``` csharp
using System;
using Serilog;
using Test2.Logging;
using Xunit.Abstractions;
 
namespace Test2.Base {
    /// <summary> Used as a Base class for testing. </summary>
    public class BaseTest : IDisposable {
 
        protected readonly ILog Logger;
        //protected readonly ITestOutputHelper output;
        //protected readonly IDisposable _logCapture;
        protected bool SerilogSetup;
 
        /// <summary> Constructor. </summary>
        /// <param name="outputHelper"> The output helper from XUnit. </param>
        public BaseTest(ITestOutputHelper outputHelper) {
            // Get a hold of the XUnit output
            //  output = outputHelper;
            // Connects Serilog to the XUnit Output
            //  _logCapture = LoggingHelper.Capture(outputHelper);
 
 
            // Currently there's problem with preivew2 tooling for Visual Studio 2015 and .Net Core
            // when it comes to capturing output for Tests in the Visual Studio Test Explorer
            // The only way around this currently is to output text to the Console
            // and see it via "dotnet test" at the command line
            if (SerilogSetup == false) {
                // Add [{SourceContext}] to the output so we know which class it is
                var outtemplate =
                "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level}] [{SourceContext}] {Message}{NewLine}{Exception}";
                Log.Logger = new LoggerConfiguration()
                    .MinimumLevel.Verbose()
                    .WriteTo.LiterateConsole(outputTemplate: outtemplate)
                    .CreateLogger();
                SerilogSetup = true;
            }
 
            // Store a reference for LibLog
            // Because this is a base class avoid GetCurrentClassLogger and use GetType().ToString()
            Logger = LogProvider.GetLogger(GetType().ToString());
        }
 
        /// <summary> Cleanup the LoggingHelper. </summary>
        public void Dispose() {
            //_logCapture.Dispose();
        }
    }
}
```

### Test Example

Next lets create an example test to show off how to create a test and log some output

``` csharp
using Test1.Base;
using Test1.Logging;
using Xunit;
using Xunit.Abstractions;
 
namespace Test1.Tests {
    /// <summary> Example of a test Class. </summary>
    public class TestClass1 : BaseTest {
 
        /// <summary> Constructor. </summary>
        /// <param name="outputHelper"> The output helper used by XUnit. </param>
        public TestClass1(ITestOutputHelper outputHelper) : base(outputHelper) {
            // We Capture the Output injected by XUnit for Outputting to Visual Studio
            // and pass it to the Base Class to setup the Logger property for use with LibLog
        }
 
        /// <summary> Example Test. </summary>
        [Fact]
        public void TestLog1() {
            // Example of throwing out some log entries for Visual Studio to pick up on in the output
 
            // This uses LibLog which is independent of the Logging framework
            // Typically this would be used in the library we're testing but we can also use it here as well
            Logger.Warn("LibLog Warning Test");
 
            // Example of checking to see if something is true for a given test
            Assert.True(true);
        }
    }
}
```


## Running Tests

To run the tests, just run within Visual Studio

  * Test -> Windows -> Test Explorer 

You'll probably need to build the test project at least once before the tests will show up.

```
Sometimes after adding all the code to the Visual Studio project, you need to close then re-open Visual Studio.
This seems to be down to the fact that the tooling within Visual Studio for .Net Core projects isn't quite perfect yet
```
