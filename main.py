import math
import random
import pygame
import neat
from enum import Enum
from pygame import mixer


width = 1024
height = 720

score = 0

generation = 0
asteroid_speed = 15
total_asteroids = 5
score_speedup = 3
bullet_speed = 1

class PlayerState(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    
    
class Player:
    sprite = None
    image = None
    hitbox = None
    girlSprite = None
    girlImage = None
    girlHitbox = None
    state = PlayerState.UP
    bullets = []
    bulCool = 0
    cooldown = 10
    HP = 3
    HEAT = 0
    SCORE = 1000
    
    def __init__(self, x, y, i):
        self.sprite = pygame.image.load("img/Ship.png")
        self.hitbox = pygame.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())
        self.image = self.sprite
        self.girlSprite= pygame.image.load("img/Devuchki/{}.png".format(i))
        self.girlHitbox = pygame.Rect(800, i * 144, self.sprite.get_width(), self.sprite.get_height())
        self.girlImage = self.girlSprite

    def update(self):
        if self.HEAT > 0:
            self.HEAT -= 1
            
        if self.bulCool > 0:
            self.bulCool -=1
            
        if self.SCORE > 0:
            self.SCORE -=1
            
        if self.state == PlayerState.UP:
            self.hitbox.y += 3
        elif self.state == PlayerState.DOWN:
            self.hitbox.y -= 3
        elif self.state == PlayerState.LEFT:
            self.hitbox.x -= 3
        elif self.state == PlayerState.RIGHT:
            self.hitbox.x += 3
            
        if self.hitbox.x <= 0:
            self.hitbox.x = 0
        if self.hitbox.x >= 700:
            self.hitbox.x = 700
        if self.hitbox.y <= 0:
            self.hitbox.y = 0
        if self.hitbox.y >= 600:
            self.hitbox.y = 600

    def draw(self, screen, dopomine):
        screen.blit(self.image, (self.hitbox.x, self.hitbox.y))
        #screen.blit(self.girlImage, (self.girlHitbox.x, self.girlHitbox.y))
        #stats_font = pygame.font.SysFont("Roboto Condensed", 20)
        #labelhp = stats_font.render("HP: " + str(self.HP), True, (255, 255, 255))
        #labelhp_rect = labelhp.get_rect()
        #labelhp_rect.center = (self.girlHitbox.x + 136, self.girlHitbox.y+20)
        #screen.blit(labelhp, labelhp_rect)
        #labelht = stats_font.render("HEAT: " + str(self.HEAT), True, (255, 255, 255))
        #labelht_rect = labelht.get_rect()
        #labelht_rect.center = (self.girlHitbox.x + 136, self.girlHitbox.y+50)
        #screen.blit(labelht, labelht_rect)
        #labeldp = stats_font.render("Pts: " + str(dopomine), True, (255, 255, 255))
        #labeldp_rect = labeldp.get_rect()
        #labeldp_rect.center = (self.girlHitbox.x + 136, self.girlHitbox.y+80)
        #screen.blit(labeldp, labeldp_rect)
        #labelsc = stats_font.render("SCORE: " + str(self.SCORE), True, (255, 255, 255))
        #labelsc_rect = labelsc.get_rect()
        #labelsc_rect.center = (self.girlHitbox.x + 136, self.girlHitbox.y+110)
        #screen.blit(labelsc, labelsc_rect)
class Asteroid:
    image = None
    hitbox = None
    is_active = True

    def __init__(self, x, y):
        self.image = pygame.image.load("img/Asteroid.png")
        self.hitbox = self.image.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y - self.hitbox.height  # origin from bottom

    def update(self):
        self.hitbox.y += asteroid_speed
        
    def draw(self, scr):
        scr.blit(self.image, self.hitbox)

class Bullet:
    image = None
    hitbox = None
    is_active = True

    def __init__(self, x, y):
        self.image = pygame.image.load("img/bullet.png")
        self.hitbox = self.image.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y - self.hitbox.height  # origin from bottom

    def update(self):
        self.hitbox.y -= bullet_speed
        
    def draw(self, scr):
        scr.blit(self.image, self.hitbox)



def run_game(genomes, config):
    global score, asteroid, players, generation, asteroid_speed, score_speedup, total_asteroids, bullet_speed
    
    generation += 1
    asteroid_speed = 3
    score = 1
    score_speedup = 30
    asteroid = []
    players = []
    nets = []

    # init genomes
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0  # every genome is not successful at the start
        players.append(Player(280,470, (i%5)))
        
        
        
    # init
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    game_background = pygame.image.load("img/space.png")
    game_background2 = pygame.image.load("img/space.png")
    BGY1 = 0
    BGY2 = -1024
    mixer.music.load("src/Labyrinth-of-Time.mp3")
    mixer.music.play(-1)
