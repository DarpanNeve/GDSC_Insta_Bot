import os
import sqlite3
from datetime import datetime
from instagrapi import Client
from instagrapi.types import StoryMention, StoryHashtag
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()


def check_today_birthdays():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/birthday.db')
    cursor = conn.cursor()

    try:
        # Execute a query to retrieve data from the Birthday table
        cursor.execute("SELECT user_id, birthday FROM birthday")

        # Fetch all the data from the query result
        data = cursor.fetchall()

        # Get the current date as a datetime object
        current_date = datetime.now()

        # Loop through the data and check for today's birthdays
        for row in data:
            user_id, birthday_str = row
            # Convert the birthday string to a datetime object
            birthday_date = datetime.strptime(birthday_str, "%Y-%m-%d")
            # Compare the month and day of the birthday with the current date
            if birthday_date.month == current_date.month and birthday_date.day == current_date.day:
                try:
                    # creds
                    your_username = os.getenv("INSTAGRAM_USERNAME")
                    your_password = os.getenv("INSTAGRAM_PASSWORD")
                    # Create an Instagrapi client and login to your Instagram account
                    client = Client()
                    client.login(your_username, your_password)
                except Exception as e:
                    print(f"An error occurred during the login process: {e}")
                    close_db(cursor, conn)
                    return -1
                # Call the function to post and create story on Instagram
                post_to_instagram(user_id, client, your_photo_path="static/img1.jpg")
                post_story_to_instagram(user_id, client, your_photo_path="static/img1.jpg")
                # Logout from your Instagram account
                client.logout()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        close_db(cursor, conn)


def close_db(cursor, conn):
    cursor.close()
    conn.close()


def post_to_instagram(username, client, your_photo_path):
    try:
        # Compose the birthday message
        your_message = f"Happy Birthday {username}! 🎉🎂🎈 Sending you lots of love and good wishes on your special day! #BirthdayWishes #Celebration"
        # Upload the photo and add the caption to post on Instagram
        client.photo_upload(your_photo_path, caption=your_message)
        print(f"Birthday message for {username} posted successfully!")

    except Exception as e:
        print(f"Error: {e}")


def post_story_to_instagram(username, client, your_photo_path):
    try:

        # Constant defined for size constraint

        CONST_SIZE_FOR_STORY_IMAGE = (720, 1280)

        # Posting image to story requires the image to 720x1280, so if the sizing is not correct of src image, we re-correct it

        img = Image.open(your_photo_path)
        wid, hgt = img.size

        if (wid, hgt) != CONST_SIZE_FOR_STORY_IMAGE:
            img = img.resize(CONST_SIZE_FOR_STORY_IMAGE)
            img.save("static/img1_c.jpg")
            your_photo_path = "static/img1_c.jpg"

        hashtag = "happybirthday"

        your_message = f"Happy Birthday {username}! 🎉🎂🎈 Sending you lots of love and good wishes on your special day! #BirthdayWishes #Celebration"

        client.photo_upload_to_story(
            your_photo_path,
            your_message,
            mentions=[StoryMention(user=client.user_info_by_username(username), x=0.49892962, y=0.703125, width=0.9333333333333334, height=0.525)],
            hashtags=[StoryHashtag(hashtag=client.hashtag_info(hashtag), x=0.23, y=0.32, width=0.8, height=0.52)]
        )

        # Remove the temporarily created correct-resolution photo

        if "_c" in your_photo_path:
            os.remove(your_photo_path)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_today_birthdays()
