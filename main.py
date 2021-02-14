from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Inventory import *

app = Ursina()

path = 'data/texture/base_texture/'

order_blocks = [
	'stone_bricks',
	'dirt',
	'oak_planks',
	'bricks',
	'glass']

texture_list = [
	load_texture(f'{path}{order_blocks[0]}.png'),
	load_texture(f'{path}{order_blocks[1]}.png'),
	load_texture(f'{path}{order_blocks[2]}.png'),
	load_texture(f'{path}{order_blocks[3]}.png'),
	load_texture(f'{path}{order_blocks[4]}.png')]

# block_break_audio = Audio('data/audio/stone1.mp3')
hand_texture = load_texture('data/model/hand/arm_texture.png')
block_num = 0
pos = 0

sky_texture = load_texture('data/texture/skybox.png')
pickaxe = load_texture('data/texture/Diffuse.png')
# grass_texture = load_texture('data/texture/expand_texture/grass_block.png')


def update():
	global block_num, pos

	# вход в инвентарь
	if held_keys['i']:
		mouse.locked = False
	elif held_keys['escape']:
		mouse.locked = True

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
		player.camera_pivot.y = 1.5
	else:
		player.camera_pivot.y = 2

	# выбор блока
	for val, key in held_keys.items():
		if key == 1:
			if val in list('123456789'):
				block_num = pos = int(val) - 1

	try:
		for i in range(len(inv.list_icons)):
			inv.list_icons[i].color = color.white
			inv.list_icons[pos].color = color.gray
	except Exception as e:
		pass


class Block(Button):
	def __init__(self, position=(0, 0, 0), texture=texture_list[block_num]):
		super().__init__(
			parent=scene,
			position=position,
			model='cube',
			origin_y=.5,
			texture=texture,
			color=color.color(0, 0, random.uniform(.9, 1.0)),
			scale=1
		)

	def input(self, key):
		if self.hovered:
			if key == 'right mouse down':
				Block(position=self.position + mouse.normal, texture=texture_list[block_num])
			if key == 'left mouse down':
				if self.y != 0:
					# block_break_audio.play()
					destroy(self)


class Hand(Entity):
	def __init__(self):
		# self.pos_x = 0.8
		# self.pos_y = -0.6
		self.pos_x = 0.6
		self.pos_y = -0.25

		super(Hand, self).__init__(
			parent=camera.ui,
			model='data/model/tools/Diamond-Pickaxe',
			texture=pickaxe,
			scale=0.03,
			rotation=Vec3(60, 20, 45),
			# rotation=Vec3(0, -80, 5),
			position=Vec2(self.pos_x, self.pos_y)
		)
		self.d_x = self.d_y = 0.1

	def active(self):
		self.position = Vec2(self.pos_x - self.d_x, self.pos_y + self.d_y)
		self.rotation = Vec3(70, 20, 45)

	def passive(self):
		self.position = Vec2(self.pos_x, self.pos_y)
		self.rotation = Vec3(60, 20, 45)


class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent=scene,
			model='sphere',
			texture=sky_texture,
			scale=150,
			double_sided=True)


def init_param():
	window.borderless = False
	window.vsync = False
	window.title = "Minecraft"
	window.exit_button.visible = False
	camera.fov = 3


if __name__ == "__main__":
	init_param()
	size_y = 32
	size_x = 32
	for y in range(size_y):
		for x in range(size_x):
			block = Block(position=(x, 0, y), texture=load_texture('data/texture/base_texture/grass_path_top.png'))

	for y in range(size_y):
		for x in range(size_x):
			if y == 0 or y == size_y - 1:
				block = Block(position=(x, 1, y))
			if x == size_x - 1 or x == 0:
				block = Block(position=(x, 1, y))

	inv = Inventory()
	inv.fillInv(order_blocks, texture_list)

	player = FirstPersonController()
	player.position = (5, 0, 5)
	player.mouse_sensitivity = Vec2(50, 50)
	player.jump_duration = 0.2

	hand = Hand()
	sky = Sky()
	app.run()
