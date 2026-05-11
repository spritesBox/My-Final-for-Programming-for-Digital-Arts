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

def correct_incorrect_guess(user_input, correct_answer):
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
    user_input = input("")
    incorrect_answers = ["incorrect1", "incorrect2", "incorrect3", "incorrect4", "incorrect5"] #placement for now
    #randomly select 3 incorrect answers from the list of incorrect answers
    selected_incorrect_answers = random.sample(incorrect_answers, 3)
    #combine the correct answer with the selected incorrect answers and shuffle the list
    answer_choices = [correct_answer] + selected_incorrect_answers
    random.shuffle(answer_choices)

    if user_input.lower() == correct_answer.lower():
        result = "Correct!"
    else:
        result = f"Wrong! The correct answer was: {correct_answer}"

    return result, answer_choices

def rescale_image(path):
    image_paths = load_pixelated_images()
    img = pygame.image.load(path)

    #full screen resolution
    infoObject = pygame.display.Info()
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)
    screen_w, screen_h = screen.get_size()

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
    
    idx = 0
    current_image, img_w, img_h, x, y = rescale_image(image_paths[idx])
    #event loop
    user_input = " "
    #correct = correct_incorrect_guess(user_input, correct_answer) #placeholder for now
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                 # Backspace deletes
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
            # Handle user input for gues
            # sing the image here
            # Display the current pixelated image and answer choices here
            # if correct, display "Correct!" and move to the next image; if incorrect, display "Wrong!" 
            # and end the game  
                elif event.key == pygame.K_RETURN:
                    correct_answer = os.path.basename(image_paths[idx]).split(".")[0]
                    result, choices = correct_incorrect_guess(user_input, correct_answer)

                    print(result)
                    print("Choices:", choices)

                    if result == "Correct!":
                        idx += 1
                        print(result)
                    if idx >= len(image_paths): #if there are more images to go through
                        #call rain.py confetti burst, but for now...
                        print ("Congradulations! You beat the Game!")
                    elif result == "Wrong! The correct answer was: " + correct_answer:
                        print(result)
                        time.sleep(3)
                        running = False
                    else:
                        #change current image to next in the list
                        current_image, img_w, img_h, x, y = rescale_image(image_paths[idx])
                    
                    user_input = ""
                
                # Normal typing
                else:
                    if hasattr(event, "unicode") and event.unicode.isprintable():
                        user_input += event.unicode
                    

        screen.fill((0,0,0))
        screen.blit(current_image, (x,y))
        pygame.display.flip()




if __name__ == "__main__":
    main()

