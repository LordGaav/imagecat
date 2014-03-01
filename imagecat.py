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

import sys

if sys.version_info < (2, 7):
	print "Sorry, {0} requires Python 2.7.".format(rsscat.NAME)
	sys.exit(1)

import imagecat
from imagecat.rotate import rotate_wallpapers
import tempfile
from argparse import ArgumentParser, SUPPRESS

config_parser = ArgumentParser(description="Looking for config", add_help=False)
config_parser.add_argument('--config', type=str)
config_parser.add_argument("--help", action="store_true", default=False)
config_parser.add_argument("--quiet", action="store_true", default=False)
config_parser.add_argument("--verbose", action="store_true", default=False)
config_parser.add_argument("--version", action="store_true", default=False)

config_arg, config_unknown = config_parser.parse_known_args()

log_handlers = {}
if not config_arg.version and not config_arg.help:
	log_handlers['syslog'] = None
loglevel = "INFO"
if config_arg.verbose:
	loglevel = "DEBUG"
if not config_arg.quiet:
	log_handlers['console'] = None

logger = imagecat.getLogger("imagecat", level=loglevel, handlers=log_handlers)

if config_arg.version:
	logger.info("{0} version {1} ({2})".format(imagecat.NAME, imagecat.VERSION, imagecat.BUILD))
	sys.exit(0)

if not config_arg.help:
	logger.info("{0} version {1} ({2}) starting...".format(imagecat.NAME, imagecat.VERSION, imagecat.BUILD))

config = imagecat.getConfig(config_arg)

arg_parser = ArgumentParser(description="{0} is an automatic wallpaper changer".format(imagecat.NAME))
arg_parser.add_argument("--automatic", action="store_true",     default=False, 											help=SUPPRESS)
arg_parser.add_argument("--config",    metavar="CFG", type=str, 														help="Config file to load")
arg_parser.add_argument("--imagedir",  metavar="DIR", type=str, default=config.get("imagedir", None), 					help="Where to look for wallpapers")
arg_parser.add_argument("--tmpdir",    metavar="DIR", type=str, default=config.get("tmpdir", tempfile.gettempdir()),	help="Where to store intermediate files")
arg_parser.add_argument("--desktops",  metavar="D",   type=int, default=config.get("desktops", 1),						help="Amount of desktops (not physical monitors)")
arg_parser.add_argument("--quiet",     action="store_true",     default=config.get("quiet", False),						help="Don't print messages to stdout")
arg_parser.add_argument("--verbose",   action="store_true",     default=config.get("verbose", False),					help="Output debug messages")
arg_parser.add_argument("--version",   action="store_true",     default=False,											help="Display version information and exit")
args = arg_parser.parse_args()

if args.automatic and config.get("autostart", 'False') == 'False':
	logger.info("Started automatically, but autostart is not enabled, exiting...")
	sys.exit(0)

if args.imagedir == None:
	logger.error("No imagedir specified, exiting...")
	sys.exit(1)

imagecat.IMAGEDIR = args.imagedir
imagecat.TMPDIR = args.tmpdir
imagecat.DESKTOPS = args.desktops
imagecat.QUIET = args.quiet
imagecat.VERBOSE = args.verbose

rotate_wallpapers()
