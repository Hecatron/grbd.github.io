Title: GTKSharp - Part 3 - Basic Example with VS and Glade
Summary: Using GTKSharp version 3 within Visual Studio under windows
Date: 2016-06-25 19:36
Tags: code, dotnet, gtksharp

## Overview

It's been a while since I posted my last blog entry so I decided to get a crack on with this one

In this post I'm going to show how to get a basic GtkSharp application working using a glade xml file and some C#. <br>
For the below examples the code is downloadable via a github link: <https://github.com/grbd/GBD.Blog.Examples>


## GtkSharp BasicForm1 Example

### Setting up the Project

First lets create a new C# Solution

![NewSolution1]({filename}/static/code/gtksharp.3.example1/NewSolution1.png)

Next lets create a new C# Windows Forms Project

![NewProject1]({filename}/static/code/gtksharp.3.example1/NewProject1.png)

We don't need Form1.cs since we're repurposing this project for GtkSharp, so lets remove Form1.cs

![RemoveFrom1cs]({filename}/static/code/gtksharp.3.example1/RemoveFrom1cs.png)

Next right click on the project and select *Manage Nuget Packages*

Lets add the NuGet packages for GtkSharp and GtkSharp.Win32 (if using windows).
Within NuGet the gtksharp package uses the gtk3 version of gtk. The GtkSharp.Win32 represents the non .net windows binaries we also need.
If your using linux and already have gtk installed then the additional binaries shouldn't be needed.

![NuGet1]({filename}/static/code/gtksharp.3.example1/NuGet1.png)

Next we want to make sure the project is running as 32bit, the package GtkSharp.Win32 only contains 32bit binaries at the moment

  * Right click on the project
  * Select **Properies** from the drop down menu
  * Select the **Build** tab on the left hand side
  * Make sure the **Platform Target** is set to **X86**

![ProjectProperties1]({filename}/static/code/gtksharp.3.example1/ProjectProperties1.png)

The dotnet version will default to **4.5.1**, you can leave it at that or increase it to a higher version such as 4.5.2, 4.6 or 4.6.1


### Setting up the Program Class

Next we need to alter the code that runs at startup. <br>

With Visual Basic you'll need to create a Program.vb file <br>
With C# There should already be a Program.cs file we can use instead

  * Within the project properties make sure that the Program class is selected
  * If you are using Visual Basic, then you will need to untick the option for **Enable Application Framework**

![ProjectProperties2]({filename}/static/code/gtksharp.3.example1/ProjectProperties2.png)

These are some examples of what the main Program class should look like

**For C#**

``` csharp
using System;
using Gtk;

namespace ExampleApp1 {
    /// <summary> A program. </summary>
    static class Program {
        /// <summary> The main entry point for the application. </summary>
        [STAThread]
        static void Main() {
            Application.Init();
            TestForm1 win = TestForm1.Create();
            win.Show();
            Application.Run();
        }
    }
}
```

**For Visual Basic:**

``` vbnet
Imports Gtk

Namespace App

    ''' <summary> A program. </summary>
    Public Class Program

        ''' <summary> Main entry-point for this application. </summary>
        Public Shared Sub Main()
            Application.Init()
            Dim win As TestForm1 = TestForm1.Create()
            win.Show()
            Application.Run()
        End Sub

    End Class

End Namespace
```


### TestForm1.glade

Next lets create a glade form to use in our project <br>
This is one created from the glade application we've used before.

  * Drag and drop the file saved from glade into the project
  * Make sure to set the **Build Action** to **Embedded Resource** for the glade file

![GladeFile1]({filename}/static/code/gtksharp.3.example1/GladeFile1.png)

The next thing to be aware of is that the resource path changes somewhat based on if your using a C# or VB based project

  * With VB The resource path is *&lt;AssemblyName&gt;.&lt;FileName&gt;*
  * With C# The resource path is *&lt;AssemblyName&gt;.&lt;Directory&gt;.&lt;FileName&gt;*

In this case since it's a C# Project and the file is in the root of the project. <br>
The full resource name is *ExampleApp1.TestForm1.glade*

It's also possible to associate the .glade file with the glade.exe by right clicking on it within Visual Studio and selecting *Open With*

**TestForm1.glade**
```
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.19.0 -->
<interface>
  <requires lib="gtk+" version="3.14"/>
  <object class="GtkWindow" id="window1">
    <property name="can_focus">False</property>
    <child>
      <object class="GtkFixed" id="fixed1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <child>
          <object class="GtkButton" id="SendButton">
            <property name="label" translatable="yes">button</property>
            <property name="width_request">91</property>
            <property name="height_request">40</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
          </object>
          <packing>
            <property name="x">11</property>
            <property name="y">8</property>
          </packing>
        </child>
        <child>
          <object class="GtkEntry" id="StdInputTxt">
            <property name="width_request">168</property>
            <property name="height_request">80</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
          </object>
          <packing>
            <property name="x">9</property>
            <property name="y">60</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
```

### TestForm1.cs

The original GTK2 based version of GTKSharp used to include a library called Glade-Sharp which handled the loading in of
forms via Glade.XML, with the newer GTK3 version this is handled via the GTK.Builder class instead.

