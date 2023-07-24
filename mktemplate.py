#!/usr/bin/env python3

import itertools as it
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

#CONFIG#
canvas_min = (-1500, -1000)
canvas_max = (1000,1000)
image_dir = "images"

grid_dir = "grids"
grid_scale = 50
grid_thickness = 1
########

#
# make sure PIL (pillow) package is installed
# place all the images in image_dir formatted as [name].[posX].[posY].png
# example file: myname.400.234.png
# they will be applied in alphabetical order
#

canvas_size =  canvas_max[0] - canvas_min[0], canvas_max[1] - canvas_min[1]

def getCoords(filename):
	nameparts = filename.split(".")
	return (int(nameparts[1]) - canvas_min[0],int(nameparts[2]) - canvas_min[1])

def makeGrid(filename,coords):
	coords = coords[0] + canvas_min[0], coords[1] + canvas_min[1]
	orig = Image.open(filename).convert("RGBA")
	new = orig.resize((orig.size[0]*grid_scale, orig.size[1]*grid_scale), resample=Image.NEAREST)
	draw = ImageDraw.Draw(new)
	font = ImageFont.truetype("LiberationMono-Bold.ttf", size=14)
	for x, y in it.product(range(orig.size[0]), range(orig.size[1])):
		color = orig.getpixel((x,y))
		if color[3] != 0: #not transparent
			if color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114 > 186:
				textcolor = "black"
			else:
				textcolor = "white"

			draw.text((x*grid_scale*grid_thickness, y*grid_scale*grid_thickness), f"{x + coords[0]}", font=font, fill=textcolor)
			draw.text((x*grid_scale*grid_thickness, y*grid_scale*grid_thickness + 14), f"{y + coords[1]}", font=font, fill=textcolor)

	for x in range(orig.size[0]):
		draw.line((x*grid_scale*grid_thickness, 0, x*grid_scale*grid_thickness, orig.size[1]*grid_scale*grid_thickness), fill="black")
	for y in range(orig.size[1]):
		draw.line((0, y*grid_scale*grid_thickness, orig.size[0]*grid_scale*grid_thickness, y*grid_scale*grid_thickness), fill="black")
	return new

def pastePos(pos, x, y):
	return (pos[0] + x) * 3 + 1, (pos[1] + y) * 3 + 1

def paste(base, image, pos):
	pixels = image.load()
	base_pixels = base.load()
	for x in range(image.width):
		for y in range(image.height):
			if pixels[x, y] != (0 ,0 ,0 ,0):
				base_pixels[pastePos(pos, x, y)] = pixels[x, y]


base = Image.new("RGBA",(canvas_size[0] * 3, canvas_size[1] * 3),(0,0,0,0))
files = Path(image_dir).glob('*')
for file in sorted(files):
	with Image.open(file).convert("RGBA") as ifile:
		paste(base, ifile, getCoords(file.name))
		print("pasting",file)

base.save("template.png","png")

grids = Path(grid_dir)
files = Path(image_dir).glob('*')
for file in files:
	makeGrid(file,getCoords(file.name)).save(grids.joinpath(file.name),"png")
	print("creating",grids.joinpath(file.name))
