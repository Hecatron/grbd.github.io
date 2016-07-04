Title: 3D Monogame within gtksharp
Date: 2016-01-28 21:00
Status: draft

It looks like more recent versions of mono now support hard float for the rpi
https://www.raspberrypi.org/forums/viewtopic.php?f=41&t=1225&start=25
https://neildanson.wordpress.com/2013/12/10/building-mono-on-a-raspberry-pi-hard-float/

http://jaquadro.com/2013/03/embedding-your-monogame-game-in-a-winforms-control/
http://jaquadro.com/2013/03/bringing-your-xna-winforms-controls-to-monogame-opengl/
https://github.com/jaquadro/MonoGame-WinFormsControls
https://github.com/CartBlanche/MonoGame-Samples/tree/master/WpfInteropSample
is there a more modern way of doing the above?

http://stackoverflow.com/questions/33054371/draw-spritebatch-of-monogame-inside-a-gtk-control
setup for gtksharp?

looks like opentk is no longer maintained
and monogame are moving to direct opengl / sdl
https://github.com/opentk/opentk/commit/2e51fe019771f4c70b15bb25b3a560f712a45fbf
https://github.com/mono/MonoGame/issues/4399#issuecomment-173001793
http://cs-sdl.sourceforge.net/


Looks like this is the solution
https://github.com/RedpointGames/MonoGame
need to look at making a Nuget package from this for the 3.4 tag
