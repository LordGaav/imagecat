#
# Copyright (c) 2014 Nick Douma < n.douma [at] nekoconeko . nl >
#
# This file is part of imagecat.
#
# imagecat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# imagecat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with imagecat. If not, see <http://www.gnu.org/licenses/>.
#

import os,time, platform
import Image

import imagecat
from imagecat.globber import Globber
from imagecat.image import cropresize, montage
from imagecat.randomizer import Randomizer
from imagecat.xrandr import XRandr

def select_images():
	"""
	Select a set of images based on the current display configuration. 
	Returns a tuple containing display information, and the selected images.
	"""
	logger = imagecat.getLogger("{0}.{1}".format(__name__, "select_images"))
	images = Globber(path=imagecat.IMAGEDIR, filter=['*.jpg', '*.jpeg', '*.gif', '*.png'], recursive=True).glob()

	logger.info("Found {0} images".format(len(images)))

	xrandr = XRandr()
	active_displays = xrandr.get_connected_displays()

	logger.info("Found {0} active displays ({1} total displays)".format(len(active_displays), len(xrandr.displays)))
	logger.info("Found {0} desktops".format(imagecat.DESKTOPS))

	random = Randomizer(images)

	logger.debug("Randomizer checksum: {0}".format(random.checksum))

	# TODO: invalidate blacklist when checksum changes

	selection = random.get_random(len(active_displays) * imagecat.DESKTOPS)

	logger.info("Selected {0} random images".format(len(selection)))

	return (active_displays, selection)

def montage_images(displays, selection):
	"""
	Montage images based on display information and a list of images.
	The end result is a set of Images that are the size of the total X viewport, 
	in which the source Images are pasted at the correct position.
	"""
	logger = imagecat.getLogger("{0}.{1}".format(__name__, "montage_images"))

	i = 0
	wallpapers = []
	offsets = map(lambda x: x['offset'], displays)
	while i < imagecat.DESKTOPS:
		logger.info("Generating wallpaper for desktop {0}".format(i))
		tmp_images = []
		for m in displays:
			f = selection.pop()
			im = Image.open(f)
			targetsize = (m['resolution'][0], m['resolution'][1])
			logger.debug("Cropresizing {0} from {1} to {2}".format(f, im.size, targetsize))
			tmp_images.append(cropresize(im, targetsize))

		logger.debug("Montaging images to wallpaper")
		wallpapers.append(montage(tmp_images, offsets))
		i += 1
	
	return wallpapers

def set_wallpapers(wallpapers):
	"""
	Removes all old wallpaper files in TMPDIR, and saves the given set of wallpapers as files.
	"""
	logger = imagecat.getLogger("{0}.{1}".format(__name__, "set_wallpapers"))

	logger.info("Remove old wallpaper files")
	old_wallpapers = Globber(path=imagecat.TMPDIR, filter=['wallpaper-*.*'], recursive=False).glob()

	for old in old_wallpapers:
		logger.debug("Unlinking {0}".format(old))
		os.unlink(old)

	j = 0
	bg_images = []
	for wallpaper in wallpapers:
		filename = os.path.join(imagecat.TMPDIR, "wallpaper-{0}-{1}-{2}.png".format(j, os.getpid(), int(time.time())))
		logger.info("Saving wallpaper {0} to {1}".format(j, filename))
		wallpaper.save(filename)
		j += 1
		bg_images.append(filename)
	
	return bg_images

def update_config(bg_images):
	"""
	Updates the appropriate configuration settings, so that the new background images are displayed.
	The appropriate configuration backend is selected based on Linux distribution, currently only
	Ubuntu 12.04 and later are supported and tested.
	"""
	logger = imagecat.getLogger("{0}.{1}".format(__name__, "update_config"))

	if platform.dist()[0] == "Ubuntu" and platform.dist()[1] in ['12.04']:
		logger.debug("Ubuntu 12.04 detected, using GConf backend.")
		import imagecat.settings_gconf as Settings
	else:
		logger.debug("Using GSettings backend.")
		import imagecat.settings_gsettings as Settings
	settings = Settings.WallpaperPluginSettings()

	logger.info("Setting new wallpapers in {0}".format(type(settings)))
	bg_colors = ["000000"] * len(bg_images)
	bg_fill_types = [Settings.SOLIDFILL] * len(bg_images)
	bg_image_pos = [Settings.CENTERED] * len(bg_images)

	settings.delay()
	logger.debug("Setting bg_image to {0}".format(bg_images))
	settings.set_bg_image(bg_images)
	logger.debug("Setting bg_color1 to {0}".format(bg_colors))
	settings.set_bg_color1(bg_colors)
	logger.debug("Setting bg_color2 to {0}".format(bg_colors))
	settings.set_bg_color2(bg_colors)
	logger.debug("Setting bg_fill_type to {0}".format(bg_fill_types))
	settings.set_bg_fill_type(bg_fill_types)
	logger.debug("Setting bg_image_pos to {0}".format(bg_image_pos))
	settings.set_bg_image_pos(bg_image_pos)
	settings.apply()

def rotate_wallpapers():
	"""
	Rotate the currently set wallpapers and select new ones randomly, based on the currently
	connected displays.
	"""
	logger = imagecat.getLogger("{0}.{1}".format(__name__, "rotate_wallpapers"))
	logger.info("Start rotation")

	selection = select_images()
	wallpapers = montage_images(*selection)
	bg_images = set_wallpapers(wallpapers)
	update_config(bg_images)

	logger.info("All done!")
