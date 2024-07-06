import random
from humancursor import SystemCursor

# Move cursor too coordinates with optional offset and click
def move_cursor_with_optional_click_and_offset(x, y, click=False, offset = 0):
    try:
        # Randomized offset
        offset_x = random.randint(-offset, offset)
        offset_y = random.randint(-offset, offset)

        # New coordinates with offset applied
        target_x = x + offset_x
        target_y = y + offset_y

        # Create cursor with HumanCursor
        cursor = SystemCursor()

        # Optional Click
        if click:
            cursor.click_on((target_x, target_y))
        else:
            cursor.move_to((target_x, target_y))

        return True
    except Exception as e:
        print(f'An error occured: {e}')
        return False
