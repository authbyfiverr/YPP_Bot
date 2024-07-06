import pyautogui
import cv2
import numpy as np
import agentVision

class GameBoard:
    def __init__(self, board):
        self.board = board  # 2D list representing the board

    def evaluate_board(self):
        score = 0
        strikes = self.identify_strikes()

        for strike in strikes:
            size = len(strike)
            if 4 <= size <= 9:  # Example size range
                score += size ** 2
            elif size > 9:
                score -= size  # Penalize oversized strikes

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board[row][col] is not None and "breaker" in self.board[row][col].block_type:
                    adjacent_strikes = self.count_adjacent_strikes(row, col)
                    score += adjacent_strikes * 10  # Arbitrary value for demonstration
                    if adjacent_strikes > 1:
                        score += (adjacent_strikes - 1) * 5  # Bonus for multiple adjacent strikes

        return score

    def identify_strikes(self):
        visited = set()
        strikes = []

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if (row, col) not in visited and self.board[row][col] is not None and "solid" in self.board[row][
                    col].block_type:
                    strike = self.flood_fill(row, col, self.board[row][col].color)
                    strikes.append(strike)
                    visited.update(strike)

        return strikes

    def flood_fill(self, row, col, color):
        stack = [(row, col)]
        strike = set()

        while stack:
            r, c = stack.pop()
            if (r, c) in strike or r < 0 or r >= BOARD_HEIGHT or c < 0 or c >= BOARD_WIDTH:
                continue
            if self.board[r][c] is None or self.board[r][c].color != color:
                continue
            strike.add((r, c))
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

        return strike

    def count_adjacent_strikes(self, row, col):
        adjacent_strikes = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_HEIGHT and 0 <= c < BOARD_WIDTH and self.board[r][c] is not None and "solid" in \
                    self.board[r][c].block_type:
                adjacent_strikes += 1
        return adjacent_strikes


# Define constants
BOARD_WIDTH = 6
BOARD_HEIGHT = 13


# Example main function to demonstrate usage
def main():
    # Example game board
    board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    game_board = GameBoard(board)

    # Example evaluation
    score = game_board.evaluate_board()
    print(f"Board score: {score}")


if __name__ == "__main__":
    main()

# Coordinates of the pixels to sample from ypp cropped screenshot
#sf_tile_x_coords = [195, 229, 260, 296, 330, 364]
#sf_tile_y_coords = [141, 191, 241, 291, 341, 391, 441, 491, 541, 591, 641, 691, 741]

sf_tile_x_coords = [192, 226, 260, 294, 327, 361]
sf_tile_y_coords = [141, 191, 241, 291, 341, 391, 441, 491, 541, 591, 641, 691, 741]


def sample_pixels(screenshot, x_coords, y_coords):
    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)

    # List to hold the sampled values
    sampled_values = []

    # Sample the specified pixels
    for y in y_coords:
        for x in x_coords:
            # Get grayscale value
            bw = screenshot_np[y, x]
            sampled_values.append({'x': x, 'y': y, 'bw': bw})

    return sampled_values

def print_sampled_values_grid(sampled_values, x_coords, y_coords):
    # Create a dictionary for quick lookup
    value_dict = {(v['x'], v['y']): v for v in sampled_values}

    # Print the grid
    for y in y_coords:
        row_bw = []
        for x in x_coords:
            value = value_dict[(x, y)]
            bw_str = f"BW: {value['bw']}"
            row_bw.append(bw_str)
        print(" | ".join(row_bw))
        print("-" * 80)  # Separator for rows

def assign_names_to_values(sampled_values, names_dict):
    # Assign names to the values
    for value in sampled_values:
        coord = (value['x'], value['y'])
        if coord in names_dict:
            value['name'] = names_dict[coord]
        else:
            value['name'] = None
    return sampled_values

def print_named_sampled_values_grid(sampled_values, x_coords, y_coords):
    # Create a dictionary for quick lookup
    value_dict = {(v['x'], v['y']): v for v in sampled_values}

    # Print the grid with names
    for y in y_coords:
        row = []
        for x in x_coords:
            value = value_dict[(x, y)]
            if value['name']:
                row.append(f"{value['name']}: RGB {value['rgb']}, BW {value['bw']}")
            else:
                row.append(f"RGB {value['rgb']}, BW {value['bw']}")
        print(" | ".join(row))
        print("-" * 80)  # Separator for rows

def sample_pixels_around_center(screenshot, center_x, center_y, grid_size_x=3, grid_size_y=3):
    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)

    # Calculate the grid half-sizes (how far from center)
    grid_half_size_x = grid_size_x // 2
    grid_half_size_y = grid_size_y // 2

    # Define boundaries for the grid around the center
    x_start = max(0, center_x - grid_half_size_x)
    x_end = min(screenshot_np.shape[1], center_x + grid_half_size_x + 1)
    y_start = max(0, center_y - grid_half_size_y)
    y_end = min(screenshot_np.shape[0], center_y + grid_half_size_y + 1)

    # Slice the region of interest from the screenshot
    region_of_interest = screenshot_np[y_start:y_end, x_start:x_end]

    # Calculate average grayscale value for the region
    average_bw = int(np.mean(region_of_interest))

    return {
        'x': center_x,
        'y': center_y,
        'bw': average_bw
    }

def sample_pixels_around_centers(screenshot, x_coords, y_coords, grid_size_x=0, grid_size_y=0):
    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)

    # List to hold the sampled values
    sampled_values = []

    # Sample the specified pixels
    for y in y_coords:
        for x in x_coords:
            result = sample_pixels_around_center(screenshot_np, x, y, grid_size_x, grid_size_y)
            sampled_values.append(result)

    return sampled_values


def add_dots_and_save(screenshot, x_coords, y_coords):
    # Convert the screenshot to a numpy array if not already
    if isinstance(screenshot, np.ndarray):
        image_with_dots = screenshot
    else:
        image_with_dots = np.array(screenshot)

    # Add black dots to the intersection points
    for y in y_coords:
        for x in x_coords:
            cv2.circle(image_with_dots, (x, y), 1, (0, 0, 0), -1)

    # Save the image with dots
    agentVision.save_image(image_with_dots, 'dots.png')

def add_dots_and_save_2(screenshot, coordinates):
    # Convert the screenshot to a numpy array if not already
    if isinstance(screenshot, np.ndarray):
        image_with_dots = screenshot
    else:
        image_with_dots = np.array(screenshot)

    # Add black dots to the coordinates
    for (x, y) in coordinates:
        cv2.circle(image_with_dots, (x, y), 5, (0, 0, 0), -1)

    # Save the image with dots
    agentVision.save_image(image_with_dots, 'dots.png')