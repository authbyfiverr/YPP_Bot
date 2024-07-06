import cv2
import numpy as np
import pyautogui
import os

screenshot_path = 'screenshot.png'


# Function to load target images from a folder into memory
def load_target_images_from_folder(folder_path='targets'):
    target_images = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                path = os.path.join(folder_path, filename)
                target_images[filename] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    except Exception as e:
        print(f'Failed to load images from folder {folder_path}: {e}')
    return target_images


def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        return screenshot_gray
    except Exception as e:
        print(f'An error has occurred: {e}')
        return None

def save_image(screenshot, file_path):
    try:
        cv2.imwrite(file_path, screenshot)
        print(f"Image saved successfully as {file_path}")
    except Exception as e:
        print(f"An error occurred while saving image: {e}")




# Function to locate an object on screen and return coordinates
def find_target_on_screenshot(target_image, screenshot, threshold=0.8, center=True):
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        target_height, target_width = target_image.shape
        if center:
            return max_loc[0] + target_width // 2, max_loc[1] + target_height // 2
        else:
            return max_loc[0], max_loc[1]
    else:
        return False

def find_all_targets_on_screenshot(target_image, screenshot, threshold=0.8, center=True):
    # Apply template matching
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)

    # Get the dimensions of the target image
    target_height, target_width = target_image.shape

    # Find all locations where the match value exceeds the threshold
    match_locations = np.where(result >= threshold)

    # Initialize a list to store the match coordinates
    matches = []

    for (x, y) in zip(match_locations[1], match_locations[0]):
        if center:
            match_x = x + target_width // 2
            match_y = y + target_height // 2
        else:
            match_x = x
            match_y = y
        matches.append((match_x, match_y))

    return matches

# Takes screenshot, finds and crops YPP window, returning cropped image or original image if exception
def crop_screenshot_to_ypp(screenshot):
    try:
        anchor_coordinates = determine_ypp_window_anchor_coordinates(screenshot)

        if not anchor_coordinates:
            print('crop_screenshot_to_ypp: YPP anchor not found, image not cropped.')
            return screenshot

        window_height = 790
        window_width = 1000

        x2, y2 = anchor_coordinates[0] + window_width, anchor_coordinates[1] + window_height

        cropped_screenshot = screenshot[anchor_coordinates[1]:y2, anchor_coordinates[0]:x2]
        return cropped_screenshot
    except Exception as e:
        print(f'An error has occured: {e}')
        return screenshot

target_images = load_target_images_from_folder()

def determine_ypp_window_anchor_coordinates(screenshot):
    return find_target_on_screenshot(target_images['puzzle_pirates_top_left_window_icon_and_text.png'], screenshot, threshold=0.90, center=False)
