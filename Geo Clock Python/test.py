# Import modules
import pygame as pg
from math import radians
from math import pi
from math import cos
from math import sin

# Initialize pygame
pg.init()

# Setup startscreen + resolution
reso = (1280, 800)
screen = pg.display.set_mode(reso)

# Game = running
running = True

# Identify objects
vliegtuig1 = pg.image.load('clock.png')                    # Load aircraft image from folders
vliegtuig1rect = vliegtuig1.get_rect()                          # Rectangle airplane (=vliegtuig1)

# initialze clock
t0 = 0.001*pg.time.get_ticks()
maxdt = 0.5                                                     # Step value

# Start position of airplane (=vliegtuig1)
x1s = 350
y1s = 400

# Start values
V = 0                                                         # Speed of airplane
thetaS = 0                                                      # Rotation of airplane at beginning (There is none = 0)
theta = 0                                                       # Initializing theta for later use because otherwise it would be initialized in a loop --> error

# Initialize loop
while running:
    
    # Clock
    t = 0.001*pg.time.get_ticks()                              
    dt = min(t-t0, maxdt)
    if dt > 0.:
        t0 = t

    screen.fill((0, 0, 0))                                      # Background color: currently black

    pg.event.pump()
    keys = pg.key.get_pressed()

    # Controls of airplane
    if keys[pg.K_LEFT]:                                         # If left key is pressed:
        theta = thetaS - 2.5*dt                                 # Turns the aircraft to the left

    if keys[pg.K_RIGHT]:                                        # If right key is pressed:
        theta = thetaS + 2.5*dt                                 # Turns the aircraft to the right
 
    # Airplane dynamics
    x1 = x1s + V*dt*cos(theta)                                  # x-coordinate = is starting x-coordanate + speed * small change in time * cos(theta)
    y1 = y1s + V*dt*sin(theta)                                  # Same as above

    x1s = x1                                                    # Calculated x-coordinate becomes new starting x-coordinate for next calculation in loop                                                   
    y1s = y1                                                    # Same as above
    thetaS = theta                                              # Same as above for angles

    rotate = pg.transform.rotate(vliegtuig1,theta*(-180/pi))    # Rotation of the plane (NOT AROUND CENTER)
    
    

    # Show aircraft on screen
    vliegtuig1rect.centerx = x1                                 # Show aircraft on x-coordinaate
    vliegtuig1rect.centery = y1                                 # Same as above
    screen.blit(rotate, vliegtuig1rect)                     # Refresh frames

    # Escape key to quit
    if keys[pg.K_ESCAPE]:
        running = False
    pg.display.flip()

# Quit pygame
pg.quit()