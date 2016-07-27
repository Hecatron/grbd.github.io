Title: Running ASP .Net 5 Websites on the Rpi via Docker
Date: 2016-01-28 21:00
Status: draft

## Overview



TODO

## Setup

### Install

In order to install the latest Docker tools for Visual Studio we first need to install Docker Toolbox

  * <https://www.docker.com/products/docker-toolbox>

Next we need the latest Docker Tools For Visual Studio 2015.
The older versions seem to have certain bugs surrounding the creation of images

  * <https://visualstudiogallery.msdn.microsoft.com/0f5b2caa-ea00-41c8-b8a2-058c7da0b3e4>


## Docker Base Image

On the server side we need a base image with everything needed installed to run a aspnet website
In this case the best option for a base image seems to be resin/rpi-raspbian:jessie for the rpi

we can then add to this base image the bits we need for aspnet

Based on these links:

  * https://github.com/aspnet/aspnet-docker/tree/master/1.0.0-rc1-update1
  * https://docs.docker.com/engine/userguide/containers/dockerimages/

TODO include modified aspnet Docker file

The above is the aspnet docker file with a couple of modifications
First it uses the **resin/rpi-raspbian:jessie** as a base image instead because we're using a rpi not an x86 machine
also it installs **ca-certificates** needed for curl

To Build
```
cd /home/ric/DockerProfiles/garlicbready/rpi-raspbian-aspnet-coreclr/
docker build -t garlicbready/rpi-raspbian-aspnet:v1 .
```


## Publish via VS

### Web Application Docker File

Within the root of the web application there should be a single Docker File with the following contents
we can't use the default microsoft/aspnet image since it's x86 based

```
FROM microsoft/aspnet:

ADD . /app

WORKDIR /app/approot

ENTRYPOINT ["./web"]
```

replace the FROM statement with
```FROM garlicbready/rpi-raspbian-aspnet-mono:4.2.2.30```

add the line for exposing the web port
```EXPOSE 5000```

The end result should be
```
FROM garlicbready/rpi-raspbian-aspnet-mono:4.2.2.30

ADD . /app
EXPOSE 5000

WORKDIR /app/approot
ENTRYPOINT ["./web"]
```

### Project File

Change the kestrel binding to the following to listen in on all ip's not just localhost
```
 "web": "Microsoft.AspNet.Server.Kestrel --server.urls=http://*:5000"
```


### Visual Studio Publish

Next to publish

  * Select Build -> Publish WebApplication
  * Select Docker Containers
  * Select Custom Docker Host tickbox, click Okay

  * For the server url use tcp://192.168.111.53:2376
  * For the Host port pick something like **8080** this is what will be viewable from the outside
  * For the Contaimer port pick **5000** by default for the web app

make sure to use tcp:// not http:// in the url

this will build the site and create a statement similar to
docker -H tcp://192.168.111.53:2376 build -t webapplication1 -f "C:\Users\ric\AppData\Local\Temp\PublishTemp\WebApplication188\approot\src\WebApplication1\Dockerfile" "C:\Users\ric\AppData\Local\Temp\PublishTemp\WebApplication188"


TODO
it looks like coreclr doesn't currently work
since the runtimes are set / compiled for x64 via
ENV DNX_RUNTIME_ID ubuntu.14.04-x64
so we need a mono based deployment instead

do we need to enable masquerading?
iptables -t nat -A  POSTROUTING  -o  wlan0  -j  MASQUERADE

