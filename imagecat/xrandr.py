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
	of dicts containing at least: name, state, primary?.
	If the state of the displays is 'connected', the following fields are also set:
	resolution, offset, size.
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
		displays = self.randr_regex.findall(output)
		self.displays = []

		for d in displays:
			e = {}
			e['name'] = d[0]
			if d[1] == "connected" and d[3] == "":
				e['state'] = "inactive"
			else:
				e['state'] = d[1]
			e['primary'] = True if d[2] == 'primary' else False
			if e['state'] == "connected":
				e['resolution'] = (int(d[3]), int(d[4]))
				e['offset'] = (int(d[5]), int(d[6]))
				e['size'] = (int(d[7].replace("mm", "")), int(d[8].replace("mm", "")))
			self.displays.append(e)

		return self.displays

if __name__ == "__main__":
	from pprint import PrettyPrinter
	r = XRandr()
	pp = PrettyPrinter(indent=4)
	pp.pprint(r.displays)
