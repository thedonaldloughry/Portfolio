# physics.py: A collection of classes / functions for doing
#			 physics simulations
import math3d
import pygame

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#@@@@@@@ COLLISION BODY CLASSES @@@@@@#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

#################################################
# Body class                                    #
#################################################
class Body(object):
	""" A generic type of object that is subject to the
		laws of physics.  Initially this is just used as an
		"interface" class (plus a color).  If enableRigidBody is
		called it then is capable of being a part of a Simulation below. """
	def __init__(self, material = None):
		""" The constructor.  Just sets the color """
		self.material = material
		#self.color = self.material["diffuse"]   # (temporary)

	def enableRigidBody(self, initialPos, initalVel, mass):
		""" 'Turns on' physics-related functionality.  The user must pass the initial position,
            velocity, and mass """
		if not isinstance(initialPos, math3d.VectorN) or \
		   not isinstance(initialVel, math3d.VectorN) or \
		   initialPos.dim != initialVel.dim:
		   	raise TypeError("Position and velocity must be equal-sized VectorN's")
		self.pos = initialPos.copy()
		self.vel = initialVel.copy()
		self.mass = mass
		self.accel = math3d.VectorN(self.pos.dim)

	def applyForce(self, F):
		""" Applies the given force to this object (an impulse force).
			Use Newton's second law to ADD to self.accel. """
		self.accel += F / self.mass

	def update(self, dT):
		""" Applies the current acceleration to the velocity.  Then
			applies the (new) velocity to the position.  Finally this
			method should zero out our accel vector. """
		if hasattr(self, "vel"):
			self.vel += self.accel * dT
			self.pos += self.vel * dT
			for i in range(len(self.accel)):
				self.accel[i] = 0.0

	def drawPygame(self, surf):
		""" Draws this body to the given surface.  This is meant to be defined
		    by derived classes. """
		pass

#################################################
# Spheroid class                                #
#################################################
class Spheroid(Body):
	""" A specific type of body.  Here a (2D/3D/nD) circle """
	def __init__(self, pos, radius, material):
		""" The constructor.  pos is a VectorN for the center, radius is the
		    scalar radius of the circle. """
		Body.__init__(self, material)
		self.pos = pos.copy()
		self.radius = radius

	def drawPygame(self, surf):
		""" Draws a 2D (projection) of this spheroid """
		pygame.draw.circle(surf, self.color, (int(self.pos[0]), int(self.pos[1])), \
					  int(self.radius), 2)

#################################################
# Plane class                                   #
#################################################
class Plane(Body):
	""" A specific type of body.  Here a (2D/3D/nD) infinite plane """
	def __init__(self, normal, d, material = None):
		""" The constructor.  normal is a VectorN, d is the scalar distance
		    from the origin (in the direction of the normal) to get onto the plane.
		    Note: The d value is negative if we have to go in the opposite direction
		    of the normal to get on the plane. """
		Body.__init__(self, material)
		self.normal = normal.normalized()
		self.d = d

	def drawPygame(self, surf):
		""" Draws a 2D (projection) of this plane to the given surface """
		# First, see if this is more of a vertical or horizontal plane
		if abs(math3d.dot(self.normal, math3d.Vector2(1,0))) > \
		   abs(math3d.dot(self.normal, math3d.Vector2(0,1))):
		   	# More vertical-ish
		   	# So...get a (x,y) point at the top and bottom
			pt1 = math3d.Vector2(self.d / self.normal[0], 0)
			pt2 = math3d.Vector2((self.d - self.normal[1] * surf.get_height()-1) / self.normal[0], surf.get_height()-1)
		else:
			# More horizontal-ish
			# So...get a (x,y) point at the left and right.
			pt1 = math3d.Vector2(0, self.d / self.normal[1])
			pt2 = math3d.Vector2(surf.get_width()-1, (self.d - self.normal[0] * surf.get_width()-1)/self.normal[1])
		# Draw the actual plane
		pygame.draw.line(surf, self.color, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), 2)
		# Draw an indicator for the normal vector at the mid-point of pt1 and pt2.
		ptm = (pt1 + pt2) / 2
		ptm2 = ptm + 15 * self.normal
		pygame.draw.line(surf, self.color, (int(ptm[0]), int(ptm[1])), (int(ptm2[0]), int(ptm2[1])), 1)

