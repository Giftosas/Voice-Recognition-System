import datetime
import math
import os
import base64


def dob_to_age(date_of_birth):
    """

    :param date_of_birth:
    :return:
    """
    if type(date_of_birth) is str:
        date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
        date_of_birth = date_of_birth.date()
        today = datetime.date.today()
        age = today - date_of_birth
        return age.days/365
    else:
        today = datetime.date.today()
        age = today - date_of_birth
        return age/365


def phone_num_validation(phone):
    """
    Validates the phone number passed in by the user, ensuring accuracy

    Parameters:
        phone (int): The user input containing an 11-digit number
    Returns:
        phone (int): Post validation, whatever reaches here m=is correct, so this would be returned to be used.
    """
    while math.floor(math.log10(phone)) + 1 < 11:
        phone = int(input("Enter please 11: -> "))
    else:
        return phone


def open_picture(image_name):
    """
    Loads an image file (PNG, JPEG, or JPG format), converts it to a byte stream, and returns the byte data.

    This function takes the name of an image file, opens it, reads its contents as bytes, and returns the byte representation.
    Useful for cases where images need to be processed or transferred in binary format.

    Parameters:
        image_name (str): The filename of the image to load, including the file extension (e.g., 'picture.jpg').

    Returns:
        bytes: The byte content of the image file, ready for further processing or storage.
    """

    cwd = os.path.dirname(__file__)
    image_path = os.path.join(cwd, "images", image_name)
    image_path = os.path.abspath(image_path)
    file = open(image_path, "rb")
    images = base64.b64encode(file.read()).decode()
    return images



phnowe= phone_num_validation(int(8088785996))
print(phnowe)