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

from gi.repository import Gio, GLib

SCALECROP = 0
SCALE = 1
CENTERED = 2
TILED = 3
CENTERTILED = 4

SOLIDFILL = 0
GRADIENTVERT = 1
GRADIENTHORIZ = 2

class WallpaperPluginSettings(object):
	"""
	Sets and retrieves settings for the Compiz Wallpaper plugin.
	"""

	default_profile = "unity"
	""" Default GConf profile to use. Ubuntu uses "unity" by default.  """
	base_key = "/org/compiz/profiles/%s/plugins/wallpaper/"
	""" Base key where the Wallpaper plugins keeps its settings in GConf. """
	schema_key = "org.compiz.wallpaper"
	""" Schema definition for Wallpaper plugin's settings. """

	def __init__(self, profile=None):
		self._init_settings(profile)

	def _init_settings(self, profile=None):
		""" Refreshes the internal GConf settings handle.  """
		if profile == None:
			profile = self.default_profile
		base_key = self.base_key % (profile)
		self.settings = Gio.Settings(self.schema_key, base_key)
	
	def _check_list_type(self, lst, tp):
		""" 
		Performs a simple validation of the given list against the given type,
		by filtering the list against the type. If the filtered list has a different
		length than the input, this function returns False.
		"""
		if tp == "hex":
			try:
				filtered = map(lambda x: int(x, 16), lst)
			except:
				return False
		else:
			filtered = filter(lambda x: isinstance(x, tp), lst)
		return len(lst) == len(filtered)

	def _set_hexstring_array(self, key, lst):
		""" Set a list of hexadecimal strings to a key in GConf. The input is validated.  """
		if not self._check_list_type(lst, "hex"):
			raise TypeError("List of %s contains non-hexadecimal strings" % key)
		return self.settings.set_value(key, GLib.Variant("as", lst))

	def _set_string_array(self, key, lst):
		""" Set a list of strings to a key in GConf. The input is validated. """
		if not self._check_list_type(lst, basestring):
			raise TypeError("List of %s contains non-strings" % key)
		return self.settings.set_value(key, GLib.Variant("as", lst))

	def _set_int_array(self, key, lst):
		""" Set a list of integers to a key in GConf. The input is validated. """
		if not self._check_list_type(lst, int):
			raise TypeError("List of %s contains non-hexadecimal strings" % key)
		return self.settings.set_value(key, GLib.Variant("ai", lst))
	
	def get_bg_image(self):
		""" Retrieve the currently set background images from GConf. """
		return self.settings.get_strv("bg-image")

	def get_bg_color1(self):
		""" Retrieve the currently set background start colors from GConf. """
		return self.settings.get_strv("bg-color1")

	def get_bg_color2(self):
		""" Retrieve the currently set background end colors from GConf.  """
		return self.settings.get_strv("bg-color2")

	def get_bg_fill_type(self):
		""" Retrieve the currently set background fill types from GConf. """
		return self.settings.get_value("bg-fill-type")

	def get_bg_image_pos(self):
		""" Retrieve the currently set background image positions from GConf. """
		return self.settings.get_value("bg-image-pos")

	def set_bg_image(self, filenames):
		""" Set background images to given filenames. Must be provided as a list of strings. """
		return self._set_string_array("bg-image", filenames)

	def set_bg_color1(self, colors):
		""" Set background start colors. Must be provided as a list of hexadecimal strings. """
		return self._set_hexstring_array("bg-color1", colors)

	def set_bg_color2(self, colors):
		""" Set background end colors. Must be provided as a list of hexadecimal strings. """
		return self._set_hexstring_array("bg-color2", colors)

	def set_bg_fill_type(self, types):
		""" Set background fill types. Must be provided as a list of integers. """
		return self._set_int_array("bg-fill-type", types)

	def set_bg_image_pos(self, pos):
		""" Set background image positions. Must be provided as a list of integers. """
		return self._set_int_array("bg-image-pos", pos)

if __name__ == "__main__":
	w = WallpaperPluginSettings()
	print w.get_bg_image()
	print w.get_bg_color1()
	print w.get_bg_color2()
	print w.get_bg_fill_type()
	print w.get_bg_image_pos()
