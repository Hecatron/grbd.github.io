Title: GTKSharp - Part 4 - Handles and WithEvents Example
Summary: A second example using GTKSharp and Visual Studio with Handles and WithEvents
Date: 2016-06-25 21:55
Tags: code, dotnet, gtksharp

## Overview

This is a second example of using GtkSharp within Visual Studio. <br>
One of the interesting things we can setup is the use of Handles and WithEvents.
This means that within the code window for the form, we can use the drop down fields in the same way we would with windows forms.

![VSImage]({filename}/static/code/gtksharp.4.example2/VSImage1.png)

![VSImage]({filename}/static/code/gtksharp.4.example2/VSImage2.png)

I've included example code within <https://github.com/grbd/GBD.Blog.Examples> although for now this is VB only

## GtkSharp Handles and WithEvents Example

For this next example we're going to use a similar project to the one used in the last part. <br>
But this time around we're going to split the code into 2 seperate files.

  * **TestForm1.glade.vb** - This acts as a sort of wrapper and makes all the properties of the Form available
  * **TestForm1.vb** - This is where our application logic sits similar to what you would use with windows forms

We'll be using *WithEvents* and *Handles* instead of the **Builder.Object** attribute. <br>
In order to link the properties to the controls on the form we can use code similar to <br>

``` vbnet
SendButton = builder.GetObject("SendButton")
```


### TestForm1.glade.vb

First we need to create a wrapper class for the glade file.
With windows forms this type of file is usually auto generated and hidden, but in this case we don't have that luxury.

**For Visual Basic:**

``` vbnet
Imports Gtk

Partial Public Class TestForm1
    Inherits Window

#Region "Properties"

    ''' <summary> Used to load in the glade file resource as a window. </summary>
    Private _builder As Builder

    ' Put a list here of all the controls you want to access on the glade form from code

    ' Note When using WithEvents, we need to link to the objects on the form within the constructor
    ' Instead of using the Builder.Object attribute, this seems to be the only way when using WithEvents and Handles

    ''' <summary> Connects to the SendButton on the Glade Window. </summary>
    Friend WithEvents SendButton As Button

    ''' <summary> Connects to the InputText Control on the Glade Window. </summary>
    Friend WithEvents StdInputTxt As Entry

    ''' <summary> Event queue for all listeners interested in Loaded events. </summary>
    Public Event Loaded As EventHandler

#End Region

#Region "Constructors / Destructors"

    ''' <summary> Default Shared Constructor. </summary>
    ''' <returns> A TestForm1. </returns>
    Public Shared Function Create() As TestForm1
        Dim builder As New Builder(Nothing, "GtkSharp_AdvForm1_VB.TestForm1.glade", Nothing)
        Return New TestForm1(builder, builder.GetObject("window1").Handle)
    End Function

    ''' <summary> Specialised constructor for use only by derived class. </summary>
    ''' <param name="builder"> The builder. </param>
    ''' <param name="handle">  The handle. </param>
    Protected Sub New(builder As Builder, handle As IntPtr)
        MyBase.New(handle)
        _builder = builder
        builder.Autoconnect(Me)

        ' Link the Controls here instead of using Attributes
        SendButton = builder.GetObject("SendButton")
        StdInputTxt = builder.GetObject("StdInputTxt")

        ' Form Loaded
        RaiseEvent Loaded(Me, Nothing)
    End Sub

#End Region

End Class
```


### TestForm1.vb

Next we need to create a class to house all of our control logic (similar again to the place where you would put code under windows forms)

**For Visual Basic:**

``` vbnet
Imports Gtk

''' <summary> Example Test Form for GTKSharp and Glade. </summary>
Partial Public Class TestForm1

#Region "Handlers"

    Private Sub TestForm1_Loaded(sender As Object, e As EventArgs) Handles Me.Loaded
        ' Form Loaded event
    End Sub

    ''' <summary> Handle Close of Form, Quit Application. </summary>
    ''' <param name="o">    Source of the event. </param>
    ''' <param name="args"> Event information to send to registered event handlers. </param>
    Private Sub TestForm1_DeleteEvent(o As Object, args As DeleteEventArgs) Handles Me.DeleteEvent
        Application.Quit()
        args.RetVal = True
    End Sub

    ''' <summary> Handle Click of Button. </summary>
    ''' <param name="sender"> Source of the event. </param>
    ''' <param name="e">      Event information to send to registered event handlers. </param>
    Private Sub SendButton_Clicked(sender As Object, e As EventArgs) Handles SendButton.Clicked
        StdInputTxt.Text = "Hello World"
    End Sub

#End Region

End Class
```

### Running the Application

When we run the application we should end up with a result similar to that as before.

![Example1]({filename}/static/code/gtksharp.4.example2/Example1.png)

The main difference now is that the setup is very familiar to those used to winforms,
also we have the option of using the drop downs within the code window to select different items and associated events

<br>
[GTKSharp - Part 3 - Basic Example with VS and Glade]({filename}./gtksharp.3.example1.md)<br>
[GTKSharp - Part 5 - Themes and ClearText]({filename}./gtksharp.5.theming.md)
