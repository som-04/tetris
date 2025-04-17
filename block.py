import pygame
import random

class Block:
    def __init__(self):
        self.id = random.randint(1, 7)
        self.cells = {
            1: [(0, 0), (0, 1), (0, 2), (0, 3)],  # I
            2: [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
            3: [(0, 1), (1, 1), (2, 1), (2, 0)],  # L
            4: [(0, 0), (1, 0), (2, 0), (2, 1)],  # J
            5: [(0, 1), (1, 0), (1, 1), (2, 0)],  # S
            6: [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
            7: [(0, 1), (1, 0), (1, 1), (1, 2)]   # T
        }
        self.row_offset = 0
        self.col_offset = 4
        self.rotation_state = 0

    def move(self, rows, cols):
        self.row_offset += rows
        self.col_offset += cols

    def get_cell_positions(self):
        tiles = self.cells[self.id]
        moved_tiles = []
        for position in tiles:
            moved_tiles.append((
                position[0] + self.row_offset,
                position[1] + self.col_offset
            ))
        return moved_tiles

    def rotate(self, grid):
        if self.id == 2:  # O piece doesn't rotate
            return

        # Store current position
        current_rotation = self.rotation_state
        current_cells = self.cells[self.id]
        
        # Rotate
        rotated = []
        for position in current_cells:
            rotated.append((-position[1], position[0]))
        
        self.cells[self.id] = rotated
        self.rotation_state = (self.rotation_state + 1) % 4

        # Wall kick tests
        if not self.can_move(grid, 0, 0):
            # Try moving right
            self.col_offset += 1
            if not self.can_move(grid, 0, 0):
                # Try moving left
                self.col_offset -= 2
                if not self.can_move(grid, 0, 0):
                    # Try moving up
                    self.col_offset += 1
                    self.row_offset -= 1
                    if not self.can_move(grid, 0, 0):
                        # Revert all changes
                        self.cells[self.id] = current_cells
                        self.rotation_state = current_rotation

    def can_move(self, grid, rows, cols):
        for position in self.get_cell_positions():
            new_row = position[0] + rows
            new_col = position[1] + cols
            if not grid.is_inside(new_row, new_col) or not grid.is_empty(new_row, new_col):
                return False
        return True

    def draw(self, screen, grid):
        for position in self.get_cell_positions():
            pygame.draw.rect(
                screen,
                grid.colors[self.id],
                (position[1] * grid.cell_size, 
                 position[0] * grid.cell_size,
                 grid.cell_size - 1, 
                 grid.cell_size - 1)
            )

    def reset(self):
        self.row_offset = 0
        self.col_offset = 4
        self.rotation_state = 0
        self.id = random.randint(1, 7)

