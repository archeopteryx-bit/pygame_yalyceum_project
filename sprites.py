import pygame

back_home = pygame.image.load('Sprites\\Backgrounds\\background_home.jpg')
back_select_game = pygame.image.load('Sprites\\Backgrounds\\back.jpg')
event_img = pygame.image.load('Sprites\\Backgrounds\\event_back.png')

math_lvl1 = pygame.image.load('Sprites\\Cards\\math_card.jpg')
math_lvl2 = pygame.image.load('Sprites\\Cards\\math_card2.jpg')
math_lvl3 = pygame.image.load('Sprites\\Cards\\math_card3.jpg')

back_img = pygame.image.load('Sprites\\Buttons\\back.png')
replay_img = pygame.image.load('Sprites\\Buttons\\replay.png')
bowl_img = pygame.image.load('Sprites\\Buttons\\bowl.png')
math_image = pygame.image.load('Sprites\\Buttons\\math.png')
math_image_mouse = pygame.image.load('Sprites\\Buttons\\math_mouse.png')
rus_image = pygame.image.load('Sprites\\Buttons\\rus.png')
rus_image_mouse = pygame.image.load('Sprites\\Buttons\\rus_mouse.png')
home_image = pygame.image.load('Sprites\\Buttons\\home.png')
home_image_mouse = pygame.image.load('Sprites\\Buttons\\home_mouse.png')
shop_image = pygame.image.load('Sprites\\Buttons\\shop.png')
shop_image_mouse = pygame.image.load('Sprites\\Buttons\\shop_mouse.png')
easy_lvl = pygame.image.load('Sprites\\Buttons\\easy.png')
easy_lvl_mouse = pygame.image.load('Sprites\\Buttons\\easy_mouse.png')
normal_lvl = pygame.image.load('Sprites\\Buttons\\normal.png')
normal_lvl_mouse = pygame.image.load('Sprites\\Buttons\\normal_mouse.png')
hard_lvl = pygame.image.load('Sprites\\Buttons\\hard.png')
hard_lvl_mouse = pygame.image.load('Sprites\\Buttons\\hard_mouse.png')
eraser_img = pygame.image.load('Sprites\\Buttons\\eraser.png')

gcat_s1 = pygame.image.load('Sprites\\Animals\\gcat_stay1.png')
gcat_s2 = pygame.image.load('Sprites\\Animals\\gcat_stay2.png')
gcat_s3 = pygame.image.load('Sprites\\Animals\\gcat_stay3.png')
gcat_s4 = pygame.image.load('Sprites\\Animals\\gcat_stay4.png')
cat_food = pygame.image.load('Sprites\\Animals\\cat_food.png')
gcat_sprites = [gcat_s1, gcat_s2, gcat_s3, gcat_s4]

dhdog_s1 = pygame.image.load('Sprites\\Animals\\dhdog_stay1.png')
dhdog_s2 = pygame.image.load('Sprites\\Animals\\dhdog_stay2.png')
dhdog_s3 = pygame.image.load('Sprites\\Animals\\dhdog_stay3.png')
dhdog_s4 = pygame.image.load('Sprites\\Animals\\dhdog_stay4.png')
dhdog_s5 = pygame.image.load('Sprites\\Animals\\dhdog_stay5.png')
dog_food = pygame.image.load('Sprites\\Animals\\cat_food.png')
dhdog_sprites = [dhdog_s1, dhdog_s2, dhdog_s3, dhdog_s4, dhdog_s5]

nmcat_s1 = pygame.image.load('Sprites\\Animals\\nmcat_stay1.png')
nmcat_s2 = pygame.image.load('Sprites\\Animals\\nmcat_stay2.png')
nmcat_s3 = pygame.image.load('Sprites\\Animals\\nmcat_stay3.png')
nmcat_sprites = [nmcat_s1, nmcat_s2, nmcat_s3]

animal_sprites_dict = {'gcat': gcat_sprites,
                       'dhdog': dhdog_sprites,
                       'nmcat': nmcat_sprites}

shop_animal = [(gcat_s1, 'gcat'),
               (dhdog_s1, 'dhdog'),
               (nmcat_s1, 'nmcat')]
shop_food = [(cat_food, 1), (dog_food, 2)]
