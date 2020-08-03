import math
import random

class Vec3:
	X=0.0
	Y=0.0
	Z=0.0

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.X=x
		self.Y=y
		self.Z=z

	def __add__(self, other):
		return Vec3(self.X+other.X, self.Y+other.Y, self.Z+other.Z)

	def __sub__(self, other):
		return Vec3(self.X-other.X, self.Y-other.Y, self.Z-other.Z)

	def __mul__(self, other):
		return Vec3(self.X*other.X, self.Y*other.Y, self.Z*other.Z)

	def Mul(self, value):
		return Vec3(self.X*value, self.Y*value, self.Z*value)

	def __div__(self, other):
		return Vec3(self.X/other.X, self.Y/other.Y, self.Z/other.Z)

	def Dot(value0, value1):
		return value0.X*value1.X + value0.Y*value1.Y + value0.Z*value1.Z

	def Cross(self, other):
		return Vec3(self.Y*other.Z-self.Z*other.Y, self.Z*other.X-self.X*other.Z, self.X*other.Y-self.Y*other.X)

	def Length(self):
		return math.sqrt(self.X*self.X + self.Y*self.Y + self.Z*self.Z)

	def Copy(self, other):
		self.X = other.X
		self.Y = other.Y
		self.Z = other.Z

	def SquaredLength(self):
		return self.X*self.X + self.Y*self.Y + self.Z*self.Z

	def Lerp(self,other, t):
		return self.Mul(1.0-t) + other.Mul(t)

	def PrintDesc(self):
		print("X:",self.X,"Y:",self.Y,"Z:",self.Z)


##################################################################################

def UnitVector(myVector):
	result = Vec3()
	length = myVector.Length()
	if length > 0.0 :
		result = myVector.Mul(1.0/length)
	return result

##################################################################################

class Ray : 
	Origin = None
	Direction = None

	def __init__(self, origin=Vec3(), direction=Vec3()):
		self.Origin = origin
		self.Direction = direction

	def PointAtParameter(self,t):
		return self.Origin + self.Direction.Mul(t)

	def Copy(self,other):
		self.Origin.Copy(other.Origin)
		self.Direction.Copy(other.Direction)

##################################################################################

def Reflect(v, n):
	return v - n.Mul(2.0*v.Dot(n))

def Refract(v, n, ni_over_nt, refracted) :
	uv = UnitVector(v)
	dt = uv.Dot(n)
	discriminant = 1.0-ni_over_nt*ni_over_nt*(1.0-dt*dt)
	if discriminant>0.0 :
		refracted.Copy((uv-n.Mul(dt)).Mul(ni_over_nt) - n.Mul(math.sqrt(discriminant)))
		return True
	else :
		return False

def Schlick(cosine, refidx):
	r0 = (1.0-refidx)/(1.0+refidx)
	r0 = r0*r0
	return r0+(1.0-r0)*math.pow(1.0-cosine,5.0)
##################################################################################
#Rejection method
def RandomInUnitSphere():
	point = Vec3(random.random(), random.random(), random.random()).Mul(2.0) - Vec3(1.0,1.0,1.0)
	while point.SquaredLength() >= 1.0 :
		point = Vec3(random.random(), random.random(), random.random()).Mul(2.0) - Vec3(1.0,1.0,1.0)
	return point

def RandomInUnitDisk():
	point = Vec3(random.random(), random.random(), 0.0).Mul(2.0) - Vec3(1.0,1.0,0.0)
	while point.SquaredLength() >= 1.0 :
		point = Vec3(random.random(), random.random(), 0.0).Mul(2.0) - Vec3(1.0,1.0,0.0)
	return point

##################################################################################
class Camera:
	Origin = None
	LowerLeftCorner = None
	Horizontal = None
	Vertical = None
	LensRadius = 0.0
	U,V,W = None, None, None

	def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
		self.LensRadius = aperture * 0.5
		theta = vfov * math.pi / 180.0
		half_height = math.tan(theta * 0.5)
		half_width = aspect * half_height
		self.Origin = lookfrom		
		self.W = UnitVector(lookfrom - lookat)
		self.U = UnitVector(vup.Cross(self.W))
		self.V= self.W.Cross(self.U)
		self.LowerLeftCorner = self.Origin + (self.U.Mul(-half_width) - self.V.Mul(half_height) -self.W).Mul(focus_dist)
		self.Horizontal = self.U.Mul(2.0*half_width*focus_dist)
		self.Vertical = self.V.Mul(2.0*half_height*focus_dist)

	def GetRay(self, s,t):
		rd = RandomInUnitDisk().Mul(self.LensRadius)
		offset = self.U.Mul(rd.X) + self.V.Mul(rd.Y)
		return Ray(self.Origin + offset, self.LowerLeftCorner + self.Horizontal.Mul(s) + self.Vertical.Mul(t) - self.Origin - offset)

##################################################################################

class HitRecord:
	ParamT = 0
	Point = Vec3()
	Normal = Vec3()
	Material = None

##################################################################################
#Material
class Material:

	def __init__(self,albedo):
		pass

	def Scatter(self, ray, hitRecord, attenuation, scatteredRay):
		pass

	def Display(self) :
		pass
	
##################################################################################

class Lambertian(Material):
	Albedo = None

	def __init__(self, albedo) :
		self.Albedo = albedo

	def Scatter(self, ray, hitRecord, attenuation, scatteredRay):
		scatteredRay.Origin.Copy(hitRecord.Point)
		scatteredRay.Direction.Copy(hitRecord.Normal + RandomInUnitSphere())
		attenuation.Copy(self.Albedo)
		return True

