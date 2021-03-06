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

from imagecat.version import NAME, VERSION
from setuptools import setup
import linecache

PACKAGE_NAME = NAME
DESCRIPTION = linecache.getline("README.md", 5)

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	license="GPLv3",
	author="Nick Douma",
	author_email="n.douma@nekoconeko.nl",
	url="https://github.com/LordGaav/imagecat",
	packages=[PACKAGE_NAME],
	setup_requires=[
		"setuptools",
		"configobj"
	],
	install_requires=[
		"configobj",
		"Pillow",
		"setproctitle"
		## We also depend on python-gobject (==12.04) or python-gi (>=14.04), but there is no proper pypi package available for those.
	],
	entry_points={"console_scripts": ["{0} = {1}.cli:main".format(NAME, PACKAGE_NAME)]}
)