# generate enemies
    heading_font = pygame.font.SysFont("Roboto Condensed", 70)
    asteroid.append(Asteroid(random.randint(10,30),random.randint(-600, 5)))
    asteroid.append(Asteroid(random.randint(10,690),random.randint(-650, -45)))
    asteroid.append(Asteroid(random.randint(10,690),random.randint(-700, -95)))
    asteroid.append(Asteroid(random.randint(10,690),random.randint(-650, -45)))
    asteroid.append(Asteroid(random.randint(660,690),random.randint(-700, -95)))   
    
    # the loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display bg & road
        screen.blit(game_background,(0,BGY1))
        screen.blit(game_background2,(0,BGY2))
        
        BGY1 +=1
        BGY2 +=1
        
        if BGY1 > 1024:
            BGY1 = -1024
        if BGY2 > 1024:
            BGY2 = -1024
        #print("score:{}".format(i))
        for player in players:
            player.update()
            
        # quit if there is no dinos left
        if len(players) == 0:
            break

        if score % score_speedup == 0:
            score = 1
            asteroid_speed += 3
            if asteroid_speed > 48:
                asteroid_speed = 48
            print("speed:{}".format(asteroid_speed))
            
        # draw enemies
        for i, ast in enumerate(asteroid):
            ast.update()
            if ast.hitbox.y >= 600:
                ast.hitbox.y = random.randint(-600, 5)
                ast.hitbox.x = random.randint(10,690)
                score +=1
            ast.draw(screen)
            for j, player in enumerate(players):
                player.draw(screen,genomes[j][1].fitness)
                
                if player.hitbox.colliderect(ast.hitbox):
                    genomes[j][1].fitness -= 3  # lower fitness (failed)
                    ast.hitbox.y = random.randint(-600, 5)
                    ast.hitbox.x = random.randint(10,690)
                    score += 1
                    player.HP -= 1
                if player.HEAT >= 120:
                    genomes[j][1].fitness -= 30  # lower fitness (failed)
                    players.pop(j)
                    genomes.pop(j)
                    nets.pop(j)
                if player.SCORE <= 0:
                    genomes[j][1].fitness -= 30  # lower fitness (failed)
                    players.pop(j)
                    genomes.pop(j)
                    nets.pop(j)
                if player.HP <= 0:
                    genomes[j][1].fitness -= 20  # lower fitness (failed)
                    players.pop(j)
                    genomes.pop(j)
                    nets.pop(j)
            for x, bul in enumerate(player.bullets):
                bul.update()
                if bul.hitbox.y <= 0:
                    player.bullets.pop(x)
                bul.draw(screen)
                for f, ast in enumerate(asteroid):
                    if ast.hitbox.colliderect(bul.hitbox):
                        ast.hitbox.y = random.randint(-600, 5)
                        ast.hitbox.x = random.randint(10,690)
                        try:
                            genomes[j][1].fitness += 20
                            player.bullets.pop(x)
                            player.SCORE += 500
                            score +=1
                        except IndexError:
                            print(":)")                        
                        
                    
                
        # display generation
        label = heading_font.render("Поколение: " + str(generation), True, (0, 72, 186))
        label_rect = label.get_rect()
        label_rect.center = (width / 2, 150)
        screen.blit(label, label_rect)
        
        cartext = heading_font.render("количество жертв: " + str(len(players)), True, (0, 36, 100))
        cartext_rect = label.get_rect()
        cartext_rect.center = (width / 4, 100)
        screen.blit(cartext, cartext_rect)
        # controls
        for i, player in enumerate(players):
            output = nets[i].activate([player.hitbox.x,
                                       player.hitbox.y,
                                       player.HP,
                                       player.HEAT,
                                       player.SCORE, 
                                       asteroid[0].hitbox.x,
                                       asteroid[0].hitbox.y,
                                       asteroid[1].hitbox.x,
                                       asteroid[1].hitbox.y,
                                       asteroid[2].hitbox.x,
                                       asteroid[2].hitbox.y,
                                       asteroid[3].hitbox.x,
                                       asteroid[3].hitbox.y,
                                       asteroid[4].hitbox.x,
                                       asteroid[4].hitbox.y,
                                       asteroid_speed])

            if output[0] > 0.5:
                 player.state = PlayerState.LEFT
            elif output[1] > 0.5:
                 player.state = PlayerState.RIGHT
            elif output[2] > 0.5:
                 player.state = PlayerState.UP
            elif output[3] > 0.5:
                 player.state = PlayerState.DOWN
            elif output[4] > 0.5:
                if player.bulCool == 0:
                    try:
                        genomes[j][1].fitness += 5
                    except IndexError:
                        print(":)")   
                    player.bullets.append(Bullet(player.hitbox.x + 32,player.hitbox.y))
                    player.HEAT += 25
                    player.bulCool = 15   
                 
       # flip & tick
        #clock.tick(600)  # fixed 60 fps
        pygame.display.flip()

if __name__ == "__main__":
    # setup config
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    # init NEAT
    #p = neat.checkpoint.Checkpointer.restore_checkpoint("./neat-checkpoint")
    p = neat.Population(config)
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    checkpointer = neat.Checkpointer(5000)
    p.add_reporter(checkpointer)

    # run NEAT
    winner = p.run(run_game, 5000)
    
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    
    if (checkpointer.last_generation_checkpoint >= 0) and (checkpointer.last_generation_checkpoint < 20):
        filename = 'neat-checkpoint-{0}'.format(checkpointer.last_generation_checkpoint)  
    
    
    
