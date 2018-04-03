#gamestest class: run this to test the game

from tile import Tile
import pygame
import random
import time
from tkinter import *
from tkinter import messagebox
from pygame.locals import *

#can change filenames to use your own pictures
tileNames = ['space-1a.png', 'space-1b.png', 'space-1c.png', 'space-1d.png', 'space-1e.png',
			 'space-2a.png', 'space-2b.png', 'space-2c.png', 'space-2d.png', 'space-2e.png',
			 'space-3a.png', 'space-3b.png', 'space-3c.png', 'space-3d.png', 'space-3e.png',
			 'space-4a.png', 'space-4b.png', 'space-4c.png', 'space-4d.png', 'space-4e.png',
			 'space-5a.png', 'space-5b.png', 'space-5c.png', 'space-5d.png', 'blank.png']

#all possible top-left coordinates of tile locations
tileCoords = [(0, 0), (200, 0), (400, 0), (600, 0), (800,0),
			  (0, 200), (200, 200), (400, 200), (600, 200), (800, 200),
			  (0, 400), (200, 400), (400, 400), (600, 400), (800, 400),
			  (0, 600), (200, 600), (400, 600), (600, 600), (800, 600),
			  (0, 800) , (200, 800), (400, 800), (600, 800), (800,800)]

#directory of where images are located
imageFolder = 'images/'

#initialize required variables
ANSWERKEY = []
POINTS = 0
TILESIZE = 200
numElements = 25
BackGround = []
clickedTile = []
emptyTile = []
movable = False
x = y = startClock = endClock = 0
startTimer = True
root = Tk()
root.withdraw()

def __init__(self):
	pygame.sprite.Sprite.__init__(self)
	screen = pygame.display.get_surface()
	self.area = screen.get_rect()

#a tile is only movable if it's tangent to the empty tile
def canMove(tile):
	global emptyTile
	if tile.x == emptyTile[0] and((tile.y - TILESIZE) == emptyTile[1] or (tile.y + TILESIZE) == emptyTile[1]):
		return True
	elif  tile.y == emptyTile[1] and ((tile.x - TILESIZE) == emptyTile[0] or (tile.x + TILESIZE) == emptyTile[0]):
		return True
	return False

#switch the clicked tile and empty tile
def move(tile, empty):
	global emptyTile
	emptyTile[0]= tile.x
	emptyTile[1] = tile.y
	tile.name, empty.name = empty.name, tile.name
	tile.image, empty.image = empty.image, tile.image

#return the index of the tile (elements 0-24)
def getIndex(coords):
	for i in range(numElements):
		if [coords[0], coords[1]] == [tileCoords[i][0], tileCoords[i][1]]:
			return i

#win condition is all tile names and locations match that of the answer key
def win():
	for i in range(numElements):
		if BackGround[i].name != ANSWERKEY[i].name:
			return False
	return True

#randomize location of tiles
def randomize():
	rInt = random.randint(75, 150)
	while rInt > 0:
		j = random.randint(0, 24)
		if canMove(BackGround[j]):
			emptyTileIndex = getIndex(emptyTile)
			move(BackGround[j], BackGround[emptyTileIndex])
			rInt -= 1


#populate the answer key
for i in range(numElements):
	ANSWERKEY.append(Tile(imageFolder+tileNames[i], tileCoords[i][0], tileCoords[i][1]))

#populate the board
for i in range(numElements):
	BackGround.append(Tile(imageFolder+tileNames[i], tileCoords[i][0], tileCoords[i][1]))
	if tileNames[i] == 'blank.png':
		emptyTile = [BackGround[i].x, BackGround[i].y]

#randomize the board (initial state is the same as answer key)
randomize()

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Tile Game (NOTE: press H for hint)')

while True: # main game loop

	#display the background
	for i in range(len(BackGround)):
		screen.blit(BackGround[i].image, (BackGround[i].x, BackGround[i].y))
		#pygame.display.update()

	#listening for events from user
	for event in pygame.event.get():

		#show hint on h key downpress or randomize board on r key downpress
		if event.type == KEYDOWN:
			if event.key == pygame.K_h:
				movable = False
				for i in range(numElements):
					BackGround[i].image, ANSWERKEY[i].image = ANSWERKEY[i].image, BackGround[i].image
					BackGround[i].x, ANSWERKEY[i].x = ANSWERKEY[i].x, BackGround[i].x
					BackGround[i].y, ANSWERKEY[i].y = ANSWERKEY[i].y, BackGround[i].y
			elif event.key == pygame.K_r:
				for i in range(numElements):
					BackGround[i] = ANSWERKEY[i]
				randomize()

		#show real board on h key release
		if event.type == KEYUP:
			if event.key == pygame.K_h:
				for i in range(numElements):
					BackGround[i].image, ANSWERKEY[i].image = ANSWERKEY[i].image, BackGround[i].image
					BackGround[i].x, ANSWERKEY[i].x = ANSWERKEY[i].x, BackGround[i].x
					BackGround[i].y, ANSWERKEY[i].y = ANSWERKEY[i].y, BackGround[i].y

		#upon mouse button press, will attempt to move the tile clicked
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			for Tile in BackGround:
				if Tile.rect.collidepoint(pos):
					clickedTile = Tile

			#If movable then move the tile
			movable = canMove(clickedTile)

			if movable:
				#start the timer upon the user's first move
				if startTimer:
					startTimer = False
					startClock = time.time()

				#get the locations of the empty tile and clicked tile, then move the two tiles
				emptyTileIndex = getIndex(emptyTile)
				clickedTileIndex = getIndex([clickedTile.x, clickedTile.y])
				move(BackGround[clickedTileIndex], BackGround[emptyTileIndex])

				# upon completion of the puzzlebox, display win message
				if win():
					pygame.display.update()
					endClock = time.time()
					timeTaken = endClock - startClock
					messagebox.showinfo('You Win!',
										'Congratulations! You have successfully completed the puzzle box!\nIt only took: %i seconds!' % (
										int(timeTaken)))
					pygame.quit()
					sys.exit()

		if event.type == QUIT:

			pygame.quit()

			sys.exit()

	#update user display
	pygame.display.update()
