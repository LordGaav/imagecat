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
VERSION = "0.3"
BUILD = "3804217"

STARTARG = None

THREADS = None

IMAGEDIR = None
TMPDIR = None
DESKTOPS = None
INTERVAL = None
ONCE = False
QUIET = False
VERBOSE = False

import logging, logging.handlers, os, pwd, grp, sys, inspect, tempfile
from configobj import ConfigObj
from argparse import ArgumentParser, SUPPRESS
from imagecat.threads import Threads
from imagecat.scheduler import Scheduler

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

def parseCliArgs(config):
	arg_parser = ArgumentParser(description="{0} is an automatic wallpaper changer".format(NAME))
	arg_parser.add_argument("--automatic", action="store_true",     default=False,                                       help=SUPPRESS)
	arg_parser.add_argument("--config",    metavar="CFG", type=str,                                                      help="Config file to load")
	arg_parser.add_argument("--imagedir",  metavar="DIR", type=str, default=config.get("imagedir", None),                help="Where to look for wallpapers")
	arg_parser.add_argument("--tmpdir",    metavar="DIR", type=str, default=config.get("tmpdir", tempfile.gettempdir()), help="Where to store intermediate files")
	arg_parser.add_argument("--desktops",  metavar="D",   type=int, default=config.get("desktops", 1),                   help="Amount of desktops (not physical monitors)")
	arg_parser.add_argument("--interval",  metavar="I",   type=int, default=config.get("interval", 60),                  help="Time between wallpaper rotations, in seconds)")
	arg_parser.add_argument("--once",      action="store_true",     default=config.get("once", False),                   help="Only run once, instead of scheduled")
	arg_parser.add_argument("--quiet",     action="store_true",     default=config.get("quiet", False),                  help="Don't print messages to stdout")
	arg_parser.add_argument("--verbose",   action="store_true",     default=config.get("verbose", False),                help="Output debug messages")
	arg_parser.add_argument("--version",   action="store_true",     default=False,                                       help="Display version information and exit")
	args = arg_parser.parse_args()

	if args.automatic and config.get("autostart", 'False') == 'False':
		logger.info("Started automatically, but autostart is not enabled, exiting...")
		sys.exit(0)

	if args.imagedir == None:
		logger.error("No imagedir specified, exiting...")
		sys.exit(1)

	return args

def reloadConfig():
	global STARTARG, THREADS
	global IMAGEDIR, TMPDIR, DESKTOPS, INTERVAL, ONCE, QUIET, VERBOSE

	config = getConfig(STARTARG)
	args = parseCliArgs(config)

	IMAGEDIR = args.imagedir
	TMPDIR = args.tmpdir
	DESKTOPS = args.desktops
	INTERVAL = args.interval
	ONCE = args.once
	QUIET = args.quiet
	VERBOSE = args.verbose

	if isinstance(THREADS, Threads) and "rotate" in THREADS.getThreads():
		THREADS.getThread("rotate").delay = INTERVAL

def initialize():
	global THREADS, INTERVAL

	getLogger(__name__).info("Initializing...")

	if THREADS is None:
		THREADS = Threads()

	from imagecat.rotate import rotate_wallpapers

	rotateThread = Scheduler(INTERVAL, rotate_wallpapers, "rotateThread", True)

	THREADS.registerThread("rotate", rotateThread)

def startAll():
	global THREADS

	getLogger(__name__).info("Starting {0} threads...".format(NAME))

	for thread in THREADS.getThreads():
		t = THREADS.getThread(thread)
		getLogger(__name__).debug("Starting {0}".format(t.name))
		t.start()

	getLogger(__name__).info("Started all threads")

def stopAll():
	global THREADS

	getLogger(__name__).info("Stopping {0} threads...".format(NAME))

	for thread in THREADS.getThreads():
		t = THREADS.getThread(thread)
		getLogger(__name__).info("Stopping {0}".format(t.name))
		t.stop = True
		t.join()
		THREADS.unregisterThread(thread)

	getLogger(__name__).info("Stopped all threads")
	getLogger(__name__).fatal("Comitting suicide")

	os._exit(0)

def signal_handler(signum=None, frame=None):
	if type(signum) != type(None):
		getLogger(__name__).info("Caught signal {0}".format(signum))
		stopAll()

def config_handler(signum=None, frame=None):
	if type(signum) != type(None):
		getLogger(__name__).info("Caught signal {0}, reloading config".format(signum))
		reloadConfig()
		getLogger(__name__).info("Config reloaded")

def hello(text):
	getLogger(__name__).info(text)
