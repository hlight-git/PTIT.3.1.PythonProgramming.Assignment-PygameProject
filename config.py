WIN_WIDTH = 800
WIN_HEIGHT = 640

ZOOM_SCALE = 1
GAME_SPEED = 0.7
FPS = 120

CAM_WIDTH = WIN_WIDTH // ZOOM_SCALE
CAM_HEIGHT = WIN_HEIGHT // ZOOM_SCALE
SCROLL_LIMIT_HORIZON = WIN_WIDTH // 10 // ZOOM_SCALE
SCROLL_LIMIT_VERTICAL = WIN_HEIGHT // 10 // ZOOM_SCALE
SCROLL_SPEED = round(2 * GAME_SPEED // ZOOM_SCALE)

PADDING_WIDTH = WIN_WIDTH // 2 // ZOOM_SCALE
PADDING_HEIGHT = WIN_HEIGHT // 2 // ZOOM_SCALE
BACKGROUND_WIDTH = (WIN_WIDTH + PADDING_WIDTH) // ZOOM_SCALE
BACKGROUND_HEIGHT = (WIN_HEIGHT + PADDING_HEIGHT) // ZOOM_SCALE
PLAYER_WIDTH = 4*WIN_WIDTH//25//ZOOM_SCALE
PLAYER_HEIGHT = 5*WIN_HEIGHT//25//ZOOM_SCALE

WEAPON_WIDTH = (4*PLAYER_WIDTH//4)//ZOOM_SCALE
WEAPON_HEIGHT = (PLAYER_HEIGHT//4)//ZOOM_SCALE
TILESIZE = 1

ANIMATION_COOLDOWN = int(100 / GAME_SPEED)
ENEMY_GEN_COOLDOWN = 200
PLAYER_SPEED = round(5 * GAME_SPEED)
ENEMY_SPEED = round(5 * GAME_SPEED)
BULLET_SPEED = 15 * GAME_SPEED

# LAYER:
BACKGROUND_LAYER = 1
PLAYER_LAYER = 2
WEAPONS_LAYER = 3


# SOUND:
WEAPONS_CHANNEL = WEAPONS_LAYER

# GAMEPLAY:
PLAYER_MAX_HEALTH = 200
BASE_ATSD = round(4 / GAME_SPEED)

EMPTY = (0, 0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)

GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)