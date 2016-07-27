Title: GtkSharp - Part 5 - Themes and ClearText
Summary: Using themes within GtkSharp and enabling cleartype font text
Date: 2016-06-25 23:30
Tags: code, dotnet, GtkSharp

## Overview

One of the interesting features of GtkSharp and GTK3 is its theming ability.
Although there doesn't seem to be a lot of documentation on handling this easily within .Net and GtkSharp

After a bit of digging around I've recently managed to get themes working with GtkSharp.
Also I've discovered a fix for cleartext to make the fonts look nicer under windows and to alter the dpi settings. <br>
As with prior code, I've placed examples within a gitrepo of <https://github.com/grbd/GBD.Blog.Examples>.

## GTK 3 Themes

### Theme Versions

The first thing to be aware of is the version of gtk in use, within the NuGet package *GtkSharp.Win32*

When theming it's important to use a theme compatible with the version of gtk used by GtkSharp, currently that's **gtk-3.14** as of writing with the NuGet package <br>
With **gtk-3.14** and upwards the theme engine (which used to be a separate Dll in older versions) is now bundled within the gtk libs <br>
If you pick a theme that complains about "adwaita not found" when loading, it's probably designed for an older version of gtk and is trying to load the engine which is already in memory

For a list of themes:

  * <https://www.gnome-look.org/>


### Selecting a theme

In order to load in a theme with GtkSharp / gtk3 we can use something similar to the below

**For C#**

``` csharp
// Load the Theme
Gtk.CssProvider css_provider = new Gtk.CssProvider();
css_provider.LoadFromPath("themes/DeLorean-Dark-3.14/gtk-3.0/gtk.css");
Gtk.StyleContext.AddProviderForScreen(Gdk.Screen.Default, css_provider, 800);
```

**For Visual Basic:**

``` vbnet
' Load the Theme
Dim css_provider As New Gtk.CssProvider
css_provider.LoadFromPath("themes/DeLorean-Dark-3.14/gtk-3.0/gtk.css")
Gtk.StyleContext.AddProviderForScreen(Gdk.Screen.Default, css_provider, 800)
```

By using LoadFromPath to load in the root css file (usually gtk-3.0/gtk.css) <br>
From that point onwards everything else should be loaded in automatically. <br>
In order for the above to work, the themes directory needs to be relative to the exe, although an absolute path can be specified.


### The old theme selection method

One older method of loading themes within GtkSharp was the use of Settings.Default.ThemeName

``` vbnet
Settings.Default.ThemeName = "delorean-dark-theme-3.9"
```

With the more recent version of GtkSharp / gtk3 this doesn't appear to work. <br>
However it still might be useful if your using an older version of GtkSharp with gtk2

  * <https://developer.gnome.org/gtk3/stable/GtkSettings.html#GtkSettings--gtk-theme-name>


### ClearText

Based on some observations of the end result, I discovered that under windows there was potentially a problem with the default setting for the use of ClearText.
ClearText has an impact on the visibility / smoothness of the displayed fonts within Gtk and GtkSharp.
With applications run from MSYS2 with the default theme, compared to an application running from GtkSharp, the fonts do seem to be very different by default

This is something that may be fixed eventually within the gtk libs (GtkSharp.Win32)
But for now one way around this is to use some code similar to the below

**For C#**

``` csharp
public static void ApplyTheme() {
    // Based on this Link http://awesome.naquadah.org/wiki/Better_Font_Rendering

    // Get the Global Settings
    var setts = Gtk.Settings.Default;
    // This enables clear text on Win32, makes the text look a lot less crappy
    setts.XftRgba = "rgb";
    // This enlarges the size of the controls based on the dpi
    setts.XftDpi = 96;
    // By Default Anti-aliasing is enabled, if you want to disable it for any reason set this value to 0
    //setts.XftAntialias = 0
    // Enable text hinting
    setts.XftHinting = 1;
    //setts.XftHintstyle = "hintslight"
    setts.XftHintstyle = "hintfull";

    // Load the Theme
    Gtk.CssProvider css_provider = new Gtk.CssProvider();
    //css_provider.LoadFromPath("themes/DeLorean-3.14/gtk-3.0/gtk.css")
    css_provider.LoadFromPath("themes/DeLorean-Dark-3.14/gtk-3.0/gtk.css");
    Gtk.StyleContext.AddProviderForScreen(Gdk.Screen.Default, css_provider, 800);
}
```

**For Visual Basic:**

``` vbnet
Public Shared Sub ApplyTheme()
    ' Based on this Link http://awesome.naquadah.org/wiki/Better_Font_Rendering

    ' Get the Global Settings
    Dim setts = Gtk.Settings.Default
    ' This enables clear text on Win32, makes the text look a lot less crappy
    setts.XftRgba = "rgb"
    ' This enlarges the size of the controls based on the dpi
    setts.XftDpi = 96
    ' By Default Anti-aliasing is enabled, if you want to disable it for any reason set this value to 0
    'setts.XftAntialias = 0
    ' Enable text hinting
    setts.XftHinting = 1
    'setts.XftHintstyle = "hintslight"
    setts.XftHintstyle = "hintfull"

    ' Load the Theme
    Dim css_provider As New Gtk.CssProvider
    'css_provider.LoadFromPath("themes/DeLorean-3.14/gtk-3.0/gtk.css")
    css_provider.LoadFromPath("themes/DeLorean-Dark-3.14/gtk-3.0/gtk.css")
    Gtk.StyleContext.AddProviderForScreen(Gdk.Screen.Default, css_provider, 800)

End Sub
```

## End Result

The end result should be a form which looks a lot clearer and can use a custom theme at the same time

### No Themes or ClearText

The first example is no theming or cleartext under Windows 10

![Example1]({filename}/static/code/gtksharp.5.theming/Example1.png)

### Themes but no ClearText

This next example has theming but with no cleartext

![Example2]({filename}/static/code/gtksharp.5.theming/Example2.png)

### Themes and ClearText

This final example has both theming and cleartext enabled

![Example3]({filename}/static/code/gtksharp.5.theming/Example3.png)

<br>
<br>
[GtkSharp - Part 4 - Handles and WithEvents Example]({filename}./gtksharp.4.example2.md)
