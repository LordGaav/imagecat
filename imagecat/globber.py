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

import os,fnmatch

class Globber(object):
	"""
	Traverses a directory and returns all absolute filenames.
	"""

	def __init__(self, path, filter=['*'], recursive=True):
		""" Initialize Globber parameters. Filter may be a list of globbing patterns. """
		self.path = path
		self.filter = filter
		self.recursive = recursive
	
	def glob(self):
		"""
		Traverse directory, and return all absolute filenames of files that
		match the globbing patterns.
		"""
		matches = []
		for root, dirnames, filenames in os.walk(self.path):
			if not self.recursive:
				while len(dirnames) > 0:
					dirnames.pop()
			for filter in self.filter:
				for filename in fnmatch.filter(filenames, filter):
					matches.append(os.path.join(root, filename))
		return matches
