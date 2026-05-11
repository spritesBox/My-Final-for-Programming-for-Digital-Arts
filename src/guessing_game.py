#from email.mime import image
import os
import glob
import random
import pygame
import time


#TODO: create a mini game where player guesses what the item is based on pixelated images
#with no score for now; just end game when player is wrong and display text when player is correct
#1. accesses pixelated_images directory and saves the file paths of the pixelated images in a list
#2. open file dialog to select an image from the directory and save the file path 
#4. display a random pixelated image from the list and ask the player to guess what it is by typing in a text box
#5. user input asks for the name of the item in the image and checks if it is correct by comparing 
# it to the name in the list that corresponds to the file path of the image
#6. if user is correct, display "correct!" and the next image appears; if user is wrong, 
# display "wrong!" and end the game
#7. if player inputs "quit", end the game
#8. if player inputs an unknown command, display "invalid input, please try again" and ask for input again
#9. after player guesses all images correctly, display "congratulations, you guessed all the images!" 
#10. game ends

def open_file_dialog():
    
    """Open a file dialog to select an image from the pixelated_images directory and return the file path.

    :param directory: The directory to open the file dialog in. Defaults to "pixelated_images".
    :type directory: str, optional

    :return: The file path of the selected image.
    :rtype: str

    :param list_of_images: A list of file paths to the pixelated images available for selection.
    :type list_of_images: list of str

    """
    for image in os.listdir("pixelated_images"): #do this for every image in directory
        if image.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join("pixelated_images", image)
            return image_path


def load_pixelated_images(directory="pixelated_images"):
    """Load the pixelated images from the specified directory.

    :param directory: The directory containing the pixelated images.
    :type directory: str, optional

    :return: A list of file paths to the pixelated images.
    :rtype: list of str
    """
    image_paths = []
    for image in os.listdir(directory):
        if image.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(directory, image)
            image_paths.append(image_path)
    return image_paths

def correct_incorrect_guess(user_choice, correct_answer):
    """Check if the user's guess is correct and return the appropriate response.
    Display multiple choices for the user to select from for each image

    :param user_input: The user's guess for the image.
    :type user_input: str

    :param correct_answer: The correct answer corresponding to the image.
    :type correct_answer: str

    :return: A message indicating whether the user's guess is correct or incorrect.
    :rtype: str
    """
    #create list of possible answers for program to randomly select from, including the correct answer and some incorrect answers
    incorrect_answers = ["incorrect1", "incorrect2", "incorrect3", "incorrect4", "incorrect5"] #placement for now
    #randomly select 3 incorrect answers from the list of incorrect answers
    selected_incorrect_answers = random.sample(incorrect_answers, 3)
    #combine the correct answer with the selected incorrect answers and shuffle the list
    answer_choices = [correct_answer] + selected_incorrect_answers
    random.shuffle(answer_choices)

    if user_choice.lower() == correct_answer.lower():
        result = "Correct!"
    else:
        result = f"Wrong! The correct answer was: {correct_answer}"

    return result, answer_choices

def rescale_image(path):
    image_paths = load_pixelated_images()
    img = pygame.image.load(path)

    #full screen resolution
    infoObject = pygame.display.Info()
    screen_w, screen_h = infoObject.current_w, infoObject.current_h

    #resize image to fit screen
    img_w, img_h = img.get_size()
    scale = min(screen_w/img_w, screen_h/img_h, 1)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    if scale < 1:
        img = pygame.transform.scale(img, (new_w, new_h))
        img_w, img_h = new_w, new_h

    #center image to screen
    x = (screen_w - img_w)//2
    y = (screen_h - img_h)//2

    return img, img_w, img_h, x, y

def button_design(screen, answer_choices, font):
    #full screen resolution
    screen_w, screen_h = screen.get_size()
    
    #button properties
    buttons = []
    button_height = 80
    button_width = 300
    spacing = 10
    bg_color = (255,220,100)
    txt_color = (0,0,0)

    total_width = 4 * button_width + 3 * spacing
    start_x = (screen_w - total_width) // 2
    y = 40

    for i, text in enumerate(answer_choices):
        x = start_x + i * (button_width + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)

        pygame.draw.rect(screen, bg_color, rect, border_radius=12)

        label = font.render(text, True, txt_color)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

        buttons.append(rect)

    return buttons

def main(): 
    
    """ function to run the guessing  and display the images. 
    This function initializes the game, displays pixelated images, and handles user input for guessing the images.

    :return: None
    :rtype: None 
    
    """
    # Load pixelated images and initialize game variables
    image_paths = load_pixelated_images()
    random.shuffle(image_paths)

    # screen scale
    pygame.init()
    pygame.display.set_caption("Guessing Game")
    infoObject = pygame.display.Info() 
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)
    font = pygame.font.SysFont(None, 48)
    
    
    idx = 0
    user_input = ""
    current_image, img_w, img_h, x, y = rescale_image(image_paths[idx])
    #event loop
    filename = os.path.basename(image_paths[idx]).split(".")[0]
    correct_answer = filename.replace("_pixelated", "")
    result, answer_choices = correct_incorrect_guess("", correct_answer)
    running = True

    while running:

        screen.fill((0,0,0))
        screen.blit(current_image, (x,y))
        buttons = button_design(screen, answer_choices, font)
        pygame.display.flip()

        for event in pygame.event.get():
        # draw image and buttons first so rects exist
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                elif hasattr(event, "unicode") and event.unicode.isprintable():
                    user_input += event.unicode
    
            # Handle user input for gues
            # sing the image here
            # Display the current pixelated image and answer choices here
            # if correct, display "Correct!" and move to the next image; if incorrect, display "Wrong!" 
            # and end the game  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                for i, rect in enumerate(buttons):
                    if rect.collidepoint(mx, my):
                        user_choice = answer_choices[i]
                    
                        result, _ = correct_incorrect_guess(user_choice, correct_answer)

                        if result == "Correct!":
                            idx += 1
                            print(result)

                            if idx >= len(image_paths): #if there are more images to go through
                                #call rain.py confetti burst, but for now...
                                print ("Congradulations! You beat the Game!")
                                running = False
                                break
                            current_image, img_w, img_h, x, y = rescale_image(image_paths[idx])
                            filename = os.path.basename(image_paths[idx]).split(".")[0]
                            correct_answer = os.path.basename(image_paths[idx]).split(".")[0]
                            result, answer_choices = correct_incorrect_guess("", correct_answer)

                        elif result == "Wrong! The correct answer was: " + correct_answer:
                            print(result)
                            time.sleep(3)
                            running = False

                        break
                
                # Normal typing
                else:
                    if hasattr(event, "unicode") and event.unicode.isprintable():
                        user_input += event.unicode
                    

if __name__ == "__main__":
    main()

