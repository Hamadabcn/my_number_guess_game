import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Guessing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)

# Fonts for different text elements
title_font = pygame.font.Font(None, 80)    # Font for the title
message_font = pygame.font.Font(None, 50)  # Font for game messages
input_font = pygame.font.Font(None, 60)    # Font for user input
small_font = pygame.font.Font(None, 40)    # Font for instructions and high score

# Game variables
secret_number = random.randint(1, 100)  # Randomly generate the secret number
attempts = 0  # Counter for the number of attempts
guess = ""  # Current guess from the user
message = "I'm thinking of a number between 1 and 100."  # Initial message
input_active = True  # Flag to check if input is active
high_score = None  # Initialize high score


# Function to draw a gradient background
def draw_gradient_background(screen, top_color, bottom_color):
    for y in range(HEIGHT):
        # Calculate the color for each line to create a gradient effect
        color = [
            top_color[i] + (bottom_color[i] - top_color[i]) * y // HEIGHT
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))


# Function to render centered text in a given rectangle
def render_centered_text(text, font, color, rect, surface):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect.topleft)


# Function to draw the range indicator (bar showing how close the guess is to the secret number)
def draw_range_indicator(screen, guess, secret_number):
    if guess is not None:
        difference = abs(guess - secret_number)  # Calculate the difference between guess and secret number
        max_diff = 100  # Maximum possible difference
        bar_width = 200  # Width of the range indicator bar
        fill_width = bar_width * (1 - difference / max_diff)  # Calculate the width of the filled part of the bar
        pygame.draw.rect(screen, RED, (WIDTH // 2 - 100, 520, fill_width, 20))  # Draw the filled part of the bar
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, 520, bar_width, 20), 2)  # Draw the outline of the bar


# Function to draw a button with hover and press effects
def draw_button(screen, text, rect, color, text_color, hover_color=None, press_color=None):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
            pygame.draw.rect(screen, press_color if press_color else color, rect)  # Draw button with press color
        else:
            pygame.draw.rect(screen, hover_color if hover_color else color, rect)  # Draw button with hover color
    else:
        pygame.draw.rect(screen, color, rect)  # Draw button with default color
    render_centered_text(text, small_font, text_color, rect, screen)  # Render the button text


# Number pad buttons configuration
number_buttons = {}
button_size = 60  # Size of each button on the number pad
button_margin = 10  # Margin between buttons
button_font = small_font

# Vertical offset for the number pad
numpad_vertical_offset = 500 + 4  # Move the numpad down by 4 pixels

# Create number buttons for digits 1 to 9
for i in range(1, 10):
    x = (i - 1) % 3 * (button_size + button_margin)
    y = (i - 1) // 3 * (button_size + button_margin)
    number_buttons[i] = pygame.Rect(WIDTH - 300 + x, numpad_vertical_offset + y, button_size, button_size)

# Position for the "0" button and the "Clear" button
number_buttons[0] = pygame.Rect(WIDTH - 300 + button_size + button_margin,
                                numpad_vertical_offset + 3 * (button_size + button_margin), button_size, button_size)

# Create the Clear button next to the "0" button
clear_button = pygame.Rect(number_buttons[0].right + button_margin, numpad_vertical_offset + 3 *
                           (button_size + button_margin), button_size, button_size)
number_buttons['C'] = clear_button

# Create Submit and Play Again buttons
submit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 120, 200, 50)
play_again_button = pygame.Rect(WIDTH - 600, submit_button.bottom + 30 - 12, 200, 50)

