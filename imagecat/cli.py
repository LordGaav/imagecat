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

import setproctitle
import signal
import sys
import time
from imagecat import signal_handler, config_handler, set_startarg
from imagecat import getLogger as get_logger, reloadConfig as reload_config, initialize as imagecat_initialize,\
	startAll as imagecat_startall
from imagecat.version import NAME, VERSION, BUILD
import imagecat  # only for config variables

if sys.version_info < (2, 7):
	print "Sorry, {0} requires Python 2.7.".format(NAME)
	sys.exit(1)

setproctitle.setproctitle("imagecat")


def initialize():
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

	logger = get_logger("imagecat", level=loglevel, handlers=log_handlers)

	if config_arg.version:
		logger.info("{0} version {1} ({2})".format(NAME, VERSION, BUILD))
		sys.exit(0)

	if not config_arg.help:
		logger.info("{0} version {1} ({2}) starting...".format(NAME, VERSION, BUILD))

	set_startarg(config_arg)

	reload_config()

	return logger


def main():
	logger = initialize()

	if imagecat.ONCE is True:
		logger.info("Single run mode")
		from imagecat.rotate import rotate_wallpapers
		rotate_wallpapers()
	else:
		logger.info("Wallpapers will rotate every {0} seconds.".format(imagecat.INTERVAL))

		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTERM, signal_handler)
		signal.signal(signal.SIGUSR1, config_handler)

		imagecat_initialize()
		imagecat_startall()

		# Stay alive to handle signals
		while True:
			time.sleep(2)

if __name__ == "__main__":
	main()
