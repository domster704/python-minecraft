from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Inventory import *

app = Ursina()

ec = Entity()

path = 'data/texture/base_texture/'

order_blocks = [
	'stone_bricks',
	'dirt',
	'oak_planks',
	'bricks',
	'glass',
	'stone']

texture_list = [
	load_texture(f'{path}{order_blocks[0]}.png'),
	load_texture(f'{path}{order_blocks[1]}.png'),
	load_texture(f'{path}{order_blocks[2]}.png'),
	load_texture(f'{path}{order_blocks[3]}.png'),
	load_texture(f'{path}{order_blocks[4]}.png'),
	load_texture(f'{path}{order_blocks[5]}.png')]

hand_texture = load_texture('data/model/hand/arm_texture.png')
block_num = 0
pos = 0

sky_texture = load_texture('data/texture/skybox.png')
pickaxe = load_texture('data/texture/Diffuse.png')


def update():
	global block_num, pos

	# if held_keys['c']:
	# 	creativeMode()
	# elif held_keys['v']:
	# 	destroy(ec)

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

	# for i in range(len(inv.list_icons)):
	# 	texture_list[i] = inv.list_icons[i].texture

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
				# проверка на расстояние между нажатым блоком и player ( если меньше {6}, то можно поставить блок
				if block_num in range(0, len(texture_list)) and \
						sqrt((int(self.position.x) - int(player.position.x)) ** 2 + (
								(int(self.position.z) - int(player.position.z))) ** 2) <= 6:
					Block(position=self.position + mouse.normal, texture=texture_list[block_num])
			if key == 'left mouse down':
				if self.y != 0:
					# block_break_audio.play()
					destroy(self)


class Hand(Entity):
	def __init__(self):
		self.switch = 0
		self.pos_x = 0.6
		self.pos_y = -0.25
		self.d_x = self.d_y = 0.1

		super(Hand, self).__init__(
			parent=camera.ui,
			model='cube',
			texture=texture_list[block_num],
			scale=0.4,
			position=Vec2(self.pos_x, self.pos_y)
		)

	def setBlock(self, texture):
		self.model = 'cube'
		self.texture = texture
		self.scale = 0.4
		self.position = Vec2(self.pos_x, self.pos_y)

	def setTool(self):
		try:
			self.model = 'data/model/tool/Diamond-Pickaxe'
			self.texture = pickaxe
			self.scale = 0.03
			self.rotation = Vec3(60, 20, 45)
			self.position = Vec2(self.pos_x, self.pos_y)
		except Exception as e:
			print(e)

	def update(self):
		if block_num in range(0, len(texture_list)):
			self.setBlock(texture_list[block_num])
			self.switch = 1
		elif block_num in range(len(texture_list) - 1, 9) and self.switch == 1:
			self.setTool()
			self.switch = 0

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


# window.fullscreen = True


def creativeMode():
	ec = EditorCamera(enabled=True, rotation=(-37, 0, 0), positon=(20, 20, 20))
	ec.gizmo.enabled = False
	ec.pan_speed = Vec2(3, 3)
	ec.rotate_around_mouse_hit = True
	ec.move_speed = 10


if __name__ == "__main__":
	init_param()
	size_y = 32
	size_x = 32
	for y in range(size_y):
		for x in range(size_x):
			block = Block(position=(x, 0, y), texture=load_texture('data/texture/base_texture/grass_path_top.png'))

	inv = Inventory()
	inv.fillInv(order_blocks, texture_list)

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
