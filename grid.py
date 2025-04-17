import pygame

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for c in range(self.num_cols)] for r in range(self.num_rows)]
        self.colors = {
            0: (44, 44, 127),    # Empty cell (dark blue)
            1: (0, 240, 240),    # Cyan (I)
            2: (240, 240, 0),    # Yellow (O)
            3: (240, 160, 0),    # Orange (L)
            4: (0, 0, 240),      # Blue (J)
            5: (0, 240, 0),      # Green (S)
            6: (240, 0, 0),      # Red (Z)
            7: (160, 0, 240)     # Purple (T)
        }
        self.score = 0
        self.level = 1

    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                cell_color = self.colors[cell_value]
                pygame.draw.rect(
                    screen,
                    cell_color,
                    (col * self.cell_size, row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                )

    def is_inside(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def is_empty(self, row, col):
        return self.grid[row][col] == 0

    def is_row_full(self, row):
        return all(self.grid[row][col] != 0 for col in range(self.num_cols))

    def clear_row(self, row):
        for col in range(self.num_cols):
            self.grid[row][col] = 0

    def move_row_down(self, row, num_rows):
        for col in range(self.num_cols):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
                for r in range(row - 1, 0, -1):
                    self.move_row_down(r, 1)
        
        # Update score based on number of rows cleared
        if completed == 1:
            self.score += 100 * self.level
        elif completed == 2:
            self.score += 300 * self.level
        elif completed == 3:
            self.score += 500 * self.level
        elif completed == 4:
            self.score += 800 * self.level

        # Update level every 10 rows cleared
        self.level = (self.score // 1000) + 1
        
        return completed

    def reset(self):
        self.grid = [[0 for c in range(self.num_cols)] for r in range(self.num_rows)]
        self.score = 0
        self.level = 1
        
