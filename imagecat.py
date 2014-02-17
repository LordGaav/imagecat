#!/usr/bin/env python
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

import sys, os

if sys.version_info < (2, 7):
	print "Sorry, {0} requires Python 2.7.".format(rsscat.NAME)
	sys.exit(1)

import imagecat
import tempfile
from argparse import ArgumentParser

config_parser = ArgumentParser(description="Looking for config", add_help=False)
config_parser.add_argument('--config',  metavar='CONFIG', type=str)
config_parser.add_argument("--quiet", action="store_true", default=False)
config_parser.add_argument("--verbose", action="store_true", default=False)

config_arg, config_unknown = config_parser.parse_known_args()

log_handlers = {}
log_handlers['syslog'] = None
loglevel = "INFO"
if config_arg.verbose:
	loglevel = "DEBUG"
if not config_arg.quiet:
	log_handlers['console'] = None

logger = imagecat.getLogger("imagecat", level=loglevel, handlers=log_handlers)

logger.info("{0} version {1} ({2}) starting...".format(imagecat.NAME, imagecat.VERSION, imagecat.BUILD))

config = imagecat.getConfig(config_arg)

arg_parser = ArgumentParser(description="{0} is an automatic wallpaper changer".format(imagecat.NAME))
arg_parser.add_argument("--imagedir", metavar="DIR", type=str, default=config.get("imagedir", None), 				help="Where to look for wallpapers")
arg_parser.add_argument("--tmpdir",   metavar="DIR", type=str, default=config.get("tmpdir", tempfile.gettempdir()),	help="Where to store intermediate files")
arg_parser.add_argument("--desktops", metavar="D",   type=int, default=config.get("desktops", 1),					help="Amount of desktops (not physical monitors)")
arg_parser.add_argument("--dry-run",  action="store_true",     default=config.get("dry-run", False),				help="Print what would've happened, but don't execute actions")
arg_parser.add_argument("--quiet",    action="store_true",     default=config.get("quiet", False),					help="Don't print messages to stdout")
arg_parser.add_argument("--verbose",  action="store_true",     default=config.get("verbose", False),				help="Output debug messages")
args = arg_parser.parse_args()

if args.imagedir == None:
	logger.error("No imagedir specified, exiting...")
	sys.exit(1)

from imagecat.globber import Globber
from imagecat.image import *
from imagecat.randomizer import Randomizer
from imagecat.gconf import *
from imagecat.xrandr import XRandr
import Image

images = Globber(path=args.imagedir, filter=['*.jpg', '*.jpeg', '*.gif', '*.png'], recursive=True).glob()

logger.info("Found {0} images".format(len(images)))

displays = XRandr().displays
active_displays = filter(lambda x: x['state'] == "connected", displays)

logger.info("Found {0} active displays ({1} total displays)".format(len(active_displays), len(displays)))
logger.info("Found {0} desktops".format(args.desktops))

random = Randomizer(images)

logger.debug("Randomizer checksum: {0}".format(random.checksum))

# TODO: invalidate blacklist when checksum changes

selection = random.get_random(len(active_displays) * args.desktops)

logger.info("Selected {0} random images".format(len(selection)))

i = 0
wallpapers = []
offsets = map(lambda x: x['offset'], active_displays)
while i < args.desktops:
	logger.info("Generating wallpaper for desktop {0}".format(i))
	tmp_images = []
	for m in active_displays:
		f = selection.pop()
		im = Image.open(f)
		targetsize = (m['resolution'][0], m['resolution'][1])
		logger.debug("Cropresizing {0} from {1} to {2}".format(f, im.size, targetsize))
		tmp_images.append(cropresize(im, targetsize))

	logger.debug("Montaging images to wallpaper")
	wallpapers.append(montage(tmp_images, offsets))
	i += 1

logger.info("Remove old wallpaper files")
old_wallpapers = Globber(path=args.tmpdir, filter=['wallpaper-*.*'], recursive=False).glob()

for old in old_wallpapers:
	logger.debug("Unlinking {0}".format(old))
	os.unlink(old)

j = 0
bg_images = []
for wallpaper in wallpapers:
	filename = os.path.join(args.tmpdir, "wallpaper-{0}-{1}.png".format(j, os.getpid()))
	logger.info("Saving wallpaper {0} to {1}".format(j, filename))
	wallpaper.save(filename)
	j += 1
	bg_images.append(filename)

logger.info("Setting new wallpapers in GConf")
bg_colors = ["000000"] * len(bg_images)
bg_fill_types = [SOLIDFILL] * len(bg_images)
bg_image_pos = [CENTERED] * len(bg_images)

gconf = WallpaperPluginSettings()
gconf.delay()
logger.debug("Setting bg_image to {0}".format(bg_images))
gconf.set_bg_image(bg_images)
logger.debug("Setting bg_color1 to {0}".format(bg_colors))
gconf.set_bg_color1(bg_colors)
logger.debug("Setting bg_color2 to {0}".format(bg_colors))
gconf.set_bg_color2(bg_colors)
logger.debug("Setting bg_fill_type to {0}".format(bg_fill_types))
gconf.set_bg_fill_type(bg_fill_types)
logger.debug("Setting bg_image_pos to {0}".format(bg_image_pos))
gconf.set_bg_image_pos(bg_image_pos)
gconf.apply()

logger.info("All done!")
