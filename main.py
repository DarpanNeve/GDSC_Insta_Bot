import sqlite3
from datetime import datetime
from instagrapi import Client

# sends only one msg loop it

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
                # Call the function to post on Instagram
                post_to_instagram(user_id)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def post_to_instagram(username):
    try:
        # creds
        your_username = "pand.a123300"
        your_password = "mihir123"
        your_photo_path = "static/img1.jpg"

        # Compose the birthday message
        your_message = f"Happy Birthday {username}! 🎉🎂🎈 Sending you lots of love and good wishes on your special day! #BirthdayWishes #Celebration"

        # Create an Instagrapi client and login to your Instagram account
        client = Client()
        client.login(your_username, your_password)

        # Upload the photo and add the caption to post on Instagram
        client.photo_upload(your_photo_path, caption=your_message)

        # Logout from your Instagram account
        client.logout()

        print(f"Birthday message for {username} posted successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_today_birthdays()


