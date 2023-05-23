from copy import copy
from math import isclose

class Point:
	def __init__(self, x = 0., y = 0.):
		self.x = x
		self.y = y

	def __repr__(self):
		return f"Point{str(self)}"

	def __str__(self):
		return f"({self.x}, {self.y})"

class Polygon:
	def __init__(self, vertices: list):
		self.vertices = vertices

	def _area_n(self, n: int):
		v = self.vertices
		a = 0.
		for i in range(n):
			w = v[(i + 1) % len(v)]
			a += v[i].x * w.y - v[i].y * w.x
		return a / 2

	def add_vertex(self, v: Point):
		self.vertices.append(v)

	def area(self):
		return self._area_n(len(self.vertices))

	def reduce_to_area(self, area: float):
		v = self.vertices
		# We copy the last vertex to avoid modifying the original point
		v[-1] = copy(v[-1])
		c, p, q = v[0], v[-2], v[-1]
		a = 2 * self._area_n(len(v) - 2)
		area = 2 * area - a
		if p.x == q.x:
			# x is known, we must find y
			q.y = (area - q.x * (c.y - p.y)) / (p.x - c.x)
		else:
			# y is known, we must find x
			q.x = (area - q.y * (p.x - c.x)) / (c.y - p.y)

	def __repr__(self):
		return f"Polygon({self.vertices})"

	def __str__(self):
		return str(self.vertices)

def nparts(l: int, w: int, n: int) -> list:
	if l < w:
		l, w = w, l
	if w < 1:
		raise ValueError("length and width must be greater than 0")
	if n < 2:
		raise ValueError("n must be greater than 1")

	# Create rectangle R
	R = [Point(0, 0), Point(l, 0), Point(l, w), Point(0, w)]

	# Convert R to Polygon
	PR = Polygon(R)

	AR = float(l * w)
	AP = AR / n
	if AP < 1: # Avoid too small areas
		raise ValueError("area of each polygon is too small")

	# Create list of polygons P
	P = []
	# Create center point c
	C = Point(l / 2, w / 2)
	# Fix the first point p1 to be the top center point
	p1 = Point(l / 2, 0)
	# Set the indice of the next vertex to be added to the current polygon
	Ri = 0

	# We create n polygons
	for _ in range(n):
		# Create a new polygon based on the previous one
		p = Polygon([C, p1])
		Ap = 0.
		# We add vertices until the area is greater than AP
		while Ap < AP:
			Ri = (Ri + 1) % len(R)
			p.add_vertex(R[Ri])
			Ap = p.area()
		if not isclose(Ap, AP):
			# We solve the system of equations to find the correct vertex
			p.reduce_to_area(AP)
			Ap = p.area()
			Ri = (len(R) + Ri - 1) % len(R)
		# We add the polygon to the list
		P.append(p)
		# We set the next point to be the last vertex of the polygon
		p1 = p.vertices[-1]
	return P
