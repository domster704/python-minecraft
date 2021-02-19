from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import textures
from ursina.shaders import *
from ursina.shaders import texture_blend_shader
from Inventory import *
from PerlinNoise import *
import numpy as np

app = Ursina()

blockBreakStone = Audio('data/audio/stone.wav', loop=False, autoplay=False)
blockBreakDirt = Audio('data/audio/grass.wav', loop=False, autoplay=False)
blockBreakWood = Audio('data/audio/wood.wav', loop=False, autoplay=False)
blockBreakGlass = Audio('data/audio/glass.wav', loop=False, autoplay=False)

path = 'data/texture/base_texture/'

order_blocks = (
	'stone_bricks',
	'dirt',
	'planks',
	'bricks',
	'glass',
	'stone')

stoneBrickTex = load_texture(f'{path}{order_blocks[0]}.png')
dirtTex = load_texture(f'{path}{order_blocks[1]}.png')
planksTex = load_texture(f'{path}{order_blocks[2]}.png')
brickTex = load_texture(f'{path}{order_blocks[3]}.png')
glassTex = load_texture(f'{path}{order_blocks[4]}.png')
stoneTex = load_texture(f'{path}{order_blocks[5]}.png')

texture_list = np.array(
	[(stoneBrickTex, blockBreakStone),
	 (dirtTex, blockBreakDirt),
	 (planksTex, blockBreakWood),
	 (brickTex, blockBreakStone),
	 (glassTex, blockBreakGlass),
	 (stoneTex, blockBreakStone)])

hand_texture = load_texture('data/model/hand/arm_texture.png')
block_num = 0
pos = 0
w = 0
sky_texture = load_texture('data/texture/skybox.png')
pickaxe = load_texture('data/texture/Diffuse.png')


def update():
	global block_num, pos, w

	# творческий режим
	# if held_keys['c']:
	# 	creativeMode()
	# elif held_keys['v']:
	# 	destroy(ec)

	# вход в инвентарь
	if held_keys['i']:
		mouse.locked = False
		w = WindowPanel(
			title='Custom Window',
			content=(
				Text('Name:'),
				InputField(name='name_field'),
				Button(text='Submit', color=color.azure),
			),
		)
	elif held_keys['escape']:
		mouse.locked = True
		try:
			w.close()
		except:
			pass

	# обработчик анимации руки
	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	# управление скоростью персонажа при нажатии Shift
	if held_keys['left shift']:
		player.speed = 10
	else:
		player.speed = 5

	# управление приседанием персонажа при нажатии Ctrl
	if held_keys['left control']:
		player.camera_pivot.y = 1.4
	else:
		player.camera_pivot.y = 1.8

	# выбор блока
	for val, key in held_keys.items():
		if key == 1:
			if val in list('123456789'):
				block_num = pos = int(val) - 1

	# for i in range(len(inv.list_icons)):
	# 	texture_list[i] = inv.list_icons[i].texture

	try:
		for i in range(len(inv.list_icons)):
			inv.list_icons[i].color = color.white
			inv.list_icons[pos].color = color.gray
	except Exception as e:
		pass


class Block(Button):
	def __init__(self, position=(0, 0, 0), model='data/model/block/1', texture=texture_list[block_num][0], scale=1,
				 nameBlock=order_blocks[block_num]):
		super().__init__(
			parent=scene,
			position=position,
			model=model,
			origin_y=.5,
			texture=texture,
			color=color.color(0, 0, random.uniform(.9, 1.0)),
			scale=scale,
		)
		self.nameBlock = nameBlock

	def input(self, key):
		if self.hovered:
			# проверка на расстояние между нажатым блоком и player ( если меньше {6}, то можно поставить блок
			checking = sqrt((int(self.position.x) - int(player.position.x)) ** 2 + (
				(int(self.position.z) - int(player.position.z))) ** 2) <= 10
			if key == 'right mouse down':
				# TODO: добавить лестниу (уже добевлена, но надо улучшить)
				# Block(position=self.position + mouse.normal, model='data/model/stairs/stairs',
				# 	  texture=load_texture('data/model/stairs/east.png'))
				if block_num in range(0, len(texture_list)) and checking:
					if order_blocks[block_num] == 'glass':
						blockBreakStone.play()
					else:
						texture_list[block_num][1].play()
					Block(position=self.position + mouse.normal, texture=texture_list[block_num][0], nameBlock=order_blocks[block_num])
			if key == 'left mouse down' and checking:
				try:
					print(self.nameBlock)
					texture_list[order_blocks.index(self.nameBlock)][1].play()
				except:
					pass
				if self.y != 0:
					destroy(self)


