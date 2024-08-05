import sys
import pyautogui as pt
from time import sleep
import os
import cv2
import numpy as np
from skimage.feature import match_template
from io import BytesIO
import keyboard
import threading

print(cv2.__version__)


# Function to check for keyboard input


def movement():
    #Note just to make the program run more efficient
    pt.keyDown(movement_key)
    pt.keyUp(movement_key)
    pt.keyDown(movement_key)
    pt.keyUp(movement_key)
    pt.keyDown(movement_key)
    pt.keyUp(movement_key)
    pt.keyDown(movement_key)
    pt.keyUp(movement_key)
    pt.keyDown(movement_key)
    pt.keyUp(movement_key)
    pt.keyDown(movement_key)
    pt.keyUp(movement_key)


def load_and_preprocess_image(image_path):
    """Load an image and convert it to grayscale."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Failed to load image from {image_path}")
    return image


def locate_images_on_screen(template, confidence=.6):
    """Locate all template images on screen with grayscale preprocessing."""
    screen = pt.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= confidence)
    detected_positions = []
    for pt_position in zip(*locations[::-1]):
        detected_positions.append((pt_position[0], pt_position[1], template.shape[1], template.shape[0]))
    return detected_positions


def nav_to_image(image_path, clicks, confidence=.5):
    """Navigate to an image on screen and click."""
    try:
        template = load_and_preprocess_image(image_path)
        if template is None:
            return False

        positions = locate_images_on_screen(template, confidence)
        if not positions:
            print(f'{image_path} not found')
            return False
        else:
            # Sort positions by x-coordinate to prioritize the leftmost position
            positions.sort(key=lambda pos: pos[0])
            leftmost_position = positions[0]
            center_x = leftmost_position[0] + leftmost_position[2] // 2
            center_y = leftmost_position[1] + leftmost_position[3] // 2
            pt.moveTo(center_x, center_y, duration=.1)
            pt.click(clicks=clicks, interval=.3)
            print(f'Clicked on {image_path} at ({center_x}, {center_y})')
            return True
    except Exception as e:
        print(f"Error occurred while navigating to image '{image_path}': {e}")
        return False


def nav_to_image2(image_path, clicks, confidence=.3):
    """Navigate to an image on screen and click."""
    try:
        template = load_and_preprocess_image(image_path)
        if template is None:
            return False

        positions = locate_images_on_screen(template, confidence)
        if not positions:
            print(f'{image_path} not found')
            return False
        else:
            # Sort positions by x-coordinate to prioritize the rightmost position
            positions.sort(key=lambda pos: pos[0] + pos[2], reverse=True)
            rightmost_position = positions[0]
            center_x = rightmost_position[0] + rightmost_position[2] // 2
            center_y = rightmost_position[1] + rightmost_position[3] // 2
            pt.moveTo(center_x, center_y, duration=.1)
            pt.click(clicks=clicks, interval=.3)
            print(f'Clicked on {image_path} at ({center_x}, {center_y})')
            return True
    except Exception as e:
        print(f"Error occurred while navigating to image '{image_path}': {e}")
        return False


def check_inventory(images, confidence_threshold=.45):
    """Check if any of the inventory images are found on screen."""
    try:
        # Capture the screen image
        screen = pt.screenshot(region=(0, 0, 1920, 1080))
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

        # Iterate over the reference images
        for image_path in images:
            if not os.path.exists(image_path):
                print(f"Image file '{image_path}' does not exist.")
                continue

            # Load the reference image
            reference_image = cv2.imread(image_path)

            # Convert to grayscale
            reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

            # Convert screen to grayscale
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            # Perform template matching
            result = cv2.matchTemplate(screen_gray, reference_gray, cv2.TM_CCOEFF_NORMED)

            # Get the maximum correlation coefficient
            max_confidence = np.max(result)

            # Check if the confidence exceeds the threshold
            if max_confidence >= confidence_threshold:
                print(f"Inventory image '{image_path}' found with confidence {max_confidence}.")
                return True

        print(f'Inventory image not found with confidence threshold {confidence_threshold}')
        return False

    except Exception as e:
        print(f'Error occurred while locating inventory image: {e}')
        return False


# List of inventory images for checking
inventory_images = [
    'Images/Inv_Open 1.png',
    'Images/Inv_Open.png',
    'Images/Inv_Open 2.png',
    'Images/Inv_Open 3.png',
    'Images/Inv_Open 4.png',
    'Images/Inv_Open 5.png',
    'Images/Inv_Open 6.png',
    'Images/Inv_Open 7.png',
    'Images/Inv_Open 8.png',
    # Add more inventory images as needed
]

# List of additional inventory images for the second part
additional_inventory_images = [
    'Images/Inventory_1.png',
    'Images/Inventory_2.png',
    'Images/Inventory_3.png',
    'Images/Inventory_4.png',
    'Images/Inevntory_5.png',
    'Images/Inevntory_6.png',
    'Images/Inevntory_7.png',
    'Images/Inevntory_8.png',
    'Images/Inevntory_9.png',
    # Add more inventory images as needed
]

# Ask the user for the target open count
while True:
    try:
        target_open_count = int(input("Enter the number of times you want to open the inventory: "))
        break
    except ValueError:
        print("Invalid input. Please enter an integer value.")

# Initial movement key
movement_key = 'd'

while True:
    # Initial sleep to give the user time to switch to the correct window
    sleep(3)

    # Counter for how many times the inventory has been opened
    inventory_open_count = 0

    while inventory_open_count < target_open_count:
        # Press the current movement key slowly until the inventory is open
        while not check_inventory(inventory_images, confidence_threshold=.43):
            print(f"Inventory is not open. Pressing '{movement_key}'.")
            pt.keyDown(movement_key)
            pt.keyUp(movement_key)
            sleep(.2)  # Adjust the sleep time as needed

        # Inventory is open, proceed with actions
        sleep(.3)
        print("Inventory is open. Pressing 'f'.")
        pt.press('f')
        sleep(.3)

        # Additional actions once inventory is open
        print("Checking additional inventory images.")
        if check_inventory(additional_inventory_images, confidence_threshold=.04):
            sleep(.3)
            print("Performing additional actions.")
            if nav_to_image('Images/Search bar.png', 2):
                pt.press('b')
                pt.press('e')
                pt.press('r')
                print("Typed 'Berry but shortened'.")
            else:
                print("Failed to find and click on 'Search bar.png'.")
            if nav_to_image('Images/Exchange.png', 1, confidence=.6):
                print("Clicked on Exchange.")
            else:
                print("Failed to find and click on 'Exchange.png'.")
            if nav_to_image2('Images/Exit_1.png', 1, confidence=.6):
                print("Exit Inventory")
                movement()
            else:
                if nav_to_image2('Images/Exit_2.png', 1, confidence=.6):
                    print('Clicked on Exit_2.png')
                    movement()
                else:
                    print("Failed to find and click on 'Exit.png'.")
                    pt.keyDown('esc')
                    pt.keyUp('esc')
                    print('Emergency Escape')
                    movement()
        else:
            print("Additional inventory images not found.")
            pt.keyDown('esc')
            pt.keyUp('esc')
            print('Emergency Escape')
            if nav_to_image('Images/Resume.png', 1, confidence=.8):
                movement()
            else:
                movement()

            # Increment the counter for inventory open count
        inventory_open_count += 1
        print(f'Inventory has been opened {inventory_open_count} times.')

        # Sleep before rechecking the inventory
        sleep(.2)

    print("Target inventory open count reached.")

    # Toggle the movement key
    if movement_key == 'd':
        movement_key = 'a'
    else:
        movement_key = 'd'
