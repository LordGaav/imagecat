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

from subprocess import Popen, PIPE
import re

class XRandr(object):
	"""
	Gathers information about connected screens using `xrandr` cli tool.
	"""

	randr_regex = re.compile("([a-zA-Z0-9]+) (connected|disconnected) (primary|)[ ]?([0-9]+)?[x]?([0-9]+)?([+-][0-9]+)?([+-][0-9]+)?[ ]?\(.+\)(?: ([0-9m]+) x ([0-9m]+))?")
	""" Regex pattern to match the display lines in the output of `xrandr` """

	displays = []
	"""
	Contains the found displays according to `xrandr`, represented as a list
	of tuples containing:
	(display name, connection state, primary?, width in px, height in px, horizontal offset in px, 
	vertical offset in px, height in mm, width in mm)
	The first two values are always set. If the connection state is disconnected, the rest of
	the values will probably be empty.
	"""

	def __init__(self):
		self.parse_xrandr()
	
	def _call_xrandr(self):
		"""
		Convenience method to call `xrandr` using Popen and return stdout and stderr. Will
		probably raise an Error if something goes wrong.
		"""
		command = "xrandr"
		proc = Popen(command, stdout=PIPE, stderr=PIPE)
		proc.wait()
		return proc.communicate()

	def parse_xrandr(self):
		"""
		Applies randr_regex to the output of `xrandr`, and store it internally. Retrieve
		from the internal displays field. To refresh, call parse_xrandr() manually.
		"""
		output = self._call_xrandr()[0]

		self.displays = self.randr_regex.findall(output)

		return self.displays

if __name__ == "__main__":
	from pprint import PrettyPrinter
	r = XRandr()
	pp = PrettyPrinter(indent=4)
	pp.pprint(r.displays)
