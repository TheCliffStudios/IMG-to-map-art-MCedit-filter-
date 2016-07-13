# This filter is a hack of @Sethbling's Player Statue filter. 
# It takes a (small) PNG from a web site and renders it vertically as blocks using @Sethbling's material mapping
# This hack @abrightmoore http://brightmoore.net
# Hacks marked up. All other code by @Sethbling, as below:

# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

# Edited for use of making maps by TheCLiffStudios + others
# https://www.youtube.com/channel/UClfE_OXIGhIw54kLuq-T8Cw
# see github for more detail https://github.com/TheCliffStudios/IMG-to-map-art-MCedit-filter-

from httplib import HTTPConnection
import png

displayName = "PNG to Blocks" # hack

inputs = (
	("Host", ("string", "value=i.imgur.com:80")), # hack
	("Path", ("string","value=/0SpgykC.jpg")), # hack
	("Horizontal", True),
)

materials = (
	(1,   3,  252,249,242), #diorite
    (2,   0,  125,176,55), #grass
    (4,   0,  111,111,111), #cobble
	(3,   0,  149,108,76), #dirt
    (9,   0,  63,63,252), #watter
    (12,   0,  244,230,161), #sand
	(5,   0,  141,118,71), #oak wood
    (18,   0,  0,123,0), #leaves
	(22,  0,   73,129,252), #lapis
	(35,  0,  252,252,252), #white wool
	(35,  1,  213,125,50), # orange wool
	(35,  2,  176,75,213), # magenta wool
	(35,  3,  101,151,213),# light blue wool
	(35,  4,  226,226,50), # yellow wool
	(35,  5,   125,202,25), # lime wool
	(35,  6,  239,125,163), # pink wool
	(35,  7,   75,75,75), # grey wool
	(35,  8,  151,151,151), # light grey wool
	(35,  9,   75,125,151), # cyan wool
	(35, 10,  125,62,176), # purple wool
	(35, 11,   50,75,176), # blue wool
	(35, 12,   101,75,50), # brown wool
	(35, 13,   101,125,50), # green wool
	(35, 14,  151,50,50), # red wool
	(35, 15,   25,25,25), # black wool
    (82,  0,  162,166,182), # clay
	(42,  0, 165,165,165), # iron block
    (46,  0,  255, 0, 0), # tnt
	(49,  0,   127,85,48	), # obsidian
	(57,  0,   91,216,210), # diamond
	(87,  0,  111,2,0), # netherrack
	(133, 0,   0,214,57), # emrald
    (170, 0,  247,235,76), # hay bale
    (174, 0,  158,158,252) # packed ice
)
def getPixel(pixels, x, y):
	idx = x*4
	return (pixels[y][idx], pixels[y][idx+1], pixels[y][idx+2], pixels[y][idx+3])
	
def transparent((r, g, b, a)):
	return a < 128
	
def closestMaterial((r, g, b, a)):
	closest = 255*255*3
	best = (35, 0)
	for (mat, dat, mr, mg, mb) in materials:
		(dr, dg, db) = (r-mr, g-mg, b-mb)
		dist = dr*dr+dg*dg+db*db
		if dist < closest:
			closest = dist
			best = (mat, dat)
	
	return best

def perform(level, box, options):
	host = options["Host"] # hack
	conn = HTTPConnection(host, timeout=10000) # hack
	path = options["Path"] # hack
	horizontal = options["Horizontal"] # hack
	print "Retrieving " + path + " from " + host # hack
	conn.request("GET", path)
	response = conn.getresponse()
	print response.status, response.reason
		
	data = response.read()
	conn.close()
	
	reader = png.Reader(bytes=data)
	(width, height, pixels, metadata) = reader.asRGBA8()
	pixels = list(pixels)
	
	for x in xrange(0, width): # hack
		y = height # hack
		while y > 0: # hack
			colour = getPixel(pixels, x, height-y) # hack
			if not transparent(colour):
				(mat, dat) = closestMaterial(colour)
				if horizontal == True:
					level.setBlockAt(box.minx + x, box.miny, box.minz+y, mat) # hack
					level.setBlockDataAt(box.minx + x, box.miny, box.minz+y, dat) # hack
				else:
					level.setBlockAt(box.minx + x, box.miny+y, box.minz, mat) # hack
					level.setBlockDataAt(box.minx + x, box.miny+y, box.minz, dat) # hack
			y = y - 1 # hack
			