#################################################
# Ray class                                     #
#################################################
class Ray(Body):
	""" A specific type of body.  Here a (2D/3D/nD) ray """
	def __init__(self, origin, direction, material = None):
		""" The constructor.  origin and direction are both VectorN's """
		Body.__init__(self, material)
		self.origin = origin.copy()
		self.direction = direction.normalized()

	def getPt(self, t):
		""" Gets a point which is t (a scalar) units along this ray. """
		return self.origin + t * self.direction

	def drawPygame(self, surf):
		""" Draws a 2D (projection) of this ray to the given surface """
		o = (int(self.origin[0]), int(self.origin[1]))
		pygame.draw.circle(surf, self.color, o, 4, 0)
		# This is a bit of a hack.  I'm calculating the farthest point along a ray
		# (if the origin were at the upper-left and the ray were pointing to the lower-right
		# of the screen).  Then let pygame clip off pixels that are off-screen.
		bigNum = surf.get_width() ** 2 + surf.get_height() ** 2
		endPt = self.getPt(bigNum)
		# Draw a line between the origin and the far-away point.
		pygame.draw.line(surf, (64,64,64), o, (int(endPt[0]), int(endPt[1])))
		endPt = self.getPt(15)
		# Draw a circle at the origin.
		pygame.draw.line(surf, self.color, o, (int(endPt[0]), int(endPt[1])))


#################################################
# AABB class                                    #
#################################################
class AABB(Body):
	""" A specific type of body.  Here a (2D/3D/nD) axis-aligned (bounding) box """
	def __init__(self, minPt, maxPt, material = None):
		""" The constructor.  The minPt and maxPt define the corners of the AABB """
		if not isinstance(minPt, math3d.VectorN) or not isinstance(maxPt, math3d.VectorN) or \
		                    minPt.dim != maxPt.dim:
			raise TypeError("You must pass two equally-sized VectorN's for min & maxPt")
		Body.__init__(self, material)
		self.minPt = minPt.copy()
		self.maxPt = maxPt.copy()

	def resetBounds(self):
		""" Resets the boundary points of the box.  It won't draw if these remain None """
		self.minPt = None
		self.maxPt = None

	def updateBounds(self, pt):
		""" Updates the min/max point given the value of this new point """
		if not isinstance(pt, math3d.VectorN):
			raise TypeError("Invalid point")
		elif self.minPt != None and pt.dim != self.minPt.dim:
			raise TypeError("Invalid dimension (" + str(pt.dim) + \
		                ") -- doesn't match existing dimension (" + str(self.minPt.dim) + ")")
		if self.minPt == None:
			self.minPt = pt.copy()
			self.maxPt = pt.copy()
		else:
			for i in range(self.minPt.dim):
				if pt[i] < self.minPt[i]:
					self.minPt[i] = pt[i]
				if pt[i] > self.maxPt[i]:
					self.maxPt[i] = pt[i]


	def drawPygame(self, surf):
		""" Draws a 2D (projection) of this box to the given surface. """
		if self.minPt != None and self.maxPt != None:
			pygame.draw.rect(surf, self.color, (int(self.minPt[0]), int(self.minPt[1]), \
							   int(self.maxPt[0] - self.minPt[0]), int(self.maxPt[1] - self.minPt[1])), 2)

	def getPts(self):
		""" Returns a copy of all the points of this object """
		if self.minPt.dim == 2:
			return (math3d.VectorN((self.minPt[0], self.minPt[1])), math3d.VectorN((self.minPt[0], self.maxPt[1])), \
					math3d.VectorN((self.maxPt[0], self.minPt[1])), math3d.VectorN((self.maxPt[0], self.maxPt[1])))
		elif self.minPt.dim == 3:
			return (math3d.VectorN((self.minPt[0], self.minPt[1], self.minPt[2])), math3d.VectorN((self.minPt[0], self.maxPt[1], self.minPt[2])), \
					math3d.VectorN((self.maxPt[0], self.minPt[1], self.minPt[2])), math3d.VectorN((self.maxPt[0], self.maxPt[1], self.minPt[2])), \
					math3d.VectorN((self.minPt[0], self.minPt[1], self.maxPt[2])), math3d.VectorN((self.minPt[0], self.maxPt[1], self.maxPt[2])), \
					math3d.VectorN((self.maxPt[0], self.minPt[1], self.maxPt[2])), math3d.VectorN((self.maxPt[0], self.maxPt[1], self.maxPt[2])))
		else:
			raise NotImplementedError("Sorry, not (yet) supported for hyper-boxes")


