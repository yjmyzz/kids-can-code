# game options

SIZE = WIDTH, HEIGHT = 320, 480
FPS = 60
DEBUG = False

TITLE = "Jumpy!"

# Player properties
PLAYER_ACC = 0.6
PLAYER_GRAVITY = 1.2
PLAYER_FRICTION = -0.06
PLAYER_JUMP = 20
FONT_NAME = "Menlo"
HIGH_SCORE_FILE = "../data/high_score.txt"
SPRITE_SHEET_PNG_FILE = "../img/spritesheet_jumper.png"
SPRITE_SHEET_XML_FILE = "../img/spritesheet_jumper.xml"

# starting platform
# PLATFORM_LIST = [(5, HEIGHT - 35),
#                  (WIDTH / 2 - 50, HEIGHT * 0.75),
#                  (WIDTH * 0.12, HEIGHT * 0.5),
#                  (WIDTH * 0.65, 200),
#                  (WIDTH * 0.5, 100)]

PLATFORM_LIST = [(15, HEIGHT - 35),
                 (55, HEIGHT - 140),
                 (5, HEIGHT - 215),
                 (WIDTH * 0.70, 180),
                 (WIDTH * 0.5, 100)]

# define color
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
LIGHT_BLUE = 0, 155, 155
BG_COLOR = LIGHT_BLUE
