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

from settingswrapper import SettingsWrapper
import gconf

SCALECROP = 0
SCALE = 1
CENTERED = 2
TILED = 3
CENTERTILED = 4

SOLIDFILL = 0
GRADIENTVERT = 1
GRADIENTHORIZ = 2

class GConfSettingsWrapper(SettingsWrapper):
	""" Base class for manipulating settings in GConf. """

	def _init_settings(self, base_key, schema_key):
		""" Refreshes the internal GConf settings handle. """
		self.base_key = base_key
		self.schema_key = schema_key
		self.settings = gconf.client_get_default()

	def _get_string_array(self, key):
		"""Retrieve a list of string from a key in GConf."""
		return self.settings.get_list(self.base_key + key, gconf.VALUE_STRING)

	def _get_int_array(self, key):
		"""Retrieve a list of integers from a key in GConf."""
		return self.settings.get_list(self.base_key + key, gconf.VALUE_INT)

	def _get_int(self, key):
		"""Retrieve a single integer from a key in GConf."""
		return self.settings.get_int(self.base_key + key)

	def _set_hexstring_array(self, key, lst):
		""" Set a list of hexadecimal strings to a key in GConf. The input is validated.  """
		if not self._check_list_type(lst, "hex"):
			raise TypeError("List of %s contains non-hexadecimal strings" % key)
		return self.settings.set_list(self.base_key + key, gconf.VALUE_STRING, lst)

	def _set_string_array(self, key, lst):
		""" Set a list of strings to a key in GConf. The input is validated. """
		if not self._check_list_type(lst, basestring):
			raise TypeError("List of %s contains non-strings" % key)
		return self.settings.set_list(self.base_key + key, gconf.VALUE_STRING, lst)

	def _set_int_array(self, key, lst):
		""" Set a list of integers to a key in GConf. The input is validated. """
		if not self._check_list_type(lst, int):
			raise TypeError("List of %s contains non-hexadecimal strings" % key)
		return self.settings.set_list(self.base_key + key, gconf.VALUE_INT, lst)

	def delay(self):
		""" Delay mode does not exist on GConf, do a no-op."""
		return True

	def revert(self):
		""" Revert active changes. Does not work on GConf, do a no-op. """
		return True

	def apply(self):
		""" Apply active changes. Suggest as sync to GConf. """
		return self.settings.suggest_sync()


class CorePluginSettings(GConfSettingsWrapper):
	""" Set and retrieves global settings for Compiz (for Ubuntu 12.04). """
	base_key = "/apps/compiz-1/general/screen0/options/"
	""" Base key where the global settings are in GConf. """
	schema_key = None

	ACTIVEPLUGINS_KEY = "active_plugins"

	def __init__(self):
		self._init_settings(self.base_key, self.schema_key)

	def get_activated_plugins(self):
		""" Retrieve the currently activated Compiz plugins. """
		return self._get_string_array(self.ACTIVEPLUGINS_KEY)

	def set_activated_plugins(self, plugins):
		""" Set the currently activated Compiz plugins. """
		return self._set_string_array(self.ACTIVEPLUGINS_KEY, plugins)

class WallpaperPluginSettings(GConfSettingsWrapper):
	""" Sets and retrieves settings for the Compiz Wallpaper plugin (for Ubuntu 12.04).  """

	base_key = "/apps/compiz-1/plugins/wallpaper/screen0/options/"
	""" Base key where the Wallpaper plugin keeps its settings in GConf. """
	schema_key = "org.freedesktop.compiz.wallpaper"
	""" Schema definition for Wallpaper plugin's settings. """

	BGIMAGE_KEY = "bg_image"
	BGCOLOR1_KEY = "bg_color1"
	BGCOLOR2_KEY = "bg_color2"
	BGFILLTYPE_KEY = "bg_fill_type"
	BGIMAGEPOS_KEY = "bg_image_pos"

	def __init__(self):
		self._init_settings(self.base_key, self.schema_key)
	
	def get_bg_image(self):
		""" Retrieve the currently set background images from GSettings. """
		return self._get_string_array(self.BGIMAGE_KEY)

	def get_bg_color1(self):
		""" Retrieve the currently set background start colors from GSettings. """
		return self._get_string_array(self.BGCOLOR1_KEY)

	def get_bg_color2(self):
		""" Retrieve the currently set background end colors from GSettings.  """
		return self._get_string_array(self.BGCOLOR2_KEY)

	def get_bg_fill_type(self):
		""" Retrieve the currently set background fill types from GSettings. """
		return self._get_int_array(self.BGFILLTYPE_KEY)

	def get_bg_image_pos(self):
		""" Retrieve the currently set background image positions from GSettings. """
		return self._get_int_array(self.BGIMAGEPOS_KEY)

	def set_bg_image(self, filenames):
		""" Set background images to given filenames. Must be provided as a list of strings. """
		return self._set_string_array(self.BGIMAGE_KEY, filenames)

	def set_bg_color1(self, colors):
		""" Set background start colors. Must be provided as a list of hexadecimal strings. """
		return self._set_hexstring_array(self.BGCOLOR1_KEY, colors)

	def set_bg_color2(self, colors):
		""" Set background end colors. Must be provided as a list of hexadecimal strings. """
		return self._set_hexstring_array(self.BGCOLOR2_KEY, colors)

	def set_bg_fill_type(self, types):
		""" Set background fill types. Must be provided as a list of integers. """
		return self._set_int_array(self.BGFILLTYPE_KEY, types)

	def set_bg_image_pos(self, pos):
		""" Set background image positions. Must be provided as a list of integers. """
		return self._set_int_array(self.BGIMAGEPOS_KEY, pos)

if __name__ == "__main__":
	c = CorePluginSettings()
	plugins = c.get_activated_plugins()
	print "wallpaper" in plugins
	if "wallpaper" in plugins:
		plugins.remove("wallpaper")
	else:
		plugins.append("wallpaper")
	c.set_activated_plugins(plugins)

	w = WallpaperPluginSettings()
	print w.get_bg_image()
	print w.get_bg_color1()
	print w.get_bg_color2()
	print w.get_bg_fill_type()
	print w.get_bg_image_pos()
