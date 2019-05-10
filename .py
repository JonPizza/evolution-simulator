
import sys, time, pygame
from random import randint
from pygame.locals import *

NUMBER_PLAYERS = 2000
goal_pos = [735, 735]


def dist_to_goal(pos, goal_pos):
	return abs(pos[0]-goal_pos[0]) + abs(pos[1]-goal_pos[1])

class Dot:
	def __init__(self, display, color, mutate=None, instuctions=None, pos=None, alive=None, step=None, fitness=None):
		self.pos = [400, 400]
		self.mutate = mutate
		self.color = color
		self.instuctions = instuctions
		self.step = 0
		self.display = display
		self.alive = True
		self.fitness = 0

	def gen_random(self):
		self.instuctions = [] # Empty list

		for i in range(1000): # This is extended later
			self.instuctions.append([0, 0])

		for i in range(len(self.instuctions)):
			self.instuctions[i][0] = randint(-5, 5)
			self.instuctions[i][1] = randint(-5, 5)

	def show(self):
		pygame.draw.circle(self.display, self.color, self.pos, 4)
		self.step+=1

	def move(self):
		if self.mutate == True:
			if 0.01 != randint(1, 500)/100:
				if self.step < len(self.instuctions):
					self.pos[0] += self.instuctions[self.step][0]
					self.pos[1] += self.instuctions[self.step][1]
				else: # No more instructions! Gen more
					self.instuctions.append([0,0])
					self.instuctions[-1][0] = randint(-5, 5)
					self.instuctions[-1][1] = randint(-5, 5)
					self.pos[0] += self.instuctions[-1][0]
					self.pos[1] += self.instuctions[-1][1]
			else: # Some on the fly mutating b/c I give up.. Really dirty but at this point who cares...
				if self.step < len(self.instuctions):
					self.instuctions[self.step][0] = randint(-5, 5)
					self.instuctions[self.step][1] = randint(-5, 5)
					self.pos[0] += self.instuctions[self.step][0]
					self.pos[1] += self.instuctions[self.step][1]
				else: # No more instructions! Gen more
					self.instuctions.append([0,0])
					self.instuctions[-1][0] = randint(-5, 5)
					self.instuctions[-1][1] = randint(-5, 5)
					self.pos[0] += self.instuctions[-1][0]
					self.pos[1] += self.instuctions[-1][1]
		else:
			if self.step < len(self.instuctions):
				self.pos[0] += self.instuctions[self.step][0]
				self.pos[1] += self.instuctions[self.step][1]
			else:
				self.instuctions.append([0,0])
				self.instuctions[-1][0] = randint(-5, 5)
				self.instuctions[-1][1] = randint(-5, 5)
				self.pos[0] += self.instuctions[-1][0]
				self.pos[1] += self.instuctions[-1][1]

	def check_alive(self):
		if (self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] > 800 or self.pos[1] > 800) or (self.pos[0] > 700 and self.pos[0] < 770 and self.pos[1] > 700 and self.pos[1] < 770):
			# <ABOVE> Checks if out of bounds or inside goal
			self.alive = False

	def update(self):
		if self.alive:
			self.check_alive()
			self.move()
		self.show() # Still show even if dead

	def calc_fitness(self):
		# Use after dead
		# Should use quadrents, and the goal for finding best dots
		'''
		if self.pos[0] < 0 and self.pos[1] < 0:
			self.fitness = [] # If ur ded u get no points
			return
		elif self.pos[0] > 700 and self.pos[0] < 770 and self.pos[1] > 700 and self.pos[1] < 770: # Reached Goal
			pts = [1 for x in range(1)] # [1, 1, 1, 1 ...]

		else:
			pts = [] # Idk... ------------------------------------------------------------------------------ NEEDS TO BE OPTIMIZED!
		'''
		pts = (1540**2-dist_to_goal(self.pos, goal_pos)**2)

		

		self.fitness = pts

def select(display, dots):
	new_dots = []
	gen_score = 0
	for dot in dots: # calc fitness, find total pts
		dot.calc_fitness()
		gen_score += dot.fitness

	if gen_score <= 1:
		for dot in dots:
			dot.gen_random()
			new_dots.append(Dot(display, (0), False, dot.instuctions))
		return new_dots

	print(f'Gen Score: {gen_score}')

	for dot in dots:
		if dot.fitness > gen_score/NUMBER_PLAYERS:
			new_dots.append(Dot(display, (255, 0, 100), False, dot.instuctions))

	while len(new_dots) < len(dots):
		choice = randint(0, gen_score)
		count = 0
		for dot in dots:
			if count > choice:
				new_dots.append(Dot(display, (0), True, dot.instuctions))
				break
			count+=dot.fitness

	return new_dots

def main():
	pygame.init()

	WHITE=(255, 255, 255)
	BLUE=(200, 200, 255)
	RED=(255, 0, 0)
	GREEN=(0, 255, 0)
	BLACK=(0)
	gen = 1

	DISPLAY=pygame.display.set_mode((800,800),0,32)
	dots = []

	for i in range(NUMBER_PLAYERS): # Initialize NUMBER_PLAYER players and put them in list dots
		dots.append(Dot(DISPLAY, (0), True))

	for i in dots:
		i.gen_random()

	print('New Gen: 1')

	while True:
		while True:
			DISPLAY.fill(WHITE)

			pygame.draw.rect(DISPLAY, RED, [700, 700, 70, 70]) # Goal

			for i in dots:
				i.update()

			pygame.display.update()

			if dots[0].step == 5000:
				break

			# Check if need to exit
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()

		gen+=1

		dots = select(DISPLAY, dots)
		for i in dots:
			i.pos = [400, 400]
			i.step = 0
			i.alive = True

		print(f'New Gen: {gen}')

main()
