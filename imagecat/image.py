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

# I want PROPER divisions, please
from __future__ import division
import Image

HORIZONTAL = 0
VERTICAL = 1

def cropresize(im, size, mode=Image.BICUBIC):
	orig = im.size

	if orig[0] < orig[1]:
		newx = int((orig[0] / orig[1]) * size[1])
		intermediate = im.resize((newx, size[1]), mode)
	else:
		newy = int((orig[1] / orig[0]) * size[0])
		intermediate = im.resize((size[0], newy), mode)
	
	isize = intermediate.size

	leftx = int(isize[0] / 2 - size[0] / 2)
	lefty = int(isize[1] / 2 - size[1] / 2)
	
	return intermediate.crop((leftx, lefty, leftx + size[0], lefty + size[1]))

def montage(images, direction):
	totalx = 0
	totaly = 0

	for image in images:
		if direction == HORIZONTAL:
			totalx += image.size[0]
			if image.size[1] > totaly:
				totaly = image.size[1]
		else:
			totaly += image.size[1]
			if image.size[0] > totalx:
				totalx = image.size[0]
	
	canvas = Image.new("RGB", (totalx, totaly))

	pointer = 0
	for image in images:
		if direction == HORIZONTAL:
			canvas.paste(image, (pointer, 0))
			pointer += image.size[0]
		else:
			canvas.paste(image, (0, pointer))
			pointer += image.size[1]
	
	return canvas
