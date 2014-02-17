![imagecat :3](https://github.com/LordGaav/imagecat/blob/develop/icons/imagecat_72.png?raw=true "imagecat :3")
imagecat
--------

An automatic wallpaper changer with multi-monitor support.

Dependencies
============

* python >= 2.7
* python-configobj
* python-gi
* python-gobject
* python-imaging
* x11-xserver-utils (or another package that provides `xrandr`)

Building
========

No building is required to use imagecat. To build a Debian package, perform the following steps:

1. `apt-get install ubuntu-dev-tools debhelper dh-exec`

From here you can either build the package with pbuilder-dist:

2. `pbuilder-dist saucy create`
3. `make -f debian/Makefile source_no_sign`
4. `make -f debian/Makefile pbuild CHANGES=../imagecat_xxxx_.dsc`
5. look for the resulting .deb in ~/pbuilder/saucy_result

Or directly using dpkg-buildpackage

2. `make -f debian/Makefile package`


Installing
==========

Either use the methods described above to build your own package, or install it from my PPA.

1. `add-apt-repository ppa:lordgaav/imagecat`
2. `apt-get update && apt-get install imagecat`

Using
=====

The package will install a global config file in /etc/imagecat.config and will cause imagecat to get started at every login. imagecat will not run by default however, if you want imagecat to automatically change your wallpaper every two minutes, you have two options:

* Change autorun to True in /etc/imagecat.config to enable imagecat for ALL users, or
* Create ~/.imagecat.config, and set autorun to True.

Optionally, change imagedir to your own directory of images. By default, imagecat will use /usr/share/background.

Man page
========

IMAGECAT(1)			 User Commands			   IMAGECAT(1)



NAME
       imagecat - manual page for imagecat version 0.1 (a5e5150)

DESCRIPTION
       usage: imagecat.py [-h] [--config CFG] [--imagedir DIR] [--tmpdir DIR]

	      [--desktops D] [--quiet] [--verbose] [--version]

       imagecat is an automatic wallpaper changer

   optional arguments:
       -h, --help
	      show this help message and exit

       --config CFG
	      Config file to load

       --imagedir DIR
	      Where to look for wallpapers

       --tmpdir DIR
	      Where to store intermediate files

       --desktops D
	      Amount of desktops (not physical monitors)

       --quiet
	      Don't print messages to stdout

       --verbose
	      Output debug messages

       --version
	      Display version information and exit

CONFIGURATION
       imagecat will look in multiple locations for a configuration file:

	1.  --config option
	2. ~/.imagecat.config
	3. /etc/imagecat.config
	4. imagecat.config in /usr/share/imagecat

       Configuration  files  are  applied according to their priority, meaning
       that options in /etc/imagecat.config can be overridden using  ~/.image-
       cat.config,  which in turn can be overridden by specifying another con-
       figuration file with --config

       Most cli options can be specified in the configuration file,  the  most
       useful options are probably:

       imagedir  :  directory  of images to load. All files ending with exten-
       sions *.jpg, *.jpeg, *.gif and *.png are loaded. Directories  are  tra-
       versed recursively.

       desktops : amount of virtual desktops.

DEBIAN SPECIFIC
       The Debian package will by default install a file in /etc/imagecat.con-
       fig, and use the autostart  option  to  disable	automatically  running
       imagecat.  Imagecat will be automatically started when a user logs into
       Gnome/Unity, but will not actually run  until  /etc/imagecat.config  is
       edited  to allow autostart, or until an user creates ~/.imagecat.config
       to achieve the same thing. The default /etc/imagecat.config will try to
       look  for  wallpapers  in  /usr/share/wallpapers, an user will probably
       want to override this with their own directory.

KNOWN ISSUES
       I have not yet found a reliable way to determine the amount of  virtual
       desktops. For now, this has to be specified manually using --desktops



imagecat version 0.1 (a5e5150)	 February 2014			   IMAGECAT(1)
