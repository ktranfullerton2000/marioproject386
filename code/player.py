import pygame 
from support import import_folder
from sound import *


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = pygame.transform.rotozoom(self.animations['idle'][self.frame_index], 0, 4)
		self.rect = self.image.get_rect(topleft = pos)
		self.sound = Sound()


		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -22

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		# player power up states. from 0 to 2, normal, super, flower
		self.states = 'normal'

		self.invulnerable_timer = pygame.time.get_ticks()
		# lives count
		self.lives = 3

	def get_invul_timer(self):
		return self.invulnerable_timer

	def change_invul_timer(self, time):
		self.invulnerable_timer = time

	def hit(self):
		self.lives -= 1
		print(f'lives left', self.lives)

	def import_character_assets(self):
		character_path = '../graphics/character/normal/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
			self.jump()

	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if not self.on_ground:
				self.status = 'fall'
			elif self.direction.x != 0:
				self.status = 'run'
			else: self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.sound.play_jump()
		self.direction.y = self.jump_speed

	def change_to_super(self):
		if not self.states == 'super':
			if self.states == 'fire':
				self.sound.play_pipe()
			else:
				self.sound.play_power_up()
			self.states = 'super'
			character_path = '../graphics/character/super/'
			for animation in self.animations.keys():
				full_path = character_path + animation
				self.animations[animation] = import_folder(full_path)

	def change_to_fire(self):
		if not self.states == 'fire':
			self.states = 'fire'
			character_path = '../graphics/character/flower/'
			self.sound.play_power_up()
			for animation in self.animations.keys():
				full_path = character_path + animation
				self.animations[animation] = import_folder(full_path)

	def change_to_normal(self):
		if not self.states == 'normal':
			self.states = 'normal'
			character_path = '../graphics/character/normal/'
			self.sound.play_pipe()
			for animation in self.animations.keys():
				full_path = character_path + animation
				self.animations[animation] = import_folder(full_path)

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		