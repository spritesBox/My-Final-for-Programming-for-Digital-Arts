import os
import glob


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

def correct_incorrect_guess(user_input, correct_answer):
    """Check if the user's guess is correct and return the appropriate response.

    :param user_input: The user's guess for the image.
    :type user_input: str

    :param correct_answer: The correct answer corresponding to the image.
    :type correct_answer: str

    :return: A message indicating whether the user's guess is correct or incorrect.
    :rtype: str
    """

def main(): 
    
    """ function to run the guessing  and display the images. 
    This function initializes the game, displays pixelated images, and handles user input for guessing the images.

    :return: None
    :rtype: None 
    
    """


if __name__ == "__main__":
    main()