class Hand(Entity):
	def __init__(self):
		self.k = -1
		self.switch = 0
		self.pos_x = 0.6
		self.pos_y = -0.25
		self.pos_z = 10
		self.d_x = self.d_y = 0.1

		super(Hand, self).__init__(
			parent=camera.ui,
			model='cube',
			texture=texture_list[block_num][0],
			scale=0.4,
			position=Vec2(self.pos_x, self.pos_y),
			shader=lit_with_shadows_shader
		)

	def setBlock(self, texture):
		try:
			self.model = 'cube'
			self.texture = texture
			self.scale = 0.4
			self.position = Vec2(self.pos_x, self.pos_y)
		except Exception as e:
			print(e)

	def setTool(self):
		try:
			# self.model = 'data/model/tool/Diamond-Pickaxe'
			# self.parent = scene
			self.model = 'data/model/tool/Diamond-Pickaxe'
			self.texture = pickaxe
			self.scale = 0.03
			self.rotation = Vec3(60, 20, 45)
			self.position = Vec2(self.pos_x, self.pos_y)
		except Exception as e:
			print(e)

	# def setStairs(self):
	# 	self.model = 'data/model/stairs/stairs'
	# 	self.texture = load_texture('data/model/stairs/east.png')
	# 	self.scale = 1
	# 	self.rotation = Vec3(60, 20, 45)
	# 	self.position = Vec2(self.pos_x, self.pos_y)

	def update(self):
		# if block_num in 9:
		# 	self.setStairs()
		if block_num in range(0, len(texture_list)) and self.k != block_num:
			self.setBlock(texture_list[block_num][0])
			self.switch = 1
			self.k = block_num
		elif block_num in range(len(texture_list), 9) and self.switch == 1:
			self.setTool()
			self.switch = 0

	def active(self):
		if block_num in range(0, len(texture_list)):
			self.position = Vec2(self.pos_x - self.d_x, self.pos_y + self.d_y)
			self.rotation = Vec3(70, 20, 45)
		else:
			self.position = Vec2(self.pos_x - self.d_x / 2, self.pos_y + self.d_y)
			self.rotation = Vec3(60, 20, 40)

	def passive(self):
		if block_num in range(0, len(texture_list)):
			self.position = Vec2(self.pos_x, self.pos_y)
			self.rotation = Vec3(60, 20, 45)
		else:
			self.position = Vec2(self.pos_x, self.pos_y)
			self.rotation = Vec3(60, 20, 45)


class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent=scene,
			model='sphere',
			# texture=sky_texture,
			texture='sky_default',
			scale=600,
			double_sided=True)


def init_param():
	window.borderless = False
	window.vsync = False
	window.title = "Minecraft"
	window.exit_button.visible = False


# window.fullscreen = True
# Light(type='ambient', color=(1, 1, 1, 1))


def creativeMode():
	EditorCamera()


# enabled = True, rotation = (-37, 0, 0), positon = (20, 20, 20)
# ec.gizmo.enabled = False
# ec.pan_speed = Vec2(3, 3)
# ec.rotate_around_mouse_hit = True
# ec.move_speed = 10
# player.add_script(NoclipMode2d())


if __name__ == "__main__":
	init_param()
	size_y = 32
	size_x = 32
	for y in range(size_y):
		for x in range(size_x):
			block = Block(position=(x, 0, y),
						  texture=load_texture('data/texture/base_texture/grass_top.png'),
						  nameBlock='grass'
						  )

	map1 = perlineNoise()
	map2 = perlineNoise()


	def checkNear(map, x, y):
		try:
			if map[x + 1][y] == '-' or map[x - 1][y] == '-' or map[x][y + 1] == '-' or map[x][y - 1] == '-' or \
					map[x + 1][y + 1] == '-' or map[x + 1][y - 1] == '-' or map[x - 1][y + 1] == '-' or map[x - 1][
				y - 1] == '-':
				return False
			else:
				return True
		except IndexError:
			pass


	textureDirt = load_texture('data/texture/base_texture/dirt.png')
	for y in range(size_y):
		for x in range(size_x):
			if map1[y][x] == '#':
				block = Block(position=(x, 1, y),
							  texture=textureDirt,
							  nameBlock='dirt'
							  )
			if map2[y][x] == '#' and map1[y][x] == "#" and checkNear(map1, y, x):
				block = Block(position=(x, 2, y),
							  texture=textureDirt,
							  nameBlock='dirt'
							  )

	print(texture_list[:, :-1])
	inv = Inventory()
	inv.fillInv(order_blocks, texture_list[:, :-1])

	player = FirstPersonController()
	cursorTexture = load_texture('data/texture/cursor.png')
	destroy(player.cursor)
	player.cursor = Entity(parent=camera.ui, model='quad', scale=.03, texture=cursorTexture,
						   position_z=-0.01)
	player.position = (5, 0, 5)
	player.mouse_sensitivity = Vec2(50, 50)
	player.jump_duration = 0.2

	hand = Hand()
	sky = Sky()
	app.run()
