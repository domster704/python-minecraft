from ursina import *

pos = 0


class Inventory(Entity):
    def __init__(self, **kwargs):
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

        for key, value in kwargs.items():
            setattr(self, key, value)

        # self.item_parent = Entity(parent=self, scale=(1 / 9, 1))
        self.list_icons = []

    def fillInv(self, order_blocks, texture_list):
        for i in range(len(texture_list)):
            self.add(order_blocks[i], texture_list[i])

    def findFreeSpot(self):
        grid_positions = [(int(e.x * self.texture_scale[0]), int(e.y * self.texture_scale[1])) for e in self.children]
        for y in range(1):
            for x in range(9):
                if not (x, -y) in grid_positions:
                    return x, -y

    def add(self, item, texture):
        x, y = self.findFreeSpot()

        icon = Draggable(
            parent=self,
            model='quad',
            scale_x=1 / self.texture_scale[0],
            scale_y=1 / self.texture_scale[1],
            texture=texture,
            color=color.white,
            origin=(-.5, .5),
            x=x * 1 / self.texture_scale[0],
            y=-y * 1 / self.texture_scale[1],
            scale=0.5,
            z=-1,
            name=item
        )
        self.list_icons.append(icon)
        name = item.title()
        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.color(0, 0, 0, .8)

        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z -= .01  # ensure the dragged item overlaps the rest

        def drop():
            icon.x = int((icon.x + (icon.scale_x / 2)) * 9) / 9
            icon.y = int((icon.y - (icon.scale_y / 2)))

            # если вытащили предмет за периметр инвентаря, вернуть в изначальное положение
            if icon.x < 0 or icon.y > 0 or icon.y <= -1:
                icon.position = icon.org_pos
                return

            for c in self.children:
                if c == icon:
                    continue
                if c.x == icon.x and c.y == icon.y:
                    print('swap positions')
                    c.position = icon.org_pos
                    self.list_icons[self.list_icons.index(c)], self.list_icons[self.list_icons.index(icon)] = \
                        self.list_icons[self.list_icons.index(icon)], self.list_icons[self.list_icons.index(c)]

        icon.drag = drag
        icon.drop = drop


def update():
    global pos
    if held_keys['1']:
        pos = 0
    if held_keys['2']:
        pos = 1
    if held_keys['3']:
        pos = 2
    if held_keys['4']:
        pos = 3

    inv.list_icons[pos].color = color.gray


if __name__ == "__main__":
    app = Ursina()
    inv = Inventory()
    inv.add("dirt", 'data/texture/base_texture/grass.png')
    inv.add("dirt", 'data/texture/base_texture/stone.png')
    inv.add("dirt", 'data/texture/base_texture/wool.png')

    inv.add("dirt", 'data/texture/base_texture/planks.png')
    app.run()
