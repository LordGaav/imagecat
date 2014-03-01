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

import sys, signal, time

if sys.version_info < (2, 7):
	print "Sorry, {0} requires Python 2.7.".format(rsscat.NAME)
	sys.exit(1)

import imagecat
from imagecat.rotate import rotate_wallpapers
from argparse import ArgumentParser

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

imagecat.STARTARG = config_arg

imagecat.reloadConfig()

def main():
	if imagecat.ONCE:
		logger.info("Single run mode")
		from imagecat.rotate import rotate_wallpapers
		rotate_wallpapers()
	else:
		logger.info("Wallpapers will rotate every {0} seconds.".format(imagecat.INTERVAL))

		signal.signal(signal.SIGINT, imagecat.signal_handler)
		signal.signal(signal.SIGTERM, imagecat.signal_handler)
		signal.signal(signal.SIGUSR1, imagecat.config_handler)

		imagecat.initialize()
		imagecat.startAll()

		# Stay alive to handle signals
		while True:
			time.sleep(2)

if __name__ == "__main__":
	main()
