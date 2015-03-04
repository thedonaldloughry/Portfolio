import pygame
import raytracer
import math3d
import physics

pygame.display.init()
win_width = 200
win_height = 150
screen = pygame.display.set_mode((win_width, win_height))
# The raytracer will modify pixel in renderSurface
renderSurface = pygame.Surface((win_width, win_height))

# Define the raytracer
RT = raytracer.RayTracer(renderSurface)

# Define our viewpoint on the scene
camPos = math3d.VectorN((-50,30,90))
camInterest = math3d.VectorN((0,0,0))  # Pos. camera is looking at
worldUp = math3d.VectorN((0,1,0))
fov = 60.0         # The angle made by the top and bottom of the
                   #  virtual view plane and the camera
RT.setCamera(camPos, camInterest, worldUp, fov)

# Define the virtual scene
redMaterial = {"ambient" : math3d.VectorN((0.3,0,0)), \
               "diffuse" : math3d.VectorN((1,0,0)), \
			   "specular" : math3d.VectorN((1,1,1)), \
			   "glossy" : 30.0}
greenMaterial = {"ambient" : math3d.VectorN((0,0.3,0)),
                 "diffuse" : math3d.VectorN((0,1,0)), \
			     "specular" : math3d.VectorN((1,1,1)), \
				 "glossy" : 10.0}
blueMaterial = {"ambient" : math3d.VectorN((0,0,0.3)), \
                "diffuse" : math3d.VectorN((0,0,1)), \
			    "specular" : math3d.VectorN((1,1,1)), \
				"glossy" : 5.0}
RT.addObject(physics.Plane(worldUp, 0.0, blueMaterial))
RT.addObject(physics.Spheroid(math3d.VectorN((0, 20.0, 0)), 20.0, redMaterial))
RT.addObject(physics.AABB(math3d.VectorN((0, 40.0, 10)), \
             math3d.VectorN((40.0,80.0,50.0)), greenMaterial))

# ... add POINT lights
RT.addLight({"pos" : math3d.VectorN((0,200,0)), \
             "diffuse" : math3d.VectorN((1,1,1)), \
			 "specular" : math3d.VectorN((1,1,1))})
RT.addLight({"pos" : math3d.VectorN((-150,150,-20)), \
             "diffuse" : math3d.VectorN((0.3,0.3,0.3)), \
			 "specular" : math3d.VectorN((1,1,1))})

# The line in renderSurf to start rendering
currentY = 0

while True:
	# Erase
    screen.fill((0,0,0))

	# Get input
    pygame.event.pump()
    event = pygame.event.wait()
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        break
    elif event.type == pygame.QUIT:
        break

	# Update
    if currentY < renderSurface.get_height():
        RT.renderOneLine(currentY)
        currentY += 1

	# Draw
    screen.blit(renderSurface, (0,0))
    pygame.display.flip()

pygame.display.quit()