#################################################
# Triangle class                                #
#################################################
class Triangle(Body):
	""" A specific type of body.  Here a (2D/3D/nD) triangle """
	def __init__(self, pts, material = None):
		""" The constructor.  pts are 2-n equally-sized VectorN's """
		if not hasattr(pts, "__len__"):
		   	raise TypeError("You must pass 2-n equally-sized VectorN's for the points")
		self.pts = []
		for i in range(len(pts)):
			if not isinstance(pts[i], math3d.VectorN):
				raise TypeError("You must pass 2-n equally-sized VectorN's for the points")
			self.pts.append(pts[i].copy())
		Body.__init__(self, material)
		self.updateNormalAndD()

	def updateNormalAndD(self):
		""" Used to update the normal and d-value of the plane this triangle lies upon.
		    Any time the points change, this method should be called. """
		if len(self.pts) == 3 and self.pts[0].dim == 3:
			self.normal = math3d.cross(self.pts[1] - self.pts[0], self.pts[2] - self.pts[0]).normalized()
			self.d = math3d.dot(self.pts[0], self.normal)
		elif len(self.pts) == 2 and self.pts[0].dim == 2:
			v = (self.pts[1] - self.pts[0]).normalized()
			self.normal = math3d.Vector2(-v[1], v[0])
			self.d = math3d.dot(self.pts[0], self.normal)

	def drawPygame(self, surf):
		""" Draws a 2D (projection) of this triangle to the given surface. """
		drawList = []
		for p in self.pts:
			drawList.append((int(p[0]), int(p[1])))
		pygame.draw.polygon(surf, self.color, drawList, 2)



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#@@@@@@@ SIMULATION CLASS       @@@@@@#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

