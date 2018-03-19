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

imageFolder = 'images/'

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

def firstMove():
	return startTimer

##Moving a tile into the correct location should add one point. Moving a correct off of a correct location should subtract one point.
#def correctMove(self, other, answer):
#	for Tile in BackGround:
#		if other.x == answer.x and other.y == answer.y:
#			correctName = answer.name
#	if correctName == answer.name:
#		return True
#	return False
#
##win condition is all 25 tiles in their corresponding locations, or 25 correct points
#def win():
#	return POINTS == 25

#brute force win condition to get it working... very slow implementation and lots to improve on...
def win():
	for i in range(numElements):
		if BackGround[i].name != ANSWERKEY[i].name:
			return False
	return True

#populate the answerkey
for i in range(numElements):
	ANSWERKEY.append(Tile(imageFolder+tileNames[i], tileCoords[i][0], tileCoords[i][1]))

#randomly populate the board with tiles
for i in range(numElements):
	rInt = random.randint(0, len(tileNames)-1)
	rLoc = tileCoords[i]
	BackGround.append(Tile(imageFolder+tileNames[rInt], rLoc[0], rLoc[1]))
	if tileNames[rInt] == 'blank.png':
		emptyTile = [BackGround[i].x, BackGround[i].y]
	tileNames.remove(tileNames[rInt])
	if BackGround[i].name == ANSWERKEY[i].name:
		POINTS += 1

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Tile Game (NOTE: impossible puzzles exist due to parity)')

while True: # main game loop

	#display the background
	for i in range(len(BackGround)):
		screen.blit(BackGround[i].image, (BackGround[i].x, BackGround[i].y))
		#pygame.display.update()

	#upon completion of the puzzlebox a message will popup
	if win():
		endClock = time.time()
		timeTaken = endClock-startClock
		messagebox.showinfo('You Win!', 'Congratulations! You have successfully completed the puzzle box!\nIt only took: %i seconds!' % (int(timeTaken)))
		pygame.quit()
		sys.exit()

	#listening for events from user
	for event in pygame.event.get():

		#show hint on h key downpress
		if event.type == KEYDOWN:
			if event.key == pygame.K_h:
				movable = False
				for i in range(numElements):
					BackGround[i].image, ANSWERKEY[i].image = ANSWERKEY[i].image, BackGround[i].image
					BackGround[i].x, ANSWERKEY[i].x = ANSWERKEY[i].x, BackGround[i].x
					BackGround[i].y, ANSWERKEY[i].y = ANSWERKEY[i].y, BackGround[i].y

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
#			for Tile in ANSWERKEY:
#				if Tile.rect.collidepoint(pos):
#					clickedTileANSWER = Tile

			#If movable then move the tile
			movable = canMove(clickedTile)
			if movable:
				#start the timer upon the user's first move
				if firstMove():
					startTimer = False
					startClock = time.time()
				#get the locations of the empty tile and clicked tile, then move the two tiles
				emptyTileIndex = getIndex(emptyTile)
				clickedTileIndex = getIndex([clickedTile.x, clickedTile.y])
				move(BackGround[clickedTileIndex], BackGround[emptyTileIndex])
				#screen.blit(clickedTile.image, [clickedTile.x, clickedTile.y])
				#screen.blit(emptyTile.image, [emptyTile.x, emptyTile.y])
				#screen.blit(BackGround[clickedTileIndex].image, [BackGround[clickedTileIndex].x, BackGround[clickedTileIndex].y])
				#screen.blit(BackGround[emptyTileIndex].image, [BackGround[emptyTileIndex].x, BackGround[emptyTileIndex].y])
				#pygame.display.update()

		if event.type == QUIT:

			pygame.quit()

			sys.exit()

	pygame.display.update()
