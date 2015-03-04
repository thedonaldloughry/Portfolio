import math3d
import physics
import math


class RayTracer(object):
	def __init__(self, surf):
		self.surf = surf
		self.objects = []
		self.lights = []
		self.backgroundColor = math3d.VectorN((0.25, 0.25, 0.25))
		self.pixelWidth = surf.get_width()
		self.pixelHeight = surf.get_height()

		# Define the ambient light level in the scene
		self.ambientLight = math3d.VectorN((1,1,1))

		# Step1. Define self.aspectRatio (the ratio of width to height of the
		# pygame window)
		self.aspectRatio = self.pixelWidth / self.pixelHeight
		# Step2. Calculate self.viewScreenWidth, the world unit width of the
		#        virtual view plane.
		self.viewScreenHeight = 1.0   # In world units.  An arbitrary choice...
		self.viewScreenWidth = self.aspectRatio * self.viewScreenHeight
		# Step3. Calculate self.deltaX and self.deltaY, the spacing (in world
		#        units) between columns and rows, respectively on the virtual
		#        view plane.
		self.deltaX = self.viewScreenWidth / (self.pixelWidth - 1)
		self.deltaY = self.viewScreenHeight / (self.pixelHeight - 1)
		# (temporary) Debug code
		print("Values set in __init__")
		print("======================")
		print("pixelWidth: " + str(self.pixelWidth))
		print("pixelHeight: " + str(self.pixelHeight))
		print("aspectRatio: " + str(self.aspectRatio))
		print("viewScreenWidth: " + str(self.viewScreenWidth))
		print("viewScreenHeight: "+ str(self.viewScreenHeight))
		print("deltaX: " + str(self.deltaX))
		print("deltaY: " + str(self.deltaY))

	def addObject(self, o):
		self.objects.append(o)

	def addLight(self, L):
		self.lights.append(L)

	def setCamera(self, pos, interest, up, fov):
		""" (Re-)Define the camera's local coordinate space """
		self.cameraPos = pos.copy()
		# Step1.  Calculate self.cameraX, self.cameraY, self.cameraZ
		#         (which are unit-length vectors in a RHS like the slides)
		self.cameraZ = (pos - interest).normalized()
		self.cameraX = math3d.cross(up, self.cameraZ).normalized()
		self.cameraY = math3d.cross(self.cameraZ, self.cameraX).normalized()
		# Step2.  Calculate self.near, which is the number of world-space
		#         units the view plane is in front of the camera.
		self.near = (self.viewScreenHeight / 2) / math.tan(math.radians(fov / 2))
		# Step4   Calculate the 3d virtual position, self.TL, of the pygame
		#         pixel(0,0)
		self.topLeft = self.cameraPos + (-self.viewScreenWidth / 2) * self.cameraX + \
		           				(self.viewScreenHeight / 2) * self.cameraY + \
								   (-self.near) * self.cameraZ
		# (temporary) Debug code
		print("Values set in setCamera")
		print("=======================")
		print("cameraPos: " + str(self.cameraPos))
		print("cameraCOI: " + str(interest))
		print("cameraX: " + str(self.cameraX))
		print("cameraY: " + str(self.cameraY))
		print("cameraZ: " + str(self.cameraZ))
		print("near: " + str(self.near))
		print("topLeft: " + str(self.topLeft))

	def shadowCheck(self, P, obj, light):
		closestObj = None
		closestT = None
		R = physics.Ray(P, light["pos"] - P)
		for i in self.objects:
			if i != obj:
				result = physics.handle_collision(R, i)
				if result != None:
					minT = min(result["tlist"])
					if closestObj == None or minT < closestT:
						if closestObj != obj:
							closestT = minT
							closestObj = i
		length = (P - light["pos"]).length()
		if closestObj == None:
			return True
		elif (length < closestT):
			return True
		else:
			return False

	def calculateLitColor(self, material, P, N, Object):
		""" material: a material dictionary (see main.py for examples),
			P : the point we're illuminating
			N : the normal vector at P
            Object : the object that P is on """
		cAmb = math3d.tensor(self.ambientLight, material["ambient"]) # Put in for loop??
		cLit = cAmb
		cDiff = math3d.VectorN((0,0,0))
		cSpec = math3d.VectorN((0,0,0))

		for light in self.lights:
			L = light["pos"]
			lightToPoint = (L - P).normalized()

			#### Shadow Check ####################################################
			check = self.shadowCheck(P, Object, light)
			if check == True:
				#### Diffuse #########################################################
				dStr = math3d.dot(lightToPoint, N)
				if dStr > 0:
					cDiff = dStr * math3d.tensor(light["diffuse"], material["diffuse"])
					cLit += cDiff

				#### Specular ########################################################
				R = 2 * math3d.dot(lightToPoint, N) * N - lightToPoint
				V = (self.cameraPos - P).normalized()
				sStr = max(math3d.dot(V, R), 0)
				if sStr > 0: # Hard-coded "shiny" value.
					cSpec = (sStr ** material["glossy"]) * math3d.tensor(light["specular"], material["specular"])
					cLit += cSpec

		return cLit
		# FINISH ME!

	def castRay(self, R):
		""" Casts the Ray R into the world.  If it hits nothing, this
			method return self.backgroundColor.  If it does hit 1-n objects,
			return the color of the CLOSEST. """


		closestObject = None	# The closest object we've seen so far
		closestT = None		 # The smallest t-value we've seen so far
		hitData = None
		for o in self.objects:
			result = physics.handle_collision(R, o)
			# If result is NOT None, adjust closestT and closestObject
			# if either closestObject is None (i.e. this is the first
			# object we've hit so far) OR the t-value from result["tlist"] is
			# less than closestT.
			if result != None:
				minT = min(result["tlist"])
				if closestObject == None or minT < closestT:
					closestT = minT
					closestObject = o
					hitData = result
		# There are two possibilites.  1) closestObject is None (the ray didn't
		# hit anything) -- return self.backgroundColor OR 2) closestObject is
		# not None -- return closestObject.color
		if closestObject == None:
			return self.backgroundColor
		else:
			index = hitData["tlist"].index(closestT)
			P = hitData["collisions"][index]
			N = hitData["nlist"][index]
			return self.calculateLitColor(closestObject.material, P, N, closestObject)



	def renderOneLine(self, y, projectionType="perspective"):
		""" Sets the color values of row y of self.surf.  The allowable
		    values for projectionType are 'perspective' and 'orthogonal' """
		# Step1. Calculate current, which is the 3d counter-part to
		#        the pygame pixel (0,y).
		current = self.topLeft + (-self.deltaY * y) * self.cameraY
		# Step2. Calculate offset, a vector which is the movement necessary
		#        to move one pixel to the right
		offset = self.deltaX * self.cameraX
		for x in range(self.pixelWidth):
			# Step3. Create a ray with origin = current and direction = ???
			#        Make sure you look at projectionType.
			if projectionType == 'perspective':
				myRay = physics.Ray(current, current - self.cameraPos)
			else:
				myRay = physics.Ray(current, -self.cameraZ, None)
			# Step4. Calculate the color of the closest object (if any) hit by
			# 	   that ray.  Note: the color being returned is a VectorN (r, g, b, each in
			#      the range 0.0 - 1.0)
			color = self.castRay(myRay)
			for i in range(int(len(color))):
				if color[i] >= 1.0:
					color[i] = 1.0
			pygameColor = color * 255
			pygameColor = (int(pygameColor[0]), int(pygameColor[1]), int(pygameColor[2]))
			self.surf.set_at((x,y), pygameColor)

			# Step5. Move to the next pixel in the row.
			current += offset