#################################################
# Simulator class                               #
#################################################
class Simulator(object):
	""" A collection of (physics-enabled) Body's """
	def __init__(self):
		""" The constructor.  Just initializes our list of walls and bodies """
		self.bodies = []
		self.walls = []	# Probably Plane objects

	def addBody(self, b):
		""" Adds (a reference to) the given body to our list of bodies. """
		if not isinstance(b, Body):
			raise TypeError("You must pass a Body object")
		self.bodies.append(b)

	def addWall(self, w):
		""" Adds a reference to the given plane to our list of walls. """
		if not isinstance(w, Plane):
			raise TypeError("You must pass a Plane object")
		self.walls.append(w)

	def update(self, dT):
		""" Updates all bodies """
		for b in self.bodies:
			b.update(dT)

	def applyGravity(self, gravityVector):
		""" Applies "normal" or "near-earth" gravity to all our
			objects.  Use our applyForce method. gravityVector contains the
			direction (and magnitude) of the gravity force.  Note: don't forget to
			multiply by the object's mass. """
		for b in self.bodies:
			# Note: I multiply by mass here.  The apply force method will divide
			# for mass, thus "proving" that all objects fall at the same speed (
			# in a vacuum) -- YAY GALILEO!
			b.applyForce(gravityVector * b.mass)

	def applyPlanetGravity(self, G, dT):
		""" Applies forces (using the gravitation formula and the given G constant)
			to all objects in the simulation """
		for i in range(len(self.bodies)):
			for j in range(i+1, len(self.bodies)):
				# Attract i towards j and j towards i.
				v = self.bodies[j].pos - self.bodies[i].pos
				v = v.normalized() * G * self.bodies[i].mass * self.bodies[j].mass / (v.length()**2)
				self.bodies[i].applyForce(v)
				self.bodies[j].applyForce(-v)

	def handleHits(self, tempCollisionMag, dT):
		""" Detect collisions between pairs of objects """
		# Note: This only checks for collisions between UNIQUE
		# pairs of objects (and doesn't check an object against
		# itself)
		for first in range(0, len(self.bodies)):
			for second in range(0, first):
				# See if self.bodies[first] hits self.bodies[second]
				f = self.bodies[first]
				s = self.bodies[second]
				result = circle_circle(f, s)
				# Handles the hit, if there is one
				hitTest = circle_circle(f, s)
				if hitTest != None:
					# The hacked version we did in class...
					#self.bodies[first].applyForce(tempCollisionMag * hitTest["correction1"])
					#self.bodies[second].applyForce(tempCollisionMag * hitTest["correction2"])
					# Push the objects away so they no longer penetrate
					#d = (hitTest["dist"] - self.bodies[first].radius - self.bodies[second].radius) / 2
					#self.bodies[first].pos +=  d * hitTest["correction1"]
					#self.bodies[second].pos += d * hitTest["correction2"]

					# The better version of what we had in class...
					norm = hitTest["correction1"].normalized()
					preV1_norm = norm.dot(f.vel) * norm
					preV2_norm = norm.dot(s.vel) * norm
					preV1_tan = f.vel - preV1_norm
					preV2_tan = s.vel - preV2_norm
					preNormSpeed1 = preV1_norm.length()
					preNormSpeed2 = preV2_norm.length()
					newNormSpeed1 = (preNormSpeed1 * (f.mass - s.mass) + 2 * s.mass * preNormSpeed2) / (f.mass + s.mass)
					newNormSpeed2 = (preNormSpeed2 * (s.mass - f.mass) + 2 * f.mass * preNormSpeed1) / (s.mass + f.mass)
					postNormSpeed1 = newNormSpeed1 * norm
					postNormSpeed2 = -newNormSpeed2 * norm
					f.vel = postNormSpeed1 + preV1_tan
					s.vel = postNormSpeed2 + preV2_tan


	def handleWallHits(self, rect, updateVel=True):
		""" Detect hits with a wall (bouncing off if we detect one). rect is a pygame-ish
			rect (leftX, topY, width, height).  If one is found, use the bouncing code on
			the slides to change velocity. """
		# Note: Once we add more types of bodies, we'll need to make this work for non-circle
		for b in self.bodies:
			newVel = b.vel.copy()
			for w in self.walls:
				plane_dist = math3d.dot(b.pos, w.normal)
				if plane_dist - b.radius < w.d:
					b.pos += w.normal * (w.d - plane_dist + b.radius)
					vel_paralel = math3d.dot(w.normal, b.vel) * w.normal
					newVel -= 2 * vel_paralel
			if updateVel:
				b.vel = newVel

	def drawPygame(self, surf):
		""" Draws all bodies and walls to the given surface """
		for b in self.bodies:
			b.drawPygame(surf)
		for w in self.walls:
			w.drawPygame(surf)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#@@@@@@@ COLLISION DETECTION functions @@@@@@#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def handle_collision(o1, o2):
	""" Detects collisions between two bodies. The real work is done by the
	    'helper' functions below. Each of the helper functions returns None if
		there is no collision, or a dictionary containing hit-related data if there
		was a collision (currently, all helper functions have at least a 'collisions'
		field, which is a list/tuple of VectorN's indicating collision point(s) """
	# Spheroid - ____ hit detection
	if isinstance(o1, Spheroid):
		if isinstance(o2, Spheroid):
			return spheroid_spheroid(o1, o2)
		if isinstance(o2, AABB):
			return aabb_spheroid(o2, o1)
		if isinstance(o2, Ray):
			return ray_spheroid(o2, o1)
		if isinstance(o2, Plane):
			return spheroid_plane(o1, o2)
	# Ray - ______ hit detection
	if isinstance(o1, Ray):
		if isinstance(o2, Plane):
			return ray_plane(o1, o2)
		if isinstance(o2, Spheroid):
			return ray_spheroid(o1, o2)
		if isinstance(o2, AABB):
			return ray_aabb(o1, o2)
		if isinstance(o2, Triangle):
			return ray_tri(o1, o2)
	# Plane - _________ hit detection
	if isinstance(o1, Plane):
		if isinstance(o2, Ray):
			return ray_plane(o2, o1)
		if isinstance(o2, Spheroid):
			return spheroid_plane(o2, o1)
		if isinstance(o2, AABB):
			return aabb_plane(o2, o1)
		if isinstance(o2, Triangle):
			return plane_tri(o1, o2)
	# AABB - ______ hit detection
	if isinstance(o1, AABB):
		if isinstance(o2, Ray):
			return ray_aabb(o2, o1)
		if isinstance(o2, AABB):
			return aabb_aabb(o1, o2)
		if isinstance(o2, Spheroid):
			return aabb_spheroid(o1, o2)
	# Triangle - _________ hit detection
	if isinstance(o1, Triangle):
		if isinstance(o2, Ray):
			return ray_tri(o1, o2)
		if isinstance(o2, Plane):
			return plane_tri(o2, o1)

	#raise NotImplementedError("Sorry, " + str(type(o1)) + "-" + str(type(o2)) + " isn't implemented yet!")
	return None



