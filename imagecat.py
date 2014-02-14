#!/usr/bin/env python

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


image1 = Image.open("081.jpg")
image2 = Image.open("084.jpg")

montage([cropresize(image1, (1920, 1080)), cropresize(image2, (1920, 1080))], HORIZONTAL).save("canvas.png")
