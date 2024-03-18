import string

from ursina.prefabs.first_person_controller import FirstPersonController

from inventory import *
from perlinNoise import *

app = Ursina()

# Загрузка звуков блоков
blockBreakStone = Audio('data/audio/stone.wav', loop=False, autoplay=False)
blockBreakDirt = Audio('data/audio/grass.wav', loop=False, autoplay=False)
blockBreakWood = Audio('data/audio/wood.wav', loop=False, autoplay=False)
blockBreakGlass = Audio('data/audio/glass.wav', loop=False, autoplay=False)
blockBreakWool = Audio('data/audio/wool.wav', loop=False, autoplay=False)

# Загрузка текстур
path = 'data/texture/expand_texture/'
pathForInv = 'data/texture/base_texture/'

order_blocks = [
    'stone_bricks',
    'grass',
    'planks',
    'bricks',
    'glass',
    'stone',
    'log',
    'wool']

textureListInv = [
    load_texture(f'{pathForInv}{order_blocks[0]}.png'),
    load_texture(f'{pathForInv}{order_blocks[1]}.png'),
    load_texture(f'{pathForInv}{order_blocks[2]}.png'),
    load_texture(f'{pathForInv}{order_blocks[3]}.png'),
    load_texture(f'{pathForInv}{order_blocks[4]}.png'),
    load_texture(f'{pathForInv}{order_blocks[5]}.png'),
    load_texture(f'{pathForInv}{order_blocks[6]}.png'),
    load_texture(f'{pathForInv}{order_blocks[7]}.png')]

texture_list = [(load_texture(f'{path}{order_blocks[0]}.png'), blockBreakStone),
                (load_texture(f'{path}{order_blocks[1]}.png'), blockBreakDirt),
                (load_texture(f'{path}{order_blocks[2]}.png'), blockBreakWood),
                (load_texture(f'{path}{order_blocks[3]}.png'), blockBreakStone),
                (load_texture(f'{path}{order_blocks[4]}.png'), blockBreakGlass),
                (load_texture(f'{path}{order_blocks[5]}.png'), blockBreakStone),
                (load_texture(f'{path}{order_blocks[6]}.png'), blockBreakWood),
                (load_texture(f'{path}{order_blocks[7]}.png'), blockBreakWool)]

hand_texture = load_texture('data/model/hand/arm_texture.png')
sky_texture = load_texture('data/texture/skybox.png')
pickaxe = load_texture('data/texture/Diffuse.png')

block_num = 0
pos = 0
w = 0


def update():
    global block_num, pos, w
    list_icons = [i.name for i in inv.list_icons]
    for i in range(len(list_icons)):
        for j in range(len(list_icons)):
            if i == j and order_blocks[i] != list_icons[i]:
                index1 = i
                index2 = list_icons.index(order_blocks[i])
                order_blocks[index1], order_blocks[index2] = order_blocks[index2], order_blocks[index1]
                texture_list[index1], texture_list[index2] = texture_list[index2], texture_list[index1]

    if held_keys['control'] and held_keys['s']:
        if not isLoaded:
            return
        print("************************************")
        file_name = 'data/map/' + file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('')
            f.close()
        for i in scene.entities:
            if i.name == 'block':
                print(i.position, i.nameBlock)
                with open(file_name, 'a', encoding='utf-8') as f:
                    f.write(str(i.position) + ";" + str(i.nameBlock) + "\n")
                    f.close()
    # творческий режим
    # if held_keys['c']:
    # 	creativeMode()
    # elif held_keys['v']:
    # 	destroy(ec)

    # вход в инвентарь
    if held_keys['i']:
        mouse.locked = False
    # w = WindowPanel(
    # 	title='Custom Window',
    # 	content=(
    # 		Text('Name:'),
    # 		InputField(name='name_field'),
    # 		Button(text='Submit', color=color.azure),
    # 	),
    # )
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

    # TODO: исправить проблему со скоростью
    # управление приседанием персонажа при нажатии Ctrl
    if held_keys['left control']:
        player.camera_pivot.y = 1.4
        player.speed = 3.5
    else:
        player.camera_pivot.y = 1.8
        player.speed = 5

    # управление скоростью персонажа при нажатии Shift
    if held_keys['left shift']:
        player.speed = 10
    else:
        player.speed = 5

    # выбор блока
    for val, key in held_keys.items():
        if key == 1:
            if val in list('123456789'):
                block_num = pos = int(val) - 1

    # выделение белым/серым цветом ячеек инвентаря
    for i in range(len(inv.list_icons)):
        try:
            inv.list_icons[i].color = color.white
            inv.list_icons[pos].color = color.gray
        except:
            inv.list_icons[i].color = color.white