def spheroid_spheroid(c1, c2):
	""" Returns None if the two spheroids don't intersect.
		If they do, return a dictionary with the following keys:
			'dist': The (scalar) distance between them
			'correction1': The unit-length vector indicating the
				   direction c1 is "pushed" to remove the collision
			'correction2': The unit-length vector inidicating the
				   direction c2 is "pushed" to remove the collision (-correction1).
			'collisions': a list of collision points. """
	e = c1.pos - c2.pos
	dist = e.length()
	if dist < c1.radius + c2.radius:
		correct1 = e.normalized()
		correct2 = -correct1
		pts = (c1.pos + correct2 * c2.radius, c2.pos + correct1 * c1.radius)
		return {"dist" : dist, "correction1" : c1, "correction2" : c2, "collisions" : pts}
	else:
		return None


def ray_plane(r, p):
	""" Returns None if the ray (r) and plane (p) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	den = math3d.dot(p.normal, r.direction)
	if den == 0:
		# This will be the case if the ray is parallel to the plane
		return None
	num = p.d - math3d.dot(p.normal, r.origin)
	t = num / den
	if t < 0:
		# This is this case when the ray points away from the plane
		return None
	return {"collisions": (r.getPt(t),), "tlist" : (t,), "nlist" : (p.normal,)}

def ray_spheroid(r, s):
	""" Returns None if the ray (r) and spheroid (s) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	e = s.pos - r.origin
	elen = e.length()
	f = math3d.dot(e, r.direction)
	closestDist = (elen * elen - f * f) ** 0.5
	if closestDist > s.radius:
		# The ray misses the sphere completely
		return None
	elif closestDist == s.radius:
		# Unlikely, but will be the case if the ray just grazes the sphere
		return {"collisions": (r.getPt(f),), "tlist": (f,), "nlist": ((r.getPt(f) - s.pos).normalized(),)}
	offset = (s.radius ** 2 - closestDist ** 2) ** 0.5
	collisions = []
	tlist = []
	nlist = []
	if elen > s.radius:
		# The ray starts outside the sphere.  There will be up to two
		# collisions.  The check for positive 't' values is to make sure these
		# are along (and not behind) the ray.
		if f - offset > 0: collisions.append(r.getPt(f - offset)); tlist.append(f - offset); nlist.append((r.getPt(f - offset) - s.pos).normalized())
		if f + offset > 0: collisions.append(r.getPt(f + offset)); tlist.append(f + offset); nlist.append((r.getPt(f + offset) - s.pos).normalized())
	else:
		# The ray originates within the sphere.  There will be exactly one collision
		collisions.append(r.getPt(f + offset))
		tlist.append(f + offset)
		nlist.append((r.getPt(f + offset) - s.pos).normalized())
	if len(collisions) == 0:
		return None
	else:
		return {"collisions": collisions, "tlist": tlist, "nlist": nlist}


