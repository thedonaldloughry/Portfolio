# A Collection of classes and (eventually) functions.  The main use of this module
# will be in graphics (2D and 3D) applications
import math
import numbers       # to look for instances of the numbers.Number type

#################################################
# VECTORN class                                 #
#################################################
class VectorN(object):
	""" A General-purpose n-dimensional vector class. """
	def __init__(self, param):
		""" param can be a
		    a) positive non-zero integer (in which case, this
			becomes a vector of that size (all 0's).  Or
			b) it can be a sequence-like list of values.  The size of the
			vector is deduced from the length of that sequence """
		if isinstance(param, int) and param > 0:
			self.dim = param
			self.data = [0.0] * param
		elif hasattr(param, "__len__") and hasattr(param, "__getitem__"):
			self.dim = len(param)
			self.data = []
			for val in param:
				# Note: This *could* fail (if say, there is a "ABC" element in
				# the sequence).  In this case, though, I'll let python handle it...
				self.data.append(float(val))
		else:
			raise ValueError("param must be a positive non-zero int (dimension) \
				or a sequence-like object with initial values")

	def __str__(self):
		""" Returns a printable version of this object """
		s = "<Vector" + str(self.dim) + ": "
		for i in range(len(self.data)-1):
			s += str(self.data[i]) + ", "
		s += str(self.data[-1]) + ">"
		return s

	def __len__(self):
		""" Returns the number of elements in this 'sequence' (i.e. self.data)"""
		return self.dim

	def __getitem__(self, index):
		""" Returns the index'th element of this 'sequence' """
		if not isinstance(index, int) or index < 0 or index >= self.dim:
			raise IndexError("Invalid Index#: " + str(index))
		return self.data[index]

	def __setitem__(self, index, newVal):
		""" Sets the index'th element of this 'sequence' to newVal """
		if not isinstance(index, int) or index < 0 or index >= self.dim:
			raise IndexError("Invalid Index#: " + str(index))
		self.data[index] = float(newVal)

	def copy(self):
		""" Returns a new copy of this vector """
		cp = VectorN(self)
		# The following line is necessary to make the types match for derived
		# classes (e.g. Vector2)
		cp.__class__ = self.__class__
		return cp

	def __neg__(self):
		""" Returns the vector negation of this vector """
		rval = self.copy()
		for i in range(self.dim):
			rval[i] = -rval[i]
		return rval

	def length(self):
		""" Returns the vector length (magnitude) of this vector """
		mag = 0.0
		for i in range(self.dim):
			mag += self.data[i] ** 2
		return mag ** 0.5

	def __mul__(self, scalar):
		""" Returns the product of this vectorN and the given scalar """
		if not isinstance(scalar, numbers.Number):
			raise TypeError("This VectorN can only be multiplied by a scalar.")
		rval = VectorN(self.dim)
		for i in range(self.dim):
			rval[i] = self.data[i] * scalar
		return rval

	def __rmul__(self, scalar):
		""" Returns the product of the given scalar and this VectorN """
		# Since vector-scalar multiplication is commutative, we can just call __mul__
		return self.__mul__(scalar)

	def __truediv__(self, scalar):
		""" Returns the result of dividing this vector by the given scalar """
		if not isinstance(scalar, numbers.Number):
			raise TypeError("This VectorN can only be multiplied by a scalar.")
		rval = VectorN(self.dim)
		for i in range(self.dim):
			rval[i] = self.data[i] / scalar
		return rval

	def __add__(self, otherVect):
		""" Returns the vector sum of this vector and otherVect (which must be
			of the same size """
		if not isinstance(otherVect, VectorN) or otherVect.dim != self.dim:
			raise TypeError("You can only add an equally-sized vectorN to this vectorN")
		rval = VectorN(self.dim)
		for i in range(self.dim):
			rval[i] = self.data[i] + otherVect[i]
		return rval

	def __sub__(self, otherVect):
		""" Returns the result of subtracting otherVect (which must be the same
			size as this VectorN) from this vector. """
		return self + (-otherVect)

	def normalized(self):
		""" Returns a normalized copy of this vector (but does not change this
			vector """
		mag = self.length()
		if mag == 0:
			raise ZeroDivisionError("You can't normalize a zero-vector")
		rval = VectorN(self.dim)
		for i in range(self.dim):
			rval[i] = self.data[i] / mag
		return rval


#################################################
# VECTORN-related functions                     #
#################################################
def dot(v, w):
	""" Returns the dot product of two equally-sized VectorN's """
	if not isinstance(v, VectorN) or not isinstance(w, VectorN) or v.dim != w.dim:
		raise TypeError("You can only take the dot product of two equally-sized VectorN's")
	dp = 0.0
	for i in range(v.dim):
		dp += v[i] * w[i]
	return dp

def cross(v, w):
	""" Returns the cross product of two equally-sized Vector3's """
	if not isinstance(v, VectorN) or not isinstance(w, VectorN) or v.dim != 3 or w.dim != 3:
		raise TypeError("You can only take the cross product of two Vector3's")
	cp = VectorN(3)
	cp[0] = v[1] * w[2] - v[2] * w[1]
	cp[1] = v[2] * w[0] - v[0] * w[2]
	cp[2] = v[0] * w[1] - v[1] * w[0]
	return cp

def tensor(v, w):
	""" Returns the 'tensor' (I'm using this term loosely) product of two 
	    equally-sized VectorN's """
	if not isinstance(v, VectorN) or not isinstance(w, VectorN) or v.dim != w.dim:
		raise TypeError("You can only take the 'tensor' product of two equally-sized VectorN's")
	tp = VectorN(v.dim)
	for i in range(v.dim):
		tp[i] = v[i] * w[i]
	return tp


#################################################
# VECTOR2 class                                 #
#################################################
class Vector2(VectorN):
	""" A specialized variant of VectorN that always has two values (useful
	    for 2D applications """
	def __init__(self, x=0, y=0):
		""" Creates two values in the Vector """
		VectorN.__init__(self, (x, y))

	@property
	def x(self):
		""" Returns the x-value (the first element in the list of numbers) """
		return self.data[0]

	@x.setter
	def x(self, newVal):
		""" Sets the first element of the list to newVal """
		self[0] = float(newVal)     # Calls VectorN.__setitem___

	@property
	def y(self):
		""" Returns the y-value (the second element in the list of numbers) """
		return self.data[1]

	@y.setter
	def y(self, newVal):
		""" Sets the second element of the list to newVal """
		self[1] = float(newVal)     # Calls VectorN.__setitem___



##############################################
# MISCELLANEOUS functions                    #
##############################################
def area(p1, p2, p3):
	""" Returns the area of a triangle """
	v = p2 - p1
	w = p3 - p1
	return cross(v, w).length() / 2

def barycentric(Q, p1, p2, p3):
	""" Returns the barycentric coordinates of Q relative to the triangle p1, p2, p3 """
	A = area(p1, p2, p3)
	A1 = area(Q, p2, p3)
	A2 = area(Q, p1, p3)
	A3 = area(Q, p1, p2)
	return VectorN((A1 / A, A2 / A, A3 / A))


# Test code (temporary)
if __name__ == "__main__":
	pass