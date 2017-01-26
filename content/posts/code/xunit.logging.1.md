Title: XUnit Unit Tests and Logging - CSProj
Summary: XUnit Unit Tests and Logging - CSProj
Date: 2017-01-25 23:30
Tags: code, dotnet, liblog, xunit, serilog


## Overview

Sometimes for libraries, it's important to be able to test the different parts to see if we get the output we expect. <br>
This might involve running a select on a database via a database library, or just checking that the type of an object returned isn't null. <br>
Unit tests can come in handy when a very important library has had changes made to it and you want to make sure the output is predictable.

The way this works

  * You create a class library to house the tests <br>
    By convention, it's usually named the same as the library being tested but with the word .Tests added to the end of it
  * You add a reference to the library / thing you want to actually test
  * You add a reference to a test framework / such as XUnit to run the tests
  * Within the test library, you can create a bunch of functions grouped by class to do the tests you want to do

There's several different testing frameworks, Microsoft even has their own one built into the framework. <br>
NUnit was a favourite of mine, but this seems to have been replaced by XUnit as one of the more popular ones

  * <http://xunit.github.io/>

I've put some examples in the below link on github

  * <https://github.com/grbd/GBD.Blog.Examples/tree/master/Source/XUnit>


## ITestOutputHelper

One of the ways in which xunit can output logging information for a given test is the use of ITestOutputHelper. 
Within the constructor of a class within the test library, we specify a parameter of ITestOutputHelper.

XUnit will notice this and use some magic called Dependency injection, this will automatically fill in the class needed for Logging output.

``` csharp
using Xunit;
using Xunit.Abstractions;
 
namespace Test1.Log {
    public class TestLog1 {
        private readonly ITestOutputHelper output;
 
        public TestLog1(ITestOutputHelper outputHelper) {
            output = outputHelper;
        }
 
        [Fact]
        public void SomeTest1() {
            output.WriteLine("Hello World");
        }
    }
}
```

ITestOutputHelper is the main pipeline for outputting text to the Visual Studio Test Explorer window (in the Output pane) for XUnit. 
One problem I have spotted with .Net Core xproj libraries setup for testing is that this currently does not seem to work. This is actually a problem with the current Visual Studio tooling for .Net Core instead of XUnit


## Setup of Project

With tests there is no actual single point of entry, this is because the XUnit runner actually handles the running of the tests.
All we need to do is create a bunch of functions with the right attributes and the XUnit runner will auto run all of these functions in parallel in a multi-threaded way (for increased speed).

CSProj is the traditional style of projects normally used with Visual Studio for targeting the original .Net framework. <br>
The first step, is to just create a new C# or VB.Net class library project within a solution

### Add References

Next, we add some references to the project

For testing

  * **xunit** - Testing framework
  * **xunit.runner.visualstudio** - This allows the tests to be picked up by Visual Studio Test Explorer

For Logging

  * **LibLog** - Logging abstraction
  * **Serilog** - Logging Framework
  * **Serilog.Sinks.Observable** - Needed to wire Serilog into XUnit's output
  * **System.Reactive** - Needed by the observable class's within Serilog


### Project Properties

Next, we are going to make a slight change to the project properties

  * Right Click on the Project and select **Properties**
  * Select the **Build** Tab on the left hand side
  * Under Conditional Compilation, symbols add **LIBLOG_PUBLIC**


### Logging Helper

Now we are going to create a class to act as a bridge from Serilog to ITestOutputHelper.
We could if we wanted to also output to other sinks / destinations such as a text file or database table.

Originally sourced from <https://github.com/damianh/CapturingLogOutputWithXunit2AndParallelTests>