##################################################################################	

class Metal(Material):
	Albedo = None
	Fuzziness = 0.0

	def __init__(self, albedo, fuzz) :
		self.Albedo = albedo
		self.Fuzziness = fuzz

	def Scatter(self, ray, hitRecord, attenuation, scatteredRay):
		reflected = Reflect(UnitVector(ray.Direction), hitRecord.Normal)
		scatteredRay.Origin.Copy(hitRecord.Point)
		scatteredRay.Direction.Copy(reflected + RandomInUnitSphere().Mul(self.Fuzziness))
		attenuation.Copy(self.Albedo)
		return (scatteredRay.Direction.Dot(hitRecord.Normal)>0)
	
##################################################################################

class Dielectric(Material):
	Ref_idx = 0.0

	def __init__(self,ref_idx) :
		self.Ref_idx = ref_idx

	def Scatter(self, ray, hitRecord, attenuation, scatteredRay):
		outward_normal = Vec3()		
		ni_over_nt = 0.0
		attenuation.Copy(Vec3(1.0,1.0,1.0))
		refracted = Vec3()
		reflect_prob = 0.0
		cosine = 0.0
		unitDirection = UnitVector(ray.Direction)
		if ray.Direction.Dot(hitRecord.Normal) > 0.0 :
			outward_normal.Copy(hitRecord.Normal.Mul(-1.0))
			ni_over_nt = self.Ref_idx
			cosine = self.Ref_idx * hitRecord.Normal.Dot(unitDirection)
		else:
			outward_normal.Copy(hitRecord.Normal)
			ni_over_nt = 1.0/self.Ref_idx
			cosine = -hitRecord.Normal.Dot(unitDirection)

		reflected = Reflect(ray.Direction, hitRecord.Normal)
		if Refract(ray.Direction, outward_normal, ni_over_nt, refracted):
			reflect_prob = Schlick(cosine, self.Ref_idx)
		else :
			reflect_prob = 1.0

		scatteredRay.Origin.Copy(hitRecord.Point)
		if random.random()<reflect_prob:
			scatteredRay.Direction.Copy(reflected)
		else:
			scatteredRay.Direction.Copy(refracted)
		return True


##################################################################################

class Sphere:
	Center = None
	radius = None
	Material = None

	def __init__(self, center, radius, material):
		self.Center = center
		self.Radius = radius
		self.Material = material

	def Hit(self, ray, tMin, tMax, hitRecord):
		centerToOrigin = ray.Origin - self.Center
		a = Vec3.Dot(ray.Direction, ray.Direction)
		b = Vec3.Dot(centerToOrigin, ray.Direction) #there should be a *2.f here but simplifies the equation later
		c = Vec3.Dot(centerToOrigin, centerToOrigin) - self.Radius*self.Radius
		discriminant = b*b-a*c
		if discriminant > 0.0:
			tmp = (-b - math.sqrt(discriminant) ) / a
			if tMin<=tmp and tmp<=tMax :
				hitRecord.ParamT = tmp
				hitRecord.Point.Copy(ray.PointAtParameter(tmp))
				hitRecord.Normal.Copy((hitRecord.Point - self.Center).Mul(1.0/self.Radius))
				hitRecord.Material = self.Material
				return True
			
			tmp = (-b + math.sqrt(discriminant) ) / a
			if tMin<=tmp and tmp<=tMax : #maybe some code to put in common here
				hitRecord.ParamT = tmp
				hitRecord.Point.Copy(ray.PointAtParameter(tmp))
				hitRecord.Normal.Copy((hitRecord.Point - self.Center).Mul(1.0/self.Radius))
				hitRecord.Material = self.Material
				return True
		return False
##################################################################################


class HitableList:
	Elems = []
	def Hit(self, ray, tMin, tMax, hitRecord):
		hitSomething = False
		closestSoFar = tMax
		for curElem in self.Elems:
			if curElem.Hit(ray, tMin, closestSoFar, hitRecord):
				hitSomething = True
				closestSoFar = hitRecord.ParamT
		return hitSomething
	
##################################################################################

def RandomScene(Scene):	
	Scene.Elems.append(Sphere(Vec3(0.0,-1000.0,0.0), 1000.0, Lambertian(Vec3(0.5,0.5,0.5))))#ground sphere
	for a in range(-11,11) :
		for b in range(-11,11) :
			chooseMat = random.random()
			center = Vec3(float(a)+0.9*random.random(), 0.2, float(b)+0.9*random.random())
			if (center-Vec3(4.0,0.2,0.0)).Length() >= 0.9:
				if (chooseMat<=0.95):
					Scene.Elems.append(Sphere(center, 0.2, Lambertian(Vec3(random.random()*random.random(),random.random()*random.random(),random.random()*random.random()))))
				else:
					Scene.Elems.append(Sphere(center, 0.2, Metal(Vec3(0.5*(1.0+random.random()), 0.5*(1.0+random.random()), 0.5*(1.0+random.random())), 0.5*random.random())))
			else:
				Scene.Elems.append(Sphere(center, 0.2, Dielectric(1.5)))

	Scene.Elems.append(Sphere(Vec3(0.0,1.0,0.0), 1.0, Dielectric(1.5)))
	Scene.Elems.append(Sphere(Vec3(-4.0,1.0,0.0), 1.0, Lambertian(Vec3(0.4,0.2,0.1))))
	Scene.Elems.append(Sphere(Vec3(4.0,1.0,0.0), 1.0, Metal(Vec3(0.7,0.6,0.5), 0.0)))