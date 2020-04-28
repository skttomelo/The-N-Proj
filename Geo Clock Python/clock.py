import pygame
from sys import exit
import json
import math
import random
import sqlite3

# we initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Geo Clock")
pygame.display.set_icon(pygame.image.load('./Assets/clockface.ico'))


# load assets
clockface = pygame.image.load('./Assets/clockface.png')
hand = pygame.image.load('./Assets/clockhand.png').convert_alpha() # by using the convert_alpha functions we are able to include the alpha channels for transparency in the image
hand_offset = (25, 8) # offset is relative to the clock hand
with open('./Assets/locations.json', 'r') as f:
    locations = json.load(f)
clock_excess_width = 110
clock_actual_width = 800-220
clock_actual_height = 600-20
text_zone = (clock_actual_width/8, clock_actual_height/8)

# font asset setup
SPRITE = pygame.sprite.Sprite()
SPRITE.image = hand
SPRITE.rect = hand.get_rect()
font = pygame.font.SysFont('Sans', 16)
font1 = pygame.font.SysFont('Sans', 20)

white = (255,255,255)
black = (0,0,0)

class Person:
    def __init__(self, name, latitude, longitude, hand, img, color):
        self.name = name
        self.lat = latitude
        self.long = longitude
        self.location = ""
        self.size = (246,16)
        self.loc = (400,300)
        self.color = color
        self.angle = 0
        self.select = False
        self.rendered_name = font.render(self.name, True, white, black)
        self.clock_hand = hand.copy()
        self.img = img.copy()
        if self.img.get_width() != 1:
            self.img = pygame.transform.scale(self.img, (self.rendered_name.get_width(), self.rendered_name.get_width()))
        self.fill(self.clock_hand, color)
    def set_angle(self, ang):
        self.angle = ang
    def fill(self, surface, color):
    # Fill all pixels of the surface with color, preserve transparency.
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))
    def draw_text(self):
        if screen.get_at(pygame.mouse.get_pos()) == self.color:
            screen.blit(self.rendered_name, (pygame.mouse.get_pos()[0]-self.rendered_name.get_width(),pygame.mouse.get_pos()[1]))
            if self.img.get_width() != 1:
                screen.blit(self.img, (pygame.mouse.get_pos()[0]-self.rendered_name.get_width(),pygame.mouse.get_pos()[1]+self.rendered_name.get_height()))
    def draw(self):
        rotated_image = pygame.transform.rotate(self.clock_hand, self.angle)

        center = rotated_image.get_rect().center
        offset = (self.loc[0]-center[0], self.loc[1]-center[1])
        screen.blit(rotated_image, offset)
        
people = {}
used_colors = []
used_colors.append(pygame.Color(0,0,0))
used_colors.append(pygame.Color(192,192,192))
used_colors.append(pygame.Color(255,255,255))

def create_rand_color():
    c = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    while c in used_colors:
        c = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return c

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def database_check():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f'select * from NMPOOL2485Location;')

    rows = c.fetchall()
    conn.close()
    for row in rows:
        if row[0] not in people: 
            try:
                profile_pic = pygame.image.load(f'./Assets/PFP/{row[0]}.jpg')
            except:
                profile_pic = pygame.image.load('./Assets/DNE.png')
            people[row[0]] = Person(row[0], float(row[1]), float(row[2]), hand, profile_pic, create_rand_color())
            continue
        people[row[0]].lat = float(row[1])
        people[row[0]].long = float(row[2])
    pass

# code in this function is based on https://www.geodatasource.com/developers/java
# we only care about miles for the scope of this project
def distance(lat1,lon1,lat2,lon2):
    if (lat1 == lat2) and (lon1 == lon2):
        return 0
    theta = lon1 - lon2
    dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
    dist = math.acos(dist)
    dist = math.degrees(dist)
    dist = dist * 60 * 1.1515
    return dist

def geo_fence_check():
    for person in people:
        angle_set = False
        for (i, location) in enumerate(locations['places']): # we enumerate the locations so we can take the current location and pick a rng val between it and the last 45 degs
            if location['name'] != "Traveling":
                # print(f"{distance(people[person].lat, people[person].long, location['latitude'], location['longitude'])} {location['geo_fence']}")
                if distance(people[person].lat, people[person].long, location['latitude'], location['longitude']) <= location['geo_fence']:
                    if people[person].location != location['name']:
                        people[person].set_angle(random.randint((i*45)+16, ((i+1)*45)-16))
                        people[person].location = location['name']
                    angle_set = True
                    break
        if angle_set == False and people[person].location != "Traveling":
            minimum = ((len(locations['places'])-1)*45)+16
            maximum = (len(locations['places'])*45)-16
            people[person].set_angle(random.randint(minimum,maximum))
            people[person].location = "Traveling"

def draw_text():
    for (i, location) in enumerate(locations['places']):
        text = font1.render(location['name'], True, black)
        # text = pygame.transform.rotate(text, (i*45)+45)
        text_location = (800-clock_excess_width, 600-10)
        if i == 0:
            text = pygame.transform.rotozoom(text, -60, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-text_zone[0]-t_center[0], text_location[1]-(text_zone[1]*5)-t_center[1]))
        if i == 1:
            text = pygame.transform.rotozoom(text, -30, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-(text_zone[0]*3)-t_center[0], text_location[1]-(text_zone[1]*7)-t_center[1])) 
        if i == 2:
            text = pygame.transform.rotozoom(text, 30, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-(text_zone[0]*5)-t_center[0], text_location[1]-(text_zone[1]*7)-t_center[1])) 
        if i == 3:
            text = pygame.transform.rotozoom(text, 60, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-(text_zone[0]*7)-t_center[0], text_location[1]-(text_zone[1]*5)-t_center[1]))
        if i == 4:
            text = pygame.transform.rotozoom(text, -60, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-(text_zone[0]*7)-t_center[0], text_location[1]-(text_zone[1]*3)-t_center[1]))
        if i == 5:
            text = pygame.transform.rotozoom(text, -30, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-(text_zone[0]*5)-t_center[0], text_location[1]-(text_zone[1])-t_center[1]))
        if i == 6:
            text = pygame.transform.rotozoom(text, 30, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-(text_zone[0]*3)-t_center[0], text_location[1]-(text_zone[1])-t_center[1]))
        if i == 7:
            text = pygame.transform.rotozoom(text, 60, 1)
            t_center = text.get_rect().center
            screen.blit(text, (text_location[0]-text_zone[0]-t_center[0], text_location[1]-(text_zone[1]*3)-t_center[1]))


def draw():
    for (i, person) in enumerate(people):
        people[person].draw()
    for person in people:
        people[person].draw_text()


clock = pygame.time.Clock()

# basic game loop
while True:
    events() # check inputs from user
    database = database_check() # select records from the db
    geo_fence_check() # go through hashmap and check if location data is within any fence

    screen.fill(white)
    # pygame.draw.rect(screen, black, (400-8,300-8,16,16)) # center notch for hands
    screen.blit(clockface, (0,0)) # draw clock face

    draw_text()
    draw()

    pygame.display.update()
    clock.tick(60)