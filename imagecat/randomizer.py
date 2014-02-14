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

import hashlib
import random


class Randomizer(object):
	"""
	Randomizes returned values from a list.
	"""
	def __init__(self, lst):
		"""
		Initializes a new Randomizer with a list. Altough a list of any
		type may work, Randomizer is intended to work with lists of 
		strings. Your mileage may vary.
		"""
		self.list = lst
		self.generate_checksum()
	
	def generate_checksum(self):
		"""
		Checksums the internal list, by concatenating the values and
		separating them with pipes, and creating a SHA1 hash of the
		resulting string.
		"""
		shasum = hashlib.sha1()

		for item in self.list:
			shasum.update(str(item))
			shasum.update("|")

		self.checksum = shasum.hexdigest()
		return self.checksum
	
	def get_random(self, count=1, blacklist=[]):
		"""
		Retrieves random items from the internal list, taking into
		account the blacklist. If the remaining possible choices, after
		removing the blacklisted items from the internal list, is lower
		than the requested amount, a KeyError is raised.
		"""
		temp = filter(lambda x: not x in blacklist, self.list)

		if len(temp) < count:
			raise KeyError("Randomizer list does not contain enough values.")

		i = 0

		out = []
		while i < count:
			r = random.choice(temp)

			if r in out:
				continue

			out.append(r)
			i += 1

		return out
