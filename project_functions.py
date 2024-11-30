from speechbrain.inference import SpectralMaskEnhancement
import torchaudio
import tempfile
import datetime
import sqlite3
import random
import base64
import os
import io


# Connect to the database
def create_connection():
    """
    Creates database connection

    Returns:
        None
    """
    conn = sqlite3.connect('Voice_Recognition.db')
    return conn


# Create tables
def create_tables():
    """
    Creates the two tables needed for this project (Users table and voice_print table)

    User Table: For storing user basic data
    voice_print table: Referencing the primary key from Users as a foreign key, we ae able to link users voice from
    the voice table

    Returns:
        None
    """
    conn = create_connection()
    cursor = conn.cursor()

    # Create users table add 's' to voice_print(s) and user(s)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        other_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        dob DATE NOT NULL,
        phone TEXT NOT NULL,
        about LONGTEXT NOT NULL,
        sex TEXT NOT NULL,
        occupation TEXT NOT NULL,
        marital_status TEXT NOT NULL,
        picture BLOB NOT NULL)
    ''')

    # Create voice_prints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voice_print (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            voice_embedding BLOB NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


# Insert a new user
def insert_user(first_name, other_name, last_name, dob, phone, about, sex, occupation, marital_status, picture):
    """
        Inserts user details into the database after registration.

        Parameters:
            first_name (str): User's first name.
            other_name (str): User's middle name.
            last_name (str): User's last name.
            dob (date): User's date of birth.
            phone (str): User's phone number.
            about (str): Information about the user.
            sex (str): User's gender.
            occupation (str): User's occupation.
            marital_status (str): User's marital status.
            picture (bytes): Binary data representing the user's picture.

        Returns:
            int: The user ID from the database.
    """

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO user (
        first_name, other_name, last_name, dob, phone, about, sex, occupation, marital_status, picture)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, other_name, last_name, dob, phone, about, sex, occupation, marital_status, picture))

    conn.commit()
    user_id = cursor.lastrowid  # Get the inserted user's ID
    conn.close()

    return user_id


# Insert voice embedding
def insert_voice_embedding(user_id, voice_embedding):
    """

    :param user_id:
    :param voice_embedding:
    :return: None
    """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO voice_print (user_id, voice_embedding)
        VALUES (?, ?)
    ''', (user_id, voice_embedding))

    conn.commit()
    conn.close()


def enhance_audio_to_blob(audio_bytes):
    """
        Enhances the uploaded audio file using `speechbrain.inference.SpectralMaskEnhancement`.

        Parameters:
            audio_bytes (bytes): The uploaded audio file in bytes.

        Returns:
            bytes: The enhanced audio as a binary blob.
    """

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file_path = tmp_file.name

    try:
        model = SpectralMaskEnhancement.from_hparams(
            source="speechbrain/metricgan-plus-voicebank",
            savedir="pretrained_models/metricgan-plus-voicebank"
        )

        enhanced_speech = model.enhance_file(tmp_file_path)

        # Convert to a binary object (blob)
        buffer = io.BytesIO()
        torchaudio.save(buffer, enhanced_speech.view(1, -1), 16000, format="wav")
        audio_blob = buffer.getvalue()

    finally:
        # Delete the temporary file
        os.remove(tmp_file_path)

    return audio_blob


def dob_to_age(date_of_birth):
    """
    Calculates the user's age based on their date of birth.

    Parameters:
        date_of_birth (date): A date object representing the user's date of birth.

    Returns:
        int: The user's age in years.
    """

    if type(date_of_birth) is str:
        date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
        date_of_birth = date_of_birth.date()
        today = datetime.date.today()
        age_ = today - date_of_birth
        return round(age_.days/365)

    else:
        today = datetime.date.today()
        age_ = today - date_of_birth
        return round(age_.days/365)


def open_picture(image_name):
    """
    Loads an image file (PNG, JPEG, or JPG), converts it to a byte stream, and returns the byte data.

    This function opens an image file, reads its contents as bytes, and returns the binary representation. It is useful for processing or transferring images in binary format.

    Parameters:
        image_name (str): The name of the image file, including the file extension (e.g., 'picture.jpg').

    Returns:
        bytes: The binary content of the image file for further processing or storage.
    """

    cwd = os.path.dirname(__file__)
    image_path = os.path.join(cwd, "images", image_name)
    image_path = os.path.abspath(image_path)
    file = open(image_path, "rb")
    images = base64.b64encode(file.read()).decode()
    return images


def find_best_matching_user(input_audio_blob, recognizer):
    """
    Identifies the best matching user in the database for a given audio recording.

    Parameters:
        recognizer (model): The speaker recognition model used for matching.
        input_audio_blob (bytes): The binary audio data to verify.

    Returns:
        tuple: A tuple containing:
            - best_user_id (int): The ID of the user with the highest match.
            - best_score (float): The similarity score of the best match.
    """

    # Extract embedding for the input audio
    input_embedding = enhance_audio_to_blob(input_audio_blob)
    audio_tensor, sample_rate = torchaudio.load(io.BytesIO(input_embedding))

    # Initialize variables to store the best match
    best_user_id = None
    best_score = float("-inf")
    prediction = bool

    # Connect to the database to retrieve all user audio blobs
    conn = create_connection()
    cursor = conn.cursor()

    # Query to retrieve all user_id and audio_blob pairs
    cursor.execute("SELECT user_id, voice_embedding FROM voice_print")
    results = cursor.fetchall()
    # st.text([i for i in results])
    conn.close()

    # Loop through each user in the database
    for user_id, stored_audio_blob in results:
        # Extract embedding for the stored user's audio
        stored_embedding = torchaudio.load(io.BytesIO(stored_audio_blob))

        # Use verify_batch() to compare
        score, prediction = recognizer.verify_batch(audio_tensor, stored_embedding[0])

        # Check if this score is the highest so far
        if score > best_score:
            best_score = score
            best_user_id = user_id

    return best_user_id, best_score, prediction


def show_result(user_id):
    """
    Retrieves the user's details from the database after voice verification.

    Parameters:
        user_id (int): The primary key of the user in the database.

    Returns:
        list: A list containing the user's details retrieved from the database.
    """

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM user as t1 
    LEFT JOIN voice_print as t2 ON t1.user_id = t2.user_id 
    WHERE t1.user_id = ?
    """, (user_id, ))
    # """
    # row[0] = user_id        |   row[8] = sex
    # row[1] = Firstname      |   row[9] = occupation
    # row[2] = othername      |   row[10] = marital status
    # row[3] = Last name      |   row[11] = picture
    # row[4] = age            |   row[12] = voice_user_id
    # row[5] = DOB            |   row[13] = voice_user_id
    # row[6] = phone          |   row[14] = voice_print
    # row[7] = about
    # """

    execute_rows = cursor.fetchall()
    connection.close()
    return execute_rows


def test_train_sentences():
    """
    Parameters:
        None
    :return:
    """
    sentences = ["The Greeks used to imagine that it was a sign from the gods to foretell war",
                 "The Norsemen considered the rainbow as a bridge over which the gods passed",
                 "Others have tried to explain the phenomenon physically",
                 "The difference in the rainbow depends considerably upon the size of the drops",
                 "The actual primary rainbow observed is said to be the effect of super-imposition",
                 "The wise men used to believe that fate could change the course of history.",
                 "In the quiet woods, they heard strange sounds that seemed to echo from the past.",
                 "She thought the stars above might hold the answers to the mysteries of life.",
                 "The journey across the seas was seen as a test of strength and endurance.",
                 "Many cultures have stories that speak of heroes who rise in times of need."]
    return random.choice(sentences)