**Base/LoggingHelper.cs**
``` csharp
using System;
using System.IO;
using System.Reactive.Linq;
using System.Reactive.Subjects;
using Serilog;
using Serilog.Context;
using Serilog.Events;
using Serilog.Formatting.Display;
using Xunit.Abstractions;
 
namespace Test1.Base {
    internal static class LoggingHelper {
        private static readonly Subject<LogEvent> s_logEventSubject = new Subject<LogEvent>();
        private const string CaptureCorrelationIdKey = "CaptureCorrelationId";
 
        private static readonly MessageTemplateTextFormatter s_formatter = new MessageTemplateTextFormatter(
            "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level}] {Message}{NewLine}{Exception}", null);
 
        static LoggingHelper() {
            Log.Logger = new LoggerConfiguration()
                .WriteTo
                .Observers(observable => observable.Subscribe(logEvent => s_logEventSubject.OnNext(logEvent)))
                .Enrich.FromLogContext()
                .CreateLogger();
        }
 
        public static IDisposable Capture(ITestOutputHelper testOutputHelper) {
            var captureId = Guid.NewGuid();
 
            Func<LogEvent, bool> filter = logEvent =>
                logEvent.Properties.ContainsKey(CaptureCorrelationIdKey) &&
                logEvent.Properties[CaptureCorrelationIdKey].ToString() == captureId.ToString();
 
            var subscription = s_logEventSubject.Where(filter).Subscribe(logEvent => {
                using (var writer = new StringWriter()) {
                    s_formatter.Format(logEvent, writer);
                    testOutputHelper.WriteLine(writer.ToString());
                }
            });
            var pushProperty = LogContext.PushProperty(CaptureCorrelationIdKey, captureId);
 
            return new DisposableAction(() => {
                subscription.Dispose();
                pushProperty.Dispose();
            });
        }
 
        private class DisposableAction : IDisposable {
            private readonly Action _action;
 
            public DisposableAction(Action action) {
                _action = action;
            }
 
            public void Dispose() {
                _action();
            }
        }
    }
}
```

### Test Base Class

Next, let's create a base class for our tests

**Base/BaseTest.cs**
``` csharp
using System;
using Test1.Logging;
using Xunit.Abstractions;
 
namespace Test1.Base {
    /// <summary> Used as a Base class for testing. </summary>
    public class BaseTest : IDisposable {
 
        protected readonly ILog Logger;
        protected readonly ITestOutputHelper output;
        protected readonly IDisposable _logCapture;
 
        /// <summary> Constructor. </summary>
        /// <param name="outputHelper"> The output helper from XUnit. </param>
        public BaseTest(ITestOutputHelper outputHelper) {
            // Get a hold of the XUnit output
            output = outputHelper;
            // Connects Serilog to the XUnit Output
            _logCapture = LoggingHelper.Capture(outputHelper);
            // Store a reference for LibLog
            // Because this is a base class avoid GetCurrentClassLogger and use GetType().ToString()
            Logger = LogProvider.GetLogger(GetType().ToString());
        }
 
        /// <summary> Cleanup the LoggingHelper. </summary>
        public void Dispose() {
            _logCapture.Dispose();
        }
    }
}
```


### Test Example

Using the Base class, we can now create an example test

  * LibLog is first used to pass in what we want to log
  * This then gets piped to Serilog
  * Serilog then pipes this caross to the XUnit output ITestOutputHelper

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

This might come across as a bit convoluted but at the same time

  * A library does not need to care about anything associated with different logging frameworks by using Liblog
  * Serilog can be used to pipe the results to multiple outputs
  * ITestOutputHelper is just used to pipe the result to the Visual Studio Test output result window.


## Writing Tests


### Fact Testing

The first way of testing is to stick the **Fact** attribute at the top of the test function. <br>
This is used where we don't need to test against a range of parameters typically.

The **Assert** Functions are a way of checking and registering if a test should pass or fail based on if the result of something is False or True

``` csharp
using Xunit;
 
namespace MyFirstUnitTests {
 
    public class Class1 {
        [Fact]
        public void PassingTest() {
            Assert.Equal(4, Add(2, 2));
        }
 
        [Fact]
        public void FailingTest() {
            Assert.Equal(5, Add(2, 2));
        }
 
        int Add(int x, int y) {
            return x + y;
        }
    }
}
```


### Theory Testing

The second way of testing is the use of the **Theory** attribute at the top of the test function. 
This can be used with **InlineData** to run the test function multiple times with different data inputted.

The **Assert** Functions are a way of checking and registering if a test should pass or fail based on if the result of something is False or True

``` csharp
using Xunit;
 
namespace MyFirstUnitTests {
 
    public class Class1 {
     
        [Theory]
        [InlineData(3)]
        [InlineData(5)]
        [InlineData(6)]
        public void MyFirstTheory(int value) {
            Assert.True(IsOdd(value));
        }
 
        bool IsOdd(int value) {
            return value % 2 == 1;
        }
    }
}
```

## Running Tests

To run the tests, just run within Visual Studio

  * Test -> Windows -> Test Explorer 

You'll probably need to build the test project at least once before the tests will show up.


