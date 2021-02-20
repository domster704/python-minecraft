from ursina import *

pos = 0


class Inventory(Entity):
	def __init__(self):
		super(Inventory, self).__init__(
			parent=camera.ui,
			model='quad',
			scale=(1, .1),
			origin=(-.5, .5),
			position=(-.5, -.37, -0.01),
			texture='white_cube',
			texture_scale=(9, 1),
			color=color.smoke
		)
		self.item_parent = Entity(parent=self, scale=(1 / 9, 1))
		self.list_icons = []

	def fillInv(self, order_blocks, texture_list):
		for i in range(len(texture_list)):
			self.add(order_blocks[i], texture_list[i])

	def findFreeSpot(self):
		spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]
		for y in range(1):
			for x in range(8):
				if not (x, -y) in spots:
					return x, -y

	def add(self, item, texture):
		icon = Draggable(
			parent=self.item_parent,
			model='quad',
			origin=(-.55, .55),
			texture=texture,
			color=color.white,
			position=self.findFreeSpot(),
			scale=0.9,
			z=-1
		)
		self.list_icons.append(icon)
		name = item.title()
		icon.tooltip = Tooltip(name)
		icon.tooltip.background.color = color.color(0, 0, 0, .8)

		def drag():
			icon.org_pos = (icon.x, icon.y)
			icon.z -= .01  # ensure the dragged item overlaps the rest

		def drop():
			icon.x = int(icon.x)
			icon.y = int(icon.y)

			# если вытащили предемет за периметр инвенторя, вернуть в изначальное положение
			if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
				icon.position = icon.org_pos
				return

			for c in self.children:
				if c == icon:
					continue

				if c.x == icon.x and c.y == icon.y:
					print('swap positions')
					icon.position = c.position
					c.position = icon.org_pos
					self.list_icons[self.list_icons.index(c)], self.list_icons[self.list_icons.index(icon)] = \
					self.list_icons[self.list_icons.index(icon)], self.list_icons[self.list_icons.index(c)]

		icon.drag = drag
		icon.drop = drop


def update():
	global pos
	if held_keys['1']: pos = 0
	if held_keys['2']: pos = 1
	if held_keys['3']: pos = 2
	if held_keys['4']: pos = 3

	inv.list_icons[pos].color = color.gray


if __name__ == "__main__":
	app = Ursina()
	inv = Inventory()
	inv.add("dirt", 'data/texture/base_texture/grass.png')
	app.run()
