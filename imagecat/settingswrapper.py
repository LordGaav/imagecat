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


class SettingsWrapper(object):
	""" Base class for manipulating GConfig / GSettings. """

	def _init_settings(self, profile=None):
		""" Calls to this functions should cause the internal settings to load or refresh. """
		raise NotImplementedError("_init_settings is not implemented.")

	def _check_list_type(self, lst, tp):
		"""
		Performs a simple validation of the given list against the given type,
		by filtering the list against the type. If the filtered list has a different
		length than the input, this function returns False.
		"""
		if tp == "hex":
			try:
				filtered = map(lambda x: int(x.replace("#", ""), 16), lst)
			except:
				return False
		else:
			filtered = filter(lambda x: isinstance(x, tp), lst)
		return len(lst) == len(filtered)

	def _get_string_array(self, key):
		"""Retrieve a list of string from a key."""
		raise NotImplementedError("_get_string_array is not implemented.")

	def _get_int_array(self, key):
		"""Retrieve a list of integers from a key."""
		raise NotImplementedError("_get_int_array is not implemented.")

	def _get_int(self, key):
		"""Retrieve a single integer from a key."""
		raise NotImplementedError("_get_int is not implemented.")

	def _set_hexstring_array(self, key, lst):
		""" Set a list of hexadecimal strings to a key. The input must be validated.  """
		raise NotImplementedError("_set_hexstring_array not implemented.")

	def _set_string_array(self, key, lst):
		""" Set a list of strings to a keys. The input must be validated. """
		raise NotImplementedError("_set_string_array not implemented.")

	def _set_int_array(self, key, lst):
		""" Set a list of integers to a keys. The input must be validated. """
		raise NotImplementedError("_set_int_array not implemented.")

	def delay(self):
		""" Enable delay mode. Revert active changes with revert(). Apply them with apply(). """
		raise NotImplementedError("delay not implemented.")

	def revert(self):
		""" Revert active changes. Only valid after delay(). """
		raise NotImplementedError("revert not implemented.")

	def apply(self):
		""" Apply active changes. Only valid after delay(). """
		raise NotImplementedError("apply not implemented.")
