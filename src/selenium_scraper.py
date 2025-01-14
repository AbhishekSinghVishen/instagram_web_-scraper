from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import random
import json
import os
import requests
from src.config import CHROMEDRIVER_PATH, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
class InstagramScraper:
    def __init__(self, username):
        self.username = username
        self.posts = []
        self.driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH))
        self.login()

    def random_sleep(self, min_time=2, max_time=5):
        """Introduce a random sleep interval to mimic human behavior."""
        time.sleep(random.uniform(min_time, max_time))

    def login(self):
        self.driver.get("https://www.instagram.com/")
        self.random_sleep(4, 7)

        # Log in to Instagram
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")

        username_field.send_keys(INSTAGRAM_USERNAME)
        self.random_sleep(1, 3)
        password_field.send_keys(INSTAGRAM_PASSWORD)
        self.random_sleep(1, 3)
        password_field.send_keys(Keys.RETURN)

        self.random_sleep(5, 8)

    def scrape_posts_and_reels(self):
        # Navigate to the user's profile page
        self.driver.get(f"https://www.instagram.com/{self.username}/")
        self.random_sleep(5, 8)

        # Scroll and collect post and reel links
        post_links = set()
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Find all post and reel links on the page
            links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/') or contains(@href, '/reel/')]")
            for link in links:
                post_links.add(link.get_attribute("href"))

            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_sleep(3, 6)

            # Check if scrolling is complete
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Ensure the 'downloads' folder exists
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        # Scrape data from each post or reel
        for post_link in post_links:
            self.driver.get(post_link)
            self.random_sleep(4, 7)

            try:
                # Extract likes count
                try:
                    likes = self.driver.find_element(By.XPATH, "//section//span[contains(text(), 'likes')]/span").text
                except:
                    likes = "N/A"  # In case likes are not visible

                # Check if it's a post or a reel
                is_reel = "/reel/" in post_link

                # Extract media URL
                media_url = None
                if is_reel:
                    # Extract the real video URL from the <video> tag
                    try:
                        video_element = self.driver.find_element(By.XPATH, "//video")
                        media_url = video_element.get_attribute("src")
                        if media_url.startswith("blob:"):
                            # Blob URL workaround: Extract real media URL from JavaScript execution
                            media_url = self.driver.execute_script("""
                                var videoElement = document.querySelector('video');
                                return videoElement ? videoElement.src : null;
                            """)
                    except Exception as e:
                        print(f"Error extracting reel media URL: {e}")
                else:
                    # Extract image URL for posts
                    try:
                        media_url = self.driver.find_element(By.XPATH, "//div[@class='_aagv']//img").get_attribute("src")
                    except Exception as e:
                        print(f"Error extracting post media URL: {e}")

                # Print the media URL to check
                print(f"Media URL: {media_url}")

                # Append the post or reel data
                self.posts.append({
                    "url": post_link,
                    "type": "reel" if is_reel else "post",
                    "likes": likes,
                    "media_url": media_url,
                })

                # Download the media
                if media_url:
                    self.download_media(media_url, "reel" if is_reel else "post", is_reel)

            except Exception as e:
                print(f"Error scraping post/reel: {post_link}, {e}")

    def download_media(self, media_url, media_type, is_reel=False):
        """Download the media (image or video) from the provided URL."""
        try:
            # Generate a unique filename based on timestamp
            extension = "mp4" if is_reel else media_url.split(".")[-1].split("?")[0]
            filename = f"{media_type}_{int(time.time())}.{extension}"
            filepath = os.path.join("downloads", filename)

            if is_reel:
                # Download reel using requests (video URL extracted)
                response = requests.get(media_url, stream=True)
                response.raise_for_status()
                with open(filepath, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
            else:
                # Download image using requests
                response = requests.get(media_url, stream=True)
                response.raise_for_status()
                with open(filepath, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)

            print(f"{media_type.capitalize()} downloaded: {filepath}")
        except Exception as e:
            print(f"Error downloading {media_type}: {e}")

    def save_data(self):
        # Ensure the 'processed' folder exists
        if not os.path.exists("processed"):
            os.makedirs("processed")

        # Save the scraped data
        data = {
            "username": self.username,
            "posts": self.posts,
        }
        with open(f"processed/{self.username}.json", "w") as file:
            json.dump(data, file, indent=4)

    def close(self):
        self.driver.quit()