With the below example we're going to use the **Builder.Object** attribute.
This attribute automatically links the named property to the control on the form once it's shown.
Once the property is linked to the form we can then attach to it's events or change it's properties such as a textbox text value

**TestForm1.cs**

**For C#**

``` csharp
using System;
using Gtk;

namespace ExampleApp1 {
    
    /// <summary> Example Test Form for GTKSharp and Glade. </summary>
    public class TestForm1 : Window {
        #region Properties

        /// <summary> Used to load in the glade file resource as a window. </summary>
        private Builder _builder;

#pragma warning disable 649

        /// <summary> Connects to the SendButton on the Glade Window. </summary>
        [Builder.Object]
        private Button SendButton;

        /// <summary> Connects to the InputText Control on the Glade Window. </summary>
        [Builder.Object]
        private Entry StdInputTxt;
#pragma warning restore 649

        #endregion

        #region Constructors / Destructors
        /// <summary> Default Shared Constructor. </summary>
        /// <returns> A TestForm1. </returns>
        public static TestForm1 Create() {
            Builder builder = new Builder(null, "ExampleApp1.TestForm1.glade", null);
            return new TestForm1(builder, builder.GetObject("window1").Handle);
        }

        /// <summary> Specialised constructor for use only by derived class. </summary>
        /// <param name="builder"> The builder. </param>
        /// <param name="handle">  The handle. </param>
        protected TestForm1(Builder builder, IntPtr handle) : base(handle) {
            _builder = builder;
            builder.Autoconnect(this);
            SetupHandlers();
        }

        #endregion

        #region Handlers

        /// <summary> Sets up the handlers. </summary>
        protected void SetupHandlers() {
            DeleteEvent += OnLocalDeleteEvent;
            SendButton.Clicked += OnSendClick;
        }

        /// <summary> Handle Close of Form, Quit Application. </summary>
        /// <param name="sender"> Source of the event. </param>
        /// <param name="a">      Event information to send to registered event handlers. </param>
        protected void OnLocalDeleteEvent(object sender, DeleteEventArgs a) {
            Application.Quit();
            a.RetVal = true;
        }

        /// <summary> Handle Click of Button. </summary>
        /// <param name="sender"> Source of the event. </param>
        /// <param name="a">      Event information to send to registered event handlers. </param>
        protected void OnSendClick(object sender, EventArgs a) {
            StdInputTxt.Text = "Hello World";
        }

        #endregion

    }
}
```

**For Visual Basic:**

``` vbnet
Imports Gtk

''' <summary> Example Test Form for GTKSharp and Glade. </summary>
Public Class TestForm1
    Inherits Window

#Region "Properties"

    ''' <summary> Used to load in the glade file resource as a window. </summary>
    Private _builder As Builder

    ''' <summary> Connects to the SendButton on the Glade Window. </summary>
    <Builder.Object>
    Private SendButton As Button

    ''' <summary> Connects to the InputText Control on the Glade Window. </summary>
    <Builder.Object>
    Private StdInputTxt As Entry

#End Region

#Region "Constructors / Destructors"

    ''' <summary> Default Shared Constructor. </summary>
    ''' <returns> A TestForm1. </returns>
    Public Shared Function Create() As TestForm1
        Dim builder As New Builder(Nothing, "GtkSharp_BasicForm1_VB.TestForm1.glade", Nothing)
        Return New TestForm1(builder, builder.GetObject("window1").Handle)
    End Function

    ''' <summary> Specialised constructor for use only by derived class. </summary>
    ''' <param name="builder"> The builder. </param>
    ''' <param name="handle">  The handle. </param>
    Protected Sub New(builder As Builder, handle As IntPtr)
        MyBase.New(handle)
        _builder = builder
        builder.Autoconnect(Me)
        SetupHandlers()
    End Sub

#End Region

#Region "Handlers"

    ''' <summary> Sets up the handlers. </summary>
    Protected Sub SetupHandlers()
        AddHandler DeleteEvent, AddressOf OnLocalDeleteEvent
        AddHandler SendButton.Clicked, AddressOf OnSendClick
    End Sub

    ''' <summary> Handle Close of Form, Quit Application. </summary>
    ''' <param name="sender"> Source of the event. </param>
    ''' <param name="a">      Event information to send to registered event handlers. </param>
    Protected Sub OnLocalDeleteEvent(sender As Object, a As DeleteEventArgs)
        Application.Quit()
        a.RetVal = True
    End Sub

    ''' <summary> Handle Click of Button. </summary>
    ''' <param name="sender"> Source of the event. </param>
    ''' <param name="a">      Event information to send to registered event handlers. </param>
    Protected Sub OnSendClick(sender As Object, a As EventArgs)
        StdInputTxt.Text = "Hello World"
    End Sub

#End Region

End Class
```

### Running the Application

If we now build and run the project, this should result in a window like this.

![Example1]({filename}/static/code/gtksharp.3.example1/Example1.png)

The button just puts *Hello World* into the text box

<br>
[Part 2 - Setting up Glade]({filename}./gtksharp.2.glade.md)<br>
[Part 4 - Handles and WithEvents Example]({filename}./gtksharp.4.example2.md)