class Block(Button):
    def __init__(self, position=(0, 0, 0), model='data/model/block/block', texture=texture_list[block_num][0], scale=1,
                 nameBlock=order_blocks[block_num], colorB=color.color(0, 0, random.uniform(.9, 1.0))):
        super().__init__(
            parent=scene,
            position=position,
            model=model,
            origin_y=.5,
            texture=texture,
            color=colorB,
            scale=scale,
        )
        self.nameBlock = nameBlock

    def input(self, key):
        if self.hovered:
            # проверка на расстояние между нажатым блоком и player ( если меньше {6}, то можно поставить блок
            checking = sqrt((int(self.position.x) - int(player.position.x)) ** 2 + (
                (int(self.position.z) - int(player.position.z))) ** 2) <= 10

            if key == 'right mouse down':
                # TODO: добавить лестниу (уже добавлена, но надо улучшить)
                # Block(position=self.position + mouse.normal, model='data/model/stairs/stairs',
                # 	  texture=load_texture('data/model/stairs/east.png'))
                if block_num in range(0, len(texture_list)) and checking:
                    if order_blocks[block_num] == 'glass':
                        blockBreakStone.play()
                    else:
                        texture_list[block_num][1].play()
                    Block(position=self.position + mouse.normal, texture=texture_list[block_num][0],
                          nameBlock=order_blocks[block_num])
            if key == 'left mouse down' and checking:
                try:
                    texture_list[order_blocks.index(self.nameBlock)][1].play()
                except:
                    pass
                if self.y > 0:
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
            model='data/model/block/block',
            texture=texture_list[block_num][0],
            scale=0.4,
            position=Vec2(self.pos_x, self.pos_y),
        )

    def setBlock(self, texture):
        try:
            self.model = 'data/model/block/block'
            self.texture = texture
            self.scale = 0.4
            self.position = Vec2(self.pos_x, self.pos_y)
        except Exception as e:
            print(e)

    def setTool(self):
        try:
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
            self.rotation = Vec3(-45, -20, 0)
        else:
            self.position = Vec2(self.pos_x - self.d_x / 2, self.pos_y + self.d_y)
            self.rotation = Vec3(60, 20, 40)

    def passive(self):
        if block_num in range(0, len(texture_list)):
            self.position = Vec2(self.pos_x, self.pos_y)
            self.rotation = Vec3(-45, -20, 0)
        else:
            self.position = Vec2(self.pos_x, self.pos_y)
            self.rotation = Vec3(60, 20, 45)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=600,
            double_sided=True)


def init_param():
    window.borderless = False
    window.vsync = False
    window.title = "Minecraft"
    window.exit_button.visible = False


# window.fullscreen = True


# TODO: доделать нормальный креатив
def creativeMode():
    EditorCamera()


def genWorldName(size=10):
    # count = 0
    # with open('data/map/worldInfo.txt', 'a', encoding='utf-8') as f:
    # 	for i in f:
    # 		count = i
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))


isLoaded = False


def loadMapFromFile(fileName):
    global isLoaded
    isLoaded = True
    with open('data/map/' + fileName, 'r', encoding='utf-8') as f:
        for row in f:
            # print(tuple(map(int, i[5:-2].replace('\n', '').split(','))))
            data = row.split(';')
            i = data[0]
            textureName = data[1].replace('\n', '')
            if textureName == 'main':
                textureName = 'grass'
            textureBlock = texture_list[order_blocks.index(textureName)][0]
            position = tuple(map(int, i[5:-1].replace(' ', '').split(',')))
            Block(position=position,
                  texture=textureBlock,
                  model=model,
                  nameBlock=textureName)
        f.close()


if __name__ == "__main__":
    init_param()
    size_y = 32
    size_x = 32

    textureGrass = load_texture('data/texture/expand_texture/grass.png')
    model = 'data/model/block/block'

    map1 = perlinNoise()
    map2 = perlinNoise()


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


    listMap = os.listdir('data/map')

    heightOfTransparentBlocks = 3
    # for y in range(size_y):
    # 	for x in range(size_x):
    # Block(position=(x, 0, y),
    # 	  texture=textureGrass,
    # 	  model=model,
    # 	  nameBlock='main')
    # if map1[y][x] == '#':
    # 	Block(position=(x, 1, y),
    # 		  model=model,
    # 		  texture=textureGrass,
    # 		  nameBlock='grass', )
    # if map2[y][x] == '#' and map1[y][x] == "#" and checkNear(map1, y, x):
    # 	Block(position=(x, 2, y),
    # 		  model=model,
    # 		  texture=textureGrass,
    # 		  nameBlock='grass')
    # if y == size_y - 1:
    # 	[Block(model='cube', position=(x, i, y + 1), colorB=color.rgba(0, 0, 0, 0)) for i in range(heightOfTransparentBlocks)]
    # elif y == 0:
    # 	[Block(model='cube', position=(x, i, y - 1), colorB=color.rgba(0, 0, 0, 0)) for i in range(heightOfTransparentBlocks)]
    # if x == size_x - 1:
    # 	[Block(model='cube', position=(x + 1, i, y), colorB=color.rgba(0, 0, 0, 0)) for i in range(heightOfTransparentBlocks)]
    # elif x == 0:
    # 	[Block(model='cube', position=(x - 1, i, y), colorB=color.rgba(0, 0, 0, 0)) for i in range(heightOfTransparentBlocks)]

    inv = Inventory()
    inv.fillInv(order_blocks, textureListInv)

    player = FirstPersonController()
    cursorTexture = load_texture('data/texture/cursor.png')
    destroy(player.cursor)
    player.cursor = Entity(parent=camera.ui, model='quad', scale=.03, texture=cursorTexture,
                           position_z=-0.01)
    player.position = (5, 0, 5)
    player.mouse_sensitivity = Vec2(50, 50)
    player.jump_duration = 0.25
    player.jump_height = 1.5

    file = listMap[0]  # стандартная карта
    loadMapFromFile(file)

    hand = Hand()
    sky = Sky()
    fileName = 'data/map/' + genWorldName()
    app.run()
