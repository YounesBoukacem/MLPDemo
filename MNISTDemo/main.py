import pygame
import numpy as np

# pygame setup
screen_width = 1280
screen_height = 720
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("black")


# __Creating the grid__

# Parameters
grid_res = 28
cell_size = 10
explosion_coef = 0
explosion_radius = 0
border_color = 'white'
bg = 'black'

# Grid class
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
		padding = 5
		self.border_surface = pygame.Surface((self.width+2*padding, self.height+2*padding))
		self.border_surface.fill(bg)
		pygame.draw.rect(
			surface=self.border_surface,
			color=border_color,
			rect=pygame.Rect(0, 0, self.width+2*padding, self.height+2*padding),
			width=1
		)
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill(bg)
		dest_surf.blit(self.surf, (pos[0], pos[1]))
		dest_surf.blit(self.border_surface, (pos[0]-padding, pos[1]-padding))

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
		self.img = np.zeros((self.res_x, self.res_y))
		self.dest_surf.blit(self.surf, (self.pos[0], self.pos[1]))


# Instantiating the grid
grid_size = grid_res * cell_size
grid_pos_x = 100#(screen_width-grid_size) / 2 
grid_pos_y = (screen_height-grid_size) / 2
drawing_grid = DrawingGrid(screen, (grid_pos_x, grid_pos_y), grid_res, grid_res, cell_size, bg, border_color, explosion_coef, explosion_radius)


# __Submit button__
class TextButton():
	def __init__(self, dest_surf:pygame.Surface, pos, dim, bg, border_color, text, text_color, font_size):
		self.dest_surf = dest_surf
		self.pos = pos
		self.dim = dim

		self.button_surf = pygame.Surface(dim)
		self.button_surf.fill(bg)
		pygame.draw.rect(self.button_surf, border_color, self.button_surf.get_rect(), 1, 2)
		
		self.text_surf = pygame.font.SysFont(None, font_size).render(text, True, text_color)
		text_surf_x = (dim[0] - self.text_surf.get_width()) / 2
		text_surf_y = (dim[1] - self.text_surf.get_height()) / 2
		self.button_surf.blit(self.text_surf, (text_surf_x, text_surf_y))
		self.dest_surf.blit(self.button_surf, pos)
	
	def click(self, click_pos):
		if self.pos[0] < click_pos[0] < self.pos[0] + self.dim[0] and self.pos[1] < click_pos[1] < self.pos[1] + self.dim[1]:
			return True
		return False

submit_button_width = 100
submit_button_height = 50
submit_button_x = grid_pos_x + (grid_size - submit_button_width) / 2
submit_button_y = grid_pos_y + grid_size + 50
submit_button = TextButton(screen,
						   (submit_button_x, submit_button_y),
						   (submit_button_width, submit_button_height),
						   'black','white',
						   'Submit','white', 36)
# Initial Drawing
pygame.display.flip()

running = True

# import torch

# # Define the model
# class MNISTModel(torch.nn.Module):
# 	def __init__(self):
# 		super(MNISTModel, self).__init__()
# 		self.flatten = torch.nn.Flatten()
# 		self.linear_relu_stack = torch.nn.Sequential(
# 			torch.nn.Linear(28*28, 512),
# 			torch.nn.ReLU(),
# 			torch.nn.Linear(512, 512),
# 			torch.nn.ReLU(),
# 			torch.nn.Linear(512, 10),
# 			torch.nn.LogSoftmax(dim=1)
# 		)
		
# 	def forward(self, x):
# 		x = self.flatten(x)
# 		log_probs = self.linear_relu_stack(x)
# 		return log_probs

# model = MNISTModel()
# model.load_state_dict(torch.load('D:\projects\MLPDemo\MNISTDemo\mnist_model.pth'))

from tensorflow.keras.models import load_model
model = load_model('D:\projects\MLPDemo\MNISTDemo\mnist_model.keras')

while running:
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEMOTION:
			if event.buttons[0]:
				pos = pygame.mouse.get_pos()
				drawing_grid.draw(pos)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 3:
				drawing_grid.clear()
			elif event.button == 1:
				if submit_button.click(pygame.mouse.get_pos()):
					# example = torch.tensor(drawing_grid.img, dtype=torch.float32).view(-1)
					# probs = torch.exp(model(example.expand(1, -1))).squeeze(0)
					# print(probs)
					# print(torch.argmax(probs))
					print(np.argmax(model.predict(drawing_grid.img.reshape(1, 28, 28))))
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()