# Create input box
input_box = pygame.Rect(WIDTH // 2 - 200, 400, 400, 60)

# Game loop
running = True
while running:
    # Draw gradient background
    draw_gradient_background(screen, LIGHT_BLUE, DARK_BLUE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    # Handle Enter key to submit the guess
                    if guess.isdigit():
                        guess_number = int(guess)
                        attempts += 1
                        if guess_number < secret_number:
                            message = "Too low! Try again."
                            guess = ""
                        elif guess_number > secret_number:
                            message = "Too high! Try again."
                            guess = ""
                        else:
                            message = f"Congratulations! You found it in {attempts} attempts."
                            input_active = False
                            # Update high score if needed
                            if high_score is None or attempts < high_score:
                                high_score = attempts
                    else:
                        message = "Please enter a valid number."
                        guess = ""
                elif event.key == pygame.K_BACKSPACE:
                    # Handle Backspace to remove the last character
                    guess = guess[:-1]
                else:
                    # Add the typed character to the guess
                    guess += event.unicode
            elif not input_active and event.key == pygame.K_RETURN:
                # Reset the game if Enter is pressed after winning
                secret_number = random.randint(1, 100)
                attempts = 0
                guess = ""
                message = "I'm thinking of a number between 1 and 100."
                input_active = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_active:
                mouse_pos = event.pos
                if submit_button.collidepoint(mouse_pos):
                    # Handle Submit button click
                    if guess.isdigit():
                        guess_number = int(guess)
                        attempts += 1
                        if guess_number < secret_number:
                            message = "Too low! Try again."
                            guess = ""
                        elif guess_number > secret_number:
                            message = "Too high! Try again."
                            guess = ""
                        else:
                            message = f"Congratulations! You found it in {attempts} attempts."
                            input_active = False
                            # Update high score if needed
                            if high_score is None or attempts < high_score:
                                high_score = attempts
                    else:
                        message = "Please enter a valid number."
                        guess = ""
                elif clear_button.collidepoint(mouse_pos):
                    # Handle Clear button click
                    guess = ""  # Clear the input
                else:
                    # Handle number pad button clicks
                    for number, rect in number_buttons.items():
                        if number != 'C' and rect.collidepoint(mouse_pos):
                            guess += str(number)

            elif not input_active:
                mouse_pos = event.pos
                if play_again_button.collidepoint(mouse_pos):
                    # Handle Play Again button click
                    secret_number = random.randint(1, 100)
                    attempts = 0
                    guess = ""
                    message = "I'm thinking of a number between 1 and 100."
                    input_active = True

    # Render the title
    title_surface = title_font.render("Guess My Number!", True, GOLD)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

    # Render the instructions
    instructions = [
        "Instructions:",
        "1. Enter your guess below and press Enter.",
        "2. You can also use the Numpad and the Check button.",
        "3. Try to guess the number in the fewest possible attempts.",
        "Good luck, and have fun!",
    ]
    for i, line in enumerate(instructions):
        instruction_surface = small_font.render(line, True, WHITE)
        screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, 150 + i * 35))

    # Render the message
    message_surface = message_font.render(message, True, PURPLE)
    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, 350))

    # Render the input box
    pygame.draw.rect(screen, BLACK, input_box, 2)  # Draw input box outline
    input_surface = input_font.render(guess, True, GREEN)
    input_text_rect = input_surface.get_rect(center=input_box.center)
    screen.blit(input_surface, input_text_rect.topleft)

    # Draw the range indicator
    draw_range_indicator(screen, int(guess) if guess.isdigit() else None, secret_number)

    # Render the number pad
    for number, rect in number_buttons.items():
        if number == 'C':
            draw_button(screen, "C", rect, RED, WHITE, RED, BLACK)  # Customize the Clear button
        else:
            draw_button(screen, str(number), rect, GRAY, WHITE, DARK_BLUE, BLACK)

    # Render the Submit button
    draw_button(screen, "Check", submit_button, GRAY, WHITE, DARK_BLUE, BLACK)

    # Render the Play Again button if game is over
    if not input_active:
        draw_button(screen, "Play Again", play_again_button, RED, WHITE, DARK_BLUE, BLACK)

        # Render the highest score above the Play Again button
        if high_score is not None:
            high_score_surface = small_font.render(f"Highest Score: {high_score} attempts", True, YELLOW)
            screen.blit(high_score_surface,
                        (WIDTH // 2 - high_score_surface.get_width() // 2, play_again_button.top - 120))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
