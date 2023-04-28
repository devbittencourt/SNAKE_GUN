import pygame, sys, random, asyncio
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
life_font = pygame.font.Font(None, 40)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 25
number_of_cells = 20

OFFSET = 75

class Food:
	def __init__(self, snake_body):
		self.position = self.generate_random_pos(snake_body)

		self.speed = 0.3 
		
	
	def updatefood(self, snake_body):
		self.position.y += self.speed
		if self.position.y > number_of_cells-1:
			self.position = self.generate_random_pos(snake_body)
			game.game_over()
			
	
	def draw(self):
		food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
			cell_size, cell_size)
		screen.blit(food_surface, food_rect)

	

	def generate_random_cell(self):
		x = random.randint(0, number_of_cells-7)
		y = random.randint(0, number_of_cells-7)
		return Vector2(x, y)

	def generate_random_pos(self, snake_body):
		position = self.generate_random_cell()
		while position in snake_body:
			position = self.generate_random_cell()
		return position

class Projetil:
	def __init__(self, snake_body):
		self.speed = -1.5 
		self.position = Vector2()
		
		
        
		
	def spawn_proj(self, snake_body,proj_list):
		proj = Projetil(snake_body)
		proj.position = snake_body[0].copy()
		proj_list.append(proj)

	def updateproj(self, proj_list ):
		new_proj_list = []
		for proj in proj_list:
			proj.position.y += self.speed
			game.pos = proj.position.y
			if proj.position.y < -0.4:
				continue  # Skip adding the projectile to the new list
			new_proj_list.append(proj)
		proj_list.clear()  # Clear the original proj_list
		proj_list.extend(new_proj_list)
				
			
	
	def draw(self):
		proj_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
			cell_size, cell_size)
		screen.blit(projetil_surface, proj_rect)

	

	

class Snake:
	def __init__(self):
		self.body = [Vector2(6, 19), Vector2(5,19), Vector2(4,19),Vector2(3,19),Vector2(2,19)]
		self.direction = Vector2(1, 0)
		self.add_segment = False
		

	def draw(self):
		for segment in self.body[:-1]:
			segment_rect = (OFFSET + segment.x * cell_size, OFFSET+ segment.y * cell_size, cell_size, cell_size)
			pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

	def update(self):
		self.body.insert(0, self.body[0] + self.direction)
		if self.add_segment == True:
			self.add_segment = False
		else:
			self.body = self.body[:-1]

	def reset(self):
		self.body = [Vector2(6, 19), Vector2(5,19), Vector2(4,19),Vector2(3,19),Vector2(2,19)]
		self.direction = Vector2(1, 0)

class Game:
	def __init__(self):
		self.snake = Snake()
		self.projetil= Projetil(self.snake.body)
		self.food_list = []
		self.proj_list = [] 
		self.score=0 
		self.pos=1
		for i in range(6):    
			self.food_list.append(Food(self.snake.body))
		self.state = "RUNNING"
		

	def draw(self):
		for food in self.food_list:  
			food.draw()
		for proj in self.proj_list:  # Desenha todos os projéteis na lista proj_list
			proj.draw()
		self.snake.draw()

	def update(self):
		if self.state == "RUNNING":
			self.snake.update()
			for food in self.food_list:  
				self.check_collision_with_food(food)
				food.updatefood(self.snake.body)
				 
				self.check_collision_with_projetil(food)

			self.check_collision_with_edges()
			self.lensnake()
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				self.spawn_proj()
			self.projetil.updateproj(self.proj_list)
			self.draw()
			

	def spawn_proj(self):
		self.projetil.spawn_proj(self.snake.body, self.proj_list) 

	
	def check_collision_with_projetil(self,food, error_margin=0.9):
		for projetil in self.proj_list: 
			if (
				abs(projetil.position.x - food.position.x) <= error_margin
				and abs(projetil.position.y - food.position.y) <= error_margin
			):
				self.proj_list.remove(projetil)  # Remove o projetil da lista proj_list
				self.food_list.remove(food)  # Remove o food da lista food_list
				self.food_list.append(Food(self.snake.body))
				self.score +=1
				break  


	def check_collision_with_food(self, food, error_margin=0.5):
		for segment in self.snake.body:
			if (
				abs(segment.x - food.position.x) <= error_margin
				and abs(segment.y - food.position.y) <= error_margin
			):
				game.game_over()

	def check_collision_with_edges(self):
		if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
			self.game_over()
		if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
			self.game_over()

	
	def lensnake(self):
		if len(self.snake.body) < 2:
			self.game_over()

	

	def game_over(self):
		self.snake.reset()
		self.food_list[0].position = self.food_list[0].generate_random_pos(self.snake.body)
		self.proj_list.clear()
		self.score=0
		self.state = "STOPPED"
		
		
		

screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("Graphics/food.png")
projetil_surface = pygame.image.load("Graphics/projetil.png")


SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200) 	

async def main():
	while True:
		for event in pygame.event.get():
			if event.type == SNAKE_UPDATE:
				game.update()
			
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if game.state == "STOPPED":
					game.state = "RUNNING"
				if event.key == pygame.K_UP: 
					game.snake.direction = Vector2(0, -1)
				if event.key == pygame.K_DOWN: 
					game.snake.direction = Vector2(0, 1)
				if event.key == pygame.K_LEFT: 
					game.snake.direction = Vector2(-1, 0)
				if event.key == pygame.K_RIGHT: 
					game.snake.direction = Vector2(1, 0)
				if event.key == pygame.K_SPACE:
					game.spawn_proj()

		#Drawing
		screen.fill(GREEN)
		pygame.draw.rect(screen, DARK_GREEN, 
			(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
		game.draw()
		title_surface = title_font.render("SNAKE GUN", True, DARK_GREEN)
		score_surface = title_font.render("SCORE", True, DARK_GREEN)
		life_surface = title_font.render(str(game.score), True, DARK_GREEN)
		move_surface = life_font.render("MOVE:< ^ v > space", True, DARK_GREEN)

		screen.blit(title_surface, (OFFSET-5, 20))
		screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))
		screen.blit(life_surface, (OFFSET +150, OFFSET + cell_size*number_of_cells +10))
		screen.blit(move_surface, (OFFSET +230, OFFSET + cell_size*number_of_cells +10))
		pygame.display.update()
		clock.tick(60)
		await asyncio.sleep(0)

asyncio.run(main())		