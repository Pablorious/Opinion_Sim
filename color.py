from random import randint, random, uniform

class Color(object):
	BLACK     = (  0,  0,  0)
	BLACKGREY = ( 63, 63, 63)
	GREY      = (127,127,127)
	GREYWHITE = (191,191,191)	
	WHITE     = (255,255,255)
	
	RED       = (255,  0,  0)
	GREEN     = (  0,255,  0)
	BLUE      = (  0,  0,255)
	
	CYAN      = (  0,255,255)
	YELLOW    = (255,255,  0)
	MAGENTA   = (255,  0,255)
	
	@staticmethod
	def random_rgb(low=0,high=255):
		return (randint(low,high),randint(low,high),randint(low,high))
	
	@staticmethod
	def random_hsl(low=0.0,high=1.0):
		h = randint(0,359)
		s = random()
		l = uniform(low,high) 
		return (h,s,l)

	@staticmethod
	def rgb_to_hsl(rgb):
		r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
		cmax, cmin = max(r, g, b), min(r, g, b)
		delta = cmax - cmin
		
		if delta == 0:
			hue = 0
		elif cmax == r:
			hue = (60 * ((g - b) / delta) + 360) % 360
		elif cmax == g:
			hue = (60 * ((b - r) / delta) + 120) % 360
		else:
			hue = (60 * ((r - g) / delta) + 240) % 360
		
		lightness = (cmax + cmin) / 2.0
		if delta == 0:
			saturation = 0
		else:
			saturation = delta / (1 - abs(2 * lightness - 1))
		
		return (hue, saturation, lightness)
	
	@staticmethod
	def hsl_to_rgb(hsl):
		h,s,l = hsl[0],hsl[1],hsl[2]
		c = (1 - abs(2 * l - 1)) * s
		x = c * (1 - abs((h / 60) % 2 - 1))
		m = l - c/2.0
		
		if h < 60:
			r, g, b = c, x, 0
		elif h < 120:
			r, g, b = x, c, 0
		elif h < 180:
			r, g, b = 0, c, x
		elif h < 240:
			r, g, b = 0, x, c
		elif h < 300:
			r, g, b = x, 0, c
		else:
			r, g, b = c, 0, x
			
		r, g, b = (r+m)*255, (g+m)*255, (b+m)*255
		return (int(r), int(g), int(b))

	@staticmethod
	def get_colors_by_lightness(l, d):
		colors = []
		for r in range(256):
			r_lightness = 0.33 * r
			if r_lightness - l >= d:
				continue
			for g in range(256):
				g_lightness = 0.55 * g
				if r_lightness + g_lightness - l  >= d:
					continue
				for b in range(256):
					b_lightness = 0.11 * b
					lightness = r_lightness + g_lightness + b_lightness
					if abs(lightness - l) >= d:
						continue
					colors.append((r, g, b))
		return colors

