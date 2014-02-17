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

NAME = "imagecat"
VERSION = "0.1.1"
BUILD = "c62d195"

import logging, logging.handlers, os, pwd, grp, sys, inspect
from configobj import ConfigObj

def getLogger(name, level=logging.INFO, handlers=[]):
	logger = logging.getLogger(name)

	if len(handlers) != 0:
		logger.setLevel(level)

	if "console" in handlers:
		strm = logging.StreamHandler()
		fmt = logging.Formatter('%(message)s')
		strm.setLevel(level)
		strm.setFormatter(fmt)
		logger.addHandler(strm)

	if "file" in handlers:
		conf = handlers['file']
		fl = logging.handlers.WatchedFileHandler(conf['logfile'])
		fl.setLevel(level)

		fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fl.setFormatter(fmt)
		logger.addHandler(fl)

	if "syslog" in handlers:
		sysl = logging.handlers.SysLogHandler(address='/dev/log', facility=logging.handlers.SysLogHandler.LOG_SYSLOG)
		sysl.setLevel(level)

		formatter = logging.Formatter('%(name)s[' + str(os.getpid()) + '] %(levelname)-8s: %(message)s')
		sysl.setFormatter(formatter)
		logger.addHandler(sysl)

	return logger

def getConfig(config_arg, debug_log=False, console=True):
	logger = getLogger("imagecat.getConfig", logging.DEBUG if debug_log else logging.INFO)

	logger.debug("Expanding variables")
	home = os.path.expanduser("~")
	loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

	logger.debug("Create empty config")
	config = ConfigObj()

	# Merge in config file in program dir
	if os.path.isfile(os.path.join(loc, "imagecat.config")):
		logger.debug("Loading config from workingdir")
		cfg = ConfigObj(os.path.join(loc, "imagecat.config"))
		config.merge(cfg)

	# Merge in system-wide config (Unix specific)
	if os.path.isfile("/etc/imagecat.config"):
		logger.debug("Loading config from /etc")
		cfg = ConfigObj("/etc/imagecat.config")
		config.merge(cfg)

	# Merge in user specific config
	if os.path.isfile(os.path.join(home, ".imagecat.config")):
		logger.debug("Loading config from homedir")
		cfg = ConfigObj(os.path.join(home, ".imagecat.config"))
		config.merge(cfg)

	# Config file provided on command line has preference
	if config_arg.config:
		logger.debug("Loading config from cli arguments")
		cfg = ConfigObj(config_arg.config)
		config.merge(cfg)

	return config

def hello(text):
	getLogger(__name__).info(text)