def ray_aabb(r, b):
	""" Returns None if the ray (r) and aabb (b) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	if r.origin.dim == 2:
		normals = (math3d.Vector2(0,1), math3d.Vector2(1,0), \
		           math3d.Vector2(0,-1), math3d.Vector2(-1,0))
		indicies = (1,0,1,0)
	elif r.origin.dim == 3:
		normals = (math3d.VectorN((0,0,1)), math3d.VectorN((0,0,-1)), \
		           math3d.VectorN((0,1,0)), math3d.VectorN((0,-1,0)), \
		           math3d.VectorN((1,0,0)), math3d.VectorN((-1,0,0)))
		indicies = (2,2,1,1,0,0)

	collisions = []
	tlist = []
	nlist = []
	for i in range(len(normals)):
		# Calculate the d-value for this side of the box.
		if normals[i][indicies[i]] < 0:
			d = math3d.dot(normals[i], b.minPt)
		else:
			d = math3d.dot(normals[i], b.maxPt)
		# Determine if the ray hits the (infinite) plane which this side
		# of the box lies upon.
		plane_intersect = ray_plane(r, Plane(normals[i], d, None))
		if plane_intersect != None:
			Q = plane_intersect["collisions"][0]
			T = plane_intersect["tlist"][0]
			# Now determine if the collision point is actually within the box.
			# Note for nD space, we need to check (n-1) values of the min/max (not
			# including the direction of this normal).
			in_box = True
			for j in range(r.origin.dim):
				if j != indicies[i] and (Q[j] < b.minPt[j] or Q[j] > b.maxPt[j]):
					in_box = False
					break
			if in_box:
				collisions.append(Q)
				tlist.append(T)
				nlist.append(normals[i])
	if len(collisions) == 0:
		return None
	else:
		return {"collisions": collisions, "tlist": tlist, "nlist": nlist}




def spheroid_plane(s, p):
	""" Returns None if the spheroid (s) and plane (p) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	if s.pos.dim == 2 and p.normal.dim == 2:
		dist = p.d - math3d.dot(s.pos, p.normal)
		if abs(dist) < s.radius:
			nperp = math3d.Vector2(-p.normal[1], p.normal[0])
			q = (s.radius ** 2 - dist**2)**0.5
			p1 = s.pos + p.normal * dist + nperp * q
			p2 = p1 - 2 * q * nperp
			return {"collisions": (p1, p2)}
	else:
		# Note: In 3d, if there's more than one point, the intersection defines
		# a circle -- how should we make the user indicate *which* of these
		# points they want??
		raise NotImplementedError("Sorry -- I only have this working in 2d")
	return None

