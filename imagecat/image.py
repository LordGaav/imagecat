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

"""
Functions to manipulate images. All methods that process images expect a
properly initiated PIL Image object.
"""

# I want PROPER divisions, please
from __future__ import division
import Image


def cropresize(im, size, mode=Image.BICUBIC):
	"""
	Scales a PIL Image to the specified size, cropping the parts that
	would fall outside the specified dimensions. A PIL resize mode may be
	specified, bicubic resize is the default, use NEAREST/BILINEAR/BICUBIC
	globals specified in the PIL Image module.
	"""
	orig = im.size
	orig_ratio = orig[0] / orig[1]
	size_ratio = size[0] / size[1]

	def horizontal_fit(orig, size):
		ratio = orig[0] / orig[1]
		newx = size[0]
		newy = int(newx / ratio)
		return (newx, newy)

	def vertical_fit(orig, size):
		ratio = orig[0] / orig[1]
		newy = size[1]
		newx = int(newy * ratio)
		return (newx, newy)

	if size_ratio > orig_ratio:
		newsize = horizontal_fit(orig, size)
	else:
		newsize = vertical_fit(orig, size)

	intermediate = im.resize(newsize, mode)
	isize = intermediate.size

	leftx = int(isize[0] / 2 - size[0] / 2)
	lefty = int(isize[1] / 2 - size[1] / 2)

	return intermediate.crop((leftx, lefty, leftx + size[0], lefty + size[1]))


def montage(images, offsets):
	"""
	Takes a list of PIL Images and offsets, and montages together. The result is
	one big PIL Image with all specified Images contained in it, at the specified
	offsets.
	"""
	totalx = 0
	totaly = 0

	for image, offset in zip(images, offsets):
		size = image.size
		if (offset[0] > size[0] and (offset[0] + size[0]) > totalx):
			totalx = offset[0] + size[0]
		if (offset[1] > size[1] and (offset[1] + size[1]) > totaly):
			totaly = offset[1] + size[1]

		if totalx == 0 or (offset[0] + size[0]) > totalx:
			totalx = (offset[0] + size[0])
		if totaly == 0 or (offset[1] + size[1]) > totaly:
			totaly = (offset[1] + size[1])

	canvas = Image.new("RGB", (totalx, totaly))

	for image, offset in zip(images, offsets):
		canvas.paste(image, (offset[0], offset[1]))

	return canvas
