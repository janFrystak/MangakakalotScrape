import requests
from bs4 import BeautifulSoup
from PIL import Image
import time
import io

# Function to download and show the CAPTCHA image
def get_captcha_image(soup):
    # Find the CAPTCHA image using the provided structure
    captcha_img_tag = soup.find('img', src=lambda x: x and 'captcha' in x)
    if captcha_img_tag:
        captcha_url = captcha_img_tag['src']
        return captcha_url
    return None

# Function to handle user login
def handle_login(session, username, password, captcha_answer):
    login_url = 'https://user.manganelo.com/login?l=mangakakalot&re_l=login'  # Updated login URL
    payload = {
        'username': username,
        'password': password,
        'captcha': captcha_answer  # Assuming the form field for the CAPTCHA is named 'captcha'
    }

    # Post the login request
    login_response = session.post(login_url, data=payload)

    # Check if login was successful
    return login_response.ok

# Function to fetch manga titles after logging in
def fetch_bookmarked_manga_titles(session):
    manga_url = 'https://mangakakalot.com/bookmark'  # Updated manga listing URL
    response = session.get(manga_url)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = soup.find_all('a', rel="nofollow", style="color: #e12a2a!important;")

        for title in titles:
            manga_title = title.text.strip()

            print(manga_title)
    else:
        print("Failed to retrieve manga titles.")

# Main function to orchestrate the login and title fetching process
def main():
    session = requests.Session()
    username = input("Enter your username: ")  # Prompt for username
    password = input("Enter your password: ")  # Prompt for password
    print("Starting the login  process...")

    # First, get the login page to retrieve the CAPTCHA
    response = session.get('https://user.manganelo.com/login?l=mangakakalot&re_l=login')
    if not response.ok:
        print("Failed to load login page.")
        return

    # Parse the HTML to find the CAPTCHA image
    soup = BeautifulSoup(response.content, 'html.parser')
    captcha_url = get_captcha_image(soup)

    if captcha_url:
        # Download the CAPTCHA image
        captcha_response = session.get(captcha_url)
        image = Image.open(io.BytesIO(captcha_response.content))
        image.show()  # This will open the CAPTCHA image in a window

        # Ask the user for the CAPTCHA answer
        captcha_answer = input("Please enter the CAPTCHA text: ")

        # Handle the login
        if handle_login(session, username, password, captcha_answer):
            print("Login successful!")
            time.sleep(2)
            fetch_bookmarked_manga_titles(session)
        else:
            print("Login failed! Please check your credentials and CAPTCHA.")
    else:
        print("CAPTCHA image not found.")

if __name__ == "__main__":
    main()