def ray_tri(r, t):
	""" Returns None if the ray (r) and triangle (t) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	# Make sure the ray is a 3d ray
	#if r.origin.dim != 3:
		# If we're in 2D, construct a 3D ray and use a 0 z-value.
	#	newRay = Ray(math3d.VectorN((r.origin[0],r.origin[1],0)), math3d.VectorN((r.direction[0],r.direction[1],0)))
	#else:
#		newRay = r
	# First, see if the ray hits the plane defined by the triangle.
	plane_test = ray_plane(r, Plane(t.normal, t.d))
	if plane_test != None:
		# It does hit the plane.  Now use the barycentric test to determine
		# if this hit point is actually inside the triangle.
		Q = plane_test["collisions"][0]
		T = plane_test["tlist"][0]
		if t.pts[0].dim == 3:
			bcoords = math3d.barycentric(Q, t.pts[0], t.pts[1], t.pts[2])
			if bcoords[0] + bcoords[1] + bcoords[2] <= 1.000001:
				return plane_test
		if t.pts[0].dim == 2:
			if (min(t.pts[0][0], t.pts[1][0])  <= Q[0] <= max(t.pts[0][0], t.pts[1][0]) and \
				min(t.pts[0][1], t.pts[1][1])  <= Q[1] <= max(t.pts[0][1], t.pts[1][1])):
				return plane_test
	return None

def aabb_aabb(b1, b2, firstCall = True):
	""" Returns None if the two aabb's (b1 and b2) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	# See if any of b2's points collide with b1
	collisions = []
	pts = b2.getPts()
	if b1.minPt.dim == 2:
		for p in pts:
			if b1.minPt[0] <= p[0] <= b1.maxPt[0] and b1.minPt[1] <= p[1] <= b1.maxPt[1]:
				collisions.append(p)
	elif b1.minPt.dim == 3:
		for p in pts:
			if b1.minPt[0] <= p[0] <= b1.maxPt[0] and b1.minPt[1] <= p[1] <= b1.maxPt[1] and \
			   b1.minPt[2] <= p[2] <= b1.maxPt[2]:
				collisions.append(p)
	else:
		raise NotImplementedError("Sorry, we don't have support for hyperboxes -- yet:-)")

	if firstCall:
		otherCollisions = aabb_aabb(b2, b1, False)
		collisions += otherCollisions
		if len(collisions) > 0:
			return {"collisions": collisions}
		else:
			return None
	else:
		return collisions

def aabb_spheroid(b, s):
	""" Returns None if the aabb (b) and spheroid (s) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	if b.minPt.dim != s.pos.dim:
		raise ValueError("The box and spheroid must exist in the same dimension!")
	collisions = []
	if b.minPt.dim == 2:
		if b.minPt[0] <= s.pos[0] <= b.maxPt[0]:
			if b.minPt[1] <= s.pos[1] <= b.maxPt[1]:
				# All in
				collisions.append(s.pos)
			elif s.pos[1] < b.minPt[1] and s.pos[1] + s.radius >= b.minPt[1]:
				collisions.append(math3d.Vector2(s.pos[0], b.minPt[1]))
			elif s.pos[1] > b.maxPt[1] and s.pos[1] - s.radius <= b.maxPt[1]:
				collisions.append(math3d.Vector2(s.pos[0], b.maxPt[1]))
	#elif b.minPt.dim == 3:
	#	pass
	else:
		raise NotImplementedError("Sorry.  No support for hyper-volumes yet!")

	if len(collisions) > 0:
		return {"collisions": collisions}
	else:
		return None


def aabb_plane(b, p):
	""" Returns None if the aabb (b) and plane (p) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	if b.minPt.dim == 2 or b.minPt.dim == 3:
		if b.minPt.dim == 2:
			pts = (b.minPt, b.maxPt, math3d.Vector2(b.minPt[0],b.maxPt[1]), math3d.Vector2(b.maxPt[0],b.minPt[1]))
		else:
			pts = (b.minPt, b.maxPt, math3d.VectorN((b.minPt[0],b.minPt[1],b.maxPt[2])), math3d.VectorN((b.minPt[0],b.maxPt[1],b.minPt[2])), \
			       math3d.VectorN((b.maxPt[0],b.minPt[1],b.minPt[2])), math3d.VectorN((b.minPt[0],b.maxPt[1],b.maxPt[2])), \
			       math3d.VectorN((b.maxPt[0],b.minPt[1],b.maxPt[2])), math3d.VectorN((b.maxPt[0],b.maxPt[1],b.minPt[2])))
		collisions = []
		for pt in pts:
			if math3d.dot(pt, p.normal) < p.d:
				collisions.append(pt)
		if len(collisions) > 0:
			return {"collisions": collisions}
	else:
		raise NotImplementedError("Sorry, no support for hyper-boxes (and/or hyper-planes")
	return None


def plane_tri(p, t):
	""" Returns None if the plane (p) and triangle (t) don't intersect.
		If they do, return a dictionary with the following keys:
			'collisions': a list of collision points. """
	collisions = []
	for q in t.pts:
		if math3d.dot(q, p.normal) <= p.d:
			collisions.append(q.copy())
	if len(collisions) == 0:
		return None
	else:
		return {"collisions": collisions}



