import pygame
import os

FILEDIR = os.path.dirname(__file__)



def game():
    return window


def init_game():
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
    pygame.display.set_caption("My Game")
    return win


def load_image(image, size):
    image = pygame.image.load(f'{FILEDIR}/{image}.png').convert()
    image_size = image.get_size()
    ratio = image_size[1]/image_size[0]
    x = int(size)
    y = int(ratio * x)
    image = pygame.transform.scale(image, (x, y))
    image.set_colorkey(WHITE)
    return image


SCREEN_WIDTH = int(1920//1.25)
SCREEN_HEIGHT = int(1080//1.25)
window = init_game()


SCREEN_SCALE = 2
PLAYER_VEL = 400 * SCREEN_SCALE
ENEMY_VEL = 200 * SCREEN_SCALE
CANNON_VEL = 1000 * SCREEN_SCALE
ROCKET_VEL = 3000 * SCREEN_SCALE
MISSILE_VEL = 600 * SCREEN_SCALE

PLAYER_ACC = 1
ENEMY_ACC = 1
CANNON_ACC = 2
ROCKET_ACC = 2
MISSILE_ACC = 0.75

PLAYER_MASS = 100
ENEMY_MASS = 20
CANNON_MASS = 2
ROCKET_MASS = 5
MISSILE_MASS = 10
HEALTH_MASS = -10
SHIELDS_MASS = 0.1
DAMPERS_MASS = 0.1

PLAYER_SIZE = int(40 * SCREEN_SCALE)
ENEMY_SIZE = int(50 * SCREEN_SCALE)
CANNON_SIZE = int(15 * SCREEN_SCALE)
ROCKET_SIZE = int(20 * SCREEN_SCALE)
MISSILE_SIZE = int(25 * SCREEN_SCALE)
HEALTH_SIZE = int(25 * SCREEN_SCALE)
SHIELDS_SIZE = int(20 * SCREEN_SCALE)
DAMPERS_SIZE = int(20 * SCREEN_SCALE)
BLACK_HOLE_SIZE = int(75 * SCREEN_SCALE)

SHIELDS_RADIUS = 1000
SHIELDS_DISCHARGE_RATE = 50
SKILL_SPREAD = 0

FPS = 100
CLOCK = pygame.time.Clock()
TIME_STEP = 1 / FPS

G_CONSTANT = 10000000 * SCREEN_SCALE**2

BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

PLAYER_IMAGE = load_image('player', PLAYER_SIZE)
ENEMY_IMAGE = load_image('trump', ENEMY_SIZE)
CANNON_IMAGE = load_image('cannon', CANNON_SIZE)
ROCKET_IMAGE = load_image('rocket', ROCKET_SIZE)
ROCKET_IMAGE_NO_THRUST = load_image('rocket_no_thrust', ROCKET_SIZE)
MISSILE_IMAGE = load_image('trump_missile', MISSILE_SIZE)
MISSILE_IMAGE_NO_THRUST = load_image('trump_missile', MISSILE_SIZE)
HEALTH_IMAGE = load_image('health', HEALTH_SIZE)
SHIELDS_IMAGE = load_image('shields', SHIELDS_SIZE)
DAMPERS_IMAGE = load_image('dampers', DAMPERS_SIZE)
BLACK_HOLE_IMAGE = load_image('black_hole', BLACK_HOLE_SIZE)
CANNON_EXPLOSION_IMAGE = load_image('explosion', 2*CANNON_SIZE)
ROCKET_EXPLOSION_IMAGE = load_image('explosion', 2*ROCKET_SIZE)
MISSILE_EXPLOSION_IMAGE = load_image('explosion', 2*MISSILE_SIZE)

ENEMY_SOUND = pygame.mixer.Sound(f'{FILEDIR}/missile.mp3')
CANNON_SOUND = pygame.mixer.Sound(f'{FILEDIR}/cannon.mp3')
ROCKET_SOUND = pygame.mixer.Sound(f'{FILEDIR}/rocket.mp3')
MISSILE_SOUND = pygame.mixer.Sound(f'{FILEDIR}/missile.mp3')
SHIELDS_SOUND = pygame.mixer.Sound(f'{FILEDIR}/shields.mp3')
CANNON_HIT_SOUND = pygame.mixer.Sound(f'{FILEDIR}/cannon_hit.mp3')
DESTROY_SOUND = pygame.mixer.Sound(f'{FILEDIR}/destroy.mp3')
HEALTH_PICKUP_SOUND = pygame.mixer.Sound(f'{FILEDIR}/food_pickup.mp3')
SHIELDS_PICKUP_SOUND = pygame.mixer.Sound(f'{FILEDIR}/shields_pickup.mp3')
