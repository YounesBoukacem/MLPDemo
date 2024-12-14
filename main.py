import pygame
import numpy as np

# pygame setup
screen_width = 1280
screen_height = 720
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("black")

grid_res = 28
cell_size = 10
explosion_coef = 5
explosion_radius = 3
border_color = 'white'
bg = 'black'

class DrawingGrid():

	def __init__(self, dest_surf:pygame.Surface, pos, res_x, res_y, cell_size, bg, border_color, explosion_coef, explosion_radius):
		self.img = np.zeros((res_x, res_y))
		self.dest_surf = dest_surf
		self.pos = pos
		self.res_x = res_x
		self.res_y = res_y
		self.cell_size = cell_size
		self.bg 	= bg
		self.border_color = border_color
		self.explosion_coef = explosion_coef
		self.explosion_radius = explosion_radius

		self.width	= res_x * cell_size
		self.height	= res_y * cell_size
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill(bg)
		pygame.draw.rect(
			surface=self.surf,
			color=border_color,
			rect=pygame.Rect(0, 0, self.width, self.height),
			width=1
		)
		dest_surf.blit(self.surf, (pos[0], pos[1]))
	
	def explode(self, pos):
		try:
			self.img[pos[0], pos[1]] = 1
		except IndexError:
			return
		# Drawing a rectangle around the point
		pygame.draw.rect(
			self.surf,
			pygame.Color('white'),
			pygame.Rect(pos[0]*self.cell_size, pos[1]*self.cell_size, self.cell_size, self.cell_size)
		)
		for r in range(1,self.explosion_radius+1):
			for i in [pos[0]+r, pos[0]-r]:
				for j in range(pos[1]-r, pos[1]+r+1):
					if not (0 <= i <self.res_x) or not (0 <= j <self.res_y): continue
					self.img[i, j] = min(1, self.img[i, j] + np.exp(-self.explosion_coef*r**2))
					pygame.draw.rect(
						self.surf,
						pygame.Color('black').lerp('white', self.img[i, j]),
						pygame.Rect(i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size)
					)

			for j in [pos[1]-r, pos[1]+r]:
				for i in range(pos[0]-r+1, pos[0]+r):
					if not (0 <= i <self.res_x) or not (0 <= j <self.res_y): continue				
					self.img[i, j] = min(1, self.img[i, j] + np.exp(-self.explosion_coef*r**2))
					pygame.draw.rect(
						self.surf,
						pygame.Color('black').lerp('white', self.img[i, j]),
						pygame.Rect(i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size)
					)

	def draw(self, mouse_pos):
		relative_x = mouse_pos[0] - self.pos[0]
		relative_y = mouse_pos[1] - self.pos[1]
		x_pos = int(relative_x / self.cell_size)
		y_pos = int(relative_y / self.cell_size)
		self.explode((x_pos, y_pos))
		self.dest_surf.blit(self.surf, (self.pos[0], self.pos[1]))

	def clear(self):
		self.surf.fill(self.bg)
		pygame.draw.rect(
			surface=self.surf,
			color=self.border_color,
			rect=pygame.Rect(0, 0, self.width, self.height),
			width=1
		)
		self.img = np.zeros((self.res_x, self.res_y))
		self.dest_surf.blit(self.surf, (self.pos[0], self.pos[1]))


# Creating the grid
grid_size = grid_res * cell_size
grid_pos_x = (screen_width-grid_size) / 2 
grid_pos_y = (screen_height-grid_size) / 2
drawing_grid = DrawingGrid(screen, (grid_pos_x, grid_pos_y), grid_res, grid_res, cell_size, bg, border_color, explosion_coef, explosion_radius)

# Initial Drawing
pygame.display.flip()

running = True
while running:
	
	if pygame.mouse.get_pressed()[0]:
		pos = pygame.mouse.get_pos()
		drawing_grid.draw(pos)

	if pygame.mouse.get_pressed()[2]:
		drawing_grid.clear()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()