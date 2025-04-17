import pygame
import sys
from grid import Grid
from block import Block

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Tetris")
        
        self.grid = Grid()
        self.block = Block()
        self.next_block = Block()
        
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.game_over = False
        self.paused = False
        
        # Colors
        self.dark_blue = (44, 44, 127)
        self.white = (255, 255, 255)
        
        # Font
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Game state
        self.game_over = False
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_LEFT and self.block.can_move(self.grid, 0, -1):
                        self.block.move(0, -1)
                    if event.key == pygame.K_RIGHT and self.block.can_move(self.grid, 0, 1):
                        self.block.move(0, 1)
                    if event.key == pygame.K_DOWN and self.block.can_move(self.grid, 1, 0):
                        self.block.move(1, 0)
                    if event.key == pygame.K_UP:
                        self.block.rotate(self.grid)
                    if event.key == pygame.K_SPACE:
                        while self.block.can_move(self.grid, 1, 0):
                            self.block.move(1, 0)
                            
                if event.key == pygame.K_r:
                    self.reset_game()
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def update(self):
        if self.game_over or self.paused:
            return

        # Calculate fall speed based on level
        # Reduced base speed from 500 to 300 and increased level multiplier from 20 to 30
        fall_speed = max(30, 100 - (self.grid.level * 30))
        
        self.fall_time += self.clock.get_rawtime()
        if self.fall_time >= fall_speed:
            if self.block.can_move(self.grid, 1, 0):
                self.block.move(1, 0)
            else:
                # Lock the block in place
                for pos in self.block.get_cell_positions():
                    if pos[0] <= 0:  # Game over if block locks at top
                        self.game_over = True
                        return
                    self.grid.grid[pos[0]][pos[1]] = self.block.id
                
                # Clear full rows and update score
                self.grid.clear_full_rows()
                
                # Create new block
                self.block = self.next_block
                self.next_block = Block()
            
            self.fall_time = 0

    def draw(self):
        self.screen.fill(self.dark_blue)
        
        # Draw game grid
        self.grid.draw(self.screen)
        
        # Draw current block
        self.block.draw(self.screen, self.grid)
        
        # Draw UI
        score_text = self.font.render(f'Score: {self.grid.score}', True, self.white)
        level_text = self.font.render(f'Level: {self.grid.level}', True, self.white)
        
        self.screen.blit(score_text, (320, 50))
        self.screen.blit(level_text, (320, 100))
        
        # Draw next block preview
        next_text = self.font.render('Next:', True, self.white)
        self.screen.blit(next_text, (320, 200))
        
        # Draw game over text
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to restart', True, self.white)
            self.screen.blit(game_over_text, (320, 400))
        
        # Draw pause text
        if self.paused:
            pause_text = self.font.render('PAUSED', True, self.white)
            self.screen.blit(pause_text, (320, 300))
        
        pygame.display.update()

    def reset_game(self):
        self.grid.reset()
        self.block = Block()
        self.next_block = Block()
        self.game_over = False
        self.paused = False
        self.fall_time = 0

    def run(self):
        while True:
            self.clock.tick(60)
            self.handle_input()
            self.update()
            self.draw()

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
        pygame.quit()
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
