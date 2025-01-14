# main.py
from src.selenium_scraper import InstagramScraper

if __name__ == "__main__":
    username = input("Enter the Instagram username to scrape: ")
    scraper = InstagramScraper(username)

    try:
        scraper.scrape_posts_and_reels()
        scraper.save_data()
        print(f"Scraped data saved for {username}")
    finally:
        scraper.close()
