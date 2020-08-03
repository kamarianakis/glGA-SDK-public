import array
import rt
import sys
import random
import math

def ColorToGammaSpaceToPPM(color, maxValue):
	tmp = rt.Vec3(math.sqrt(color.X),math.sqrt(color.Y), math.sqrt(color.Z))
	return tmp.Mul(maxValue)

#High quality Option
MAX_RECURSION_ALLOWED = 50 #TODO port that code into something iterative rather than recursive that's poorly performing
nsample = 100  #for aliasing# PPM header

#Comment for high quality
#nsample =  10 #for aliasing# PPM header

nx = 200 #image resolution
ny = 100 #image resolution

nx = 400 #image resolution
ny = 200 #image resolution

EPSILON = 0.001

ITERATIVE = False
ITERATIVE = True

BLUR = False
BLUR = True

def ColorIterative(ray, world):
	tmp = rt.HitRecord()
	color = rt.Vec3(1.0,1.0,1.0)
	curRay = rt.Ray()	
	curRay.Copy(ray)
	curScattered = rt.Ray()
	curAttenuation = rt.Vec3()
	
	for i in range(0,MAX_RECURSION_ALLOWED) :			
		if world.Hit(curRay, EPSILON, sys.float_info.max, tmp) :									
			if tmp.Material.Scatter(curRay, tmp, curAttenuation, curScattered):
				curRay.Copy(curScattered)
				color.Copy(color * curAttenuation)
			else :
				color.X = 0.0
				color.Y = 0.0
				color.Z = 0.0
				break
		else: #background
			unitDirection = rt.UnitVector(curRay.Direction)
			t = 0.5 * (unitDirection.Y + 1.0)
			color.Copy(color * rt.Vec3(1.0,1.0,1.0).Lerp(rt.Vec3(0.5,0.7,1.0),t))
			break

	if i==MAX_RECURSION_ALLOWED :
		color.X = 0.0
		color.Y = 0.0
		color.Z = 0.0

	return color
		

def ColorRecursive(ray, world, recursionLevel):
	tmp = rt.HitRecord()
	if world.Hit(ray, EPSILON, sys.float_info.max, tmp) :
		scattered = rt.Ray()
		attenuation = rt.Vec3()
		if  recursionLevel < MAX_RECURSION_ALLOWED and tmp.Material.Scatter(ray, tmp, attenuation, scattered):
			recursionLevel += 1
			return attenuation * ColorRecursive(scattered, world, recursionLevel)
		else :
			return rt.Vec3()
	else: #background
		unitDirection = rt.UnitVector(ray.Direction)
		t = 0.5 * (unitDirection.Y + 1.0)
		return rt.Vec3(1.0,1.0,1.0).Lerp(rt.Vec3(0.5,0.7,1.0),t)

maxval = 255
ppm_header = f"P6 {nx} {ny} {maxval}\n"

# PPM image data
image = array.array('B', [0, 0, 0] * nx * ny)

scene = rt.HitableList()
rt.RandomScene(scene)

lookFrom = rt.Vec3(14.0,2.0,4.0)
lookAt = rt.Vec3(0.0,0.0,-1.0)
distToFocus = (lookFrom-lookAt).Length()
aperture = 0.0
if BLUR :
	aperture = 0.5

mainCamera = rt.Camera(lookFrom, lookAt, rt.Vec3(0.0,1.0,0.0), 20, float(nx)/float(ny), aperture, distToFocus)
curPurcentComplete = 0

scale = 255.9
for i in range(0, nx):
	for j in range(0, ny):
		color = rt.Vec3()
		for k in range(0, nsample):
			u = ( float(i) + random.random() ) / float(nx)
			v = ( float(j) + random.random() ) / float(ny)
			ray = mainCamera.GetRay(u,v)
			if ITERATIVE :				
				color += ColorIterative(ray,scene)				
			else :			
				color += ColorRecursive(ray,scene, 0)
				
		color = color.Mul(1.0/float(nsample))
		color = ColorToGammaSpaceToPPM(color, scale)
		index = 3 * ((ny-1-j) * nx + i) #matching what is in the book		
		image[index] = int(color.X)
		image[index + 1] = int(color.Y)
		image[index + 2] = int(color.Z)

		print("Cur Pixel, ", i+1, ", ", j+1, "complete ")

print("Saving Image")
# Save the PPM image as a binary file
with open('raytracing.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)