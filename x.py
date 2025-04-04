# # # # import requests
# # # # from bs4 import BeautifulSoup
# # # # import logging
# # # # import json

# # # # # Configure logging
# # # # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# # # # logger = logging.getLogger(__name__)

# # # # def scrape_university_reviews(url='https://www.careers360.com/university/apeejay-stya-university-sohna'):
# # # #     # Comprehensive headers to mimic browser
# # # #     headers = {
# # # #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
# # # #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# # # #         'Accept-Language': 'en-US,en;q=0.5',
# # # #         'DNT': '1',
# # # #         'Connection': 'keep-alive',
# # # #         'Upgrade-Insecure-Requests': '1'
# # # #     }

# # # #     try:
# # # #         # Send GET request
# # # #         response = requests.get(url, headers=headers, timeout=30)
        
# # # #         # Check response status
# # # #         logger.debug(f"Response Status Code: {response.status_code}")
# # # #         logger.debug(f"Response Content Length: {len(response.content)}")
        
# # # #         # Parse HTML
# # # #         soup = BeautifulSoup(response.content, 'html.parser')
        
# # # #         # Debug: Print out all div classes
# # # #         divs = soup.find_all('div')
# # # #         div_classes = set()
# # # #         for div in divs:
# # # #             if div.get('class'):
# # # #                 div_classes.update(div.get('class'))
        
# # # #         logger.debug(f"All div classes found: {div_classes}")
        
# # # #         # More comprehensive review extraction
# # # #         review_data = {
# # # #             "reviews": [],
# # # #             "raw_html": str(soup)
# # # #         }
        
# # # #         # Try multiple potential review section selectors
# # # #         review_selectors = [
# # # #             'div.detail_content_review',
# # # #             'div.review-content',
# # # #             'div.college-review',
# # # #             'div.review-section'
# # # #         ]
        
# # # #         for selector in review_selectors:
# # # #             reviews = soup.select(selector)
# # # #             logger.debug(f"Reviews found with selector {selector}: {len(reviews)}")
            
# # # #             for review in reviews:
# # # #                 review_text = review.get_text(strip=True)
# # # #                 if review_text:
# # # #                     review_data["reviews"].append(review_text)
        
# # # #         return review_data
    
# # # #     except Exception as e:
# # # #         logger.error(f"Scraping error: {e}")
# # # #         return None

# # # # def main():
# # # #     # Scrape reviews
# # # #     scrape_result = scrape_university_reviews()
    
# # # #     if scrape_result:
# # # #         # Save raw HTML for debugging
# # # #         with open('debug_page.html', 'w', encoding='utf-8') as f:
# # # #             f.write(scrape_result['raw_html'])
        
# # # #         # Save reviews to JSON for easy inspection
# # # #         with open('reviews.json', 'w', encoding='utf-8') as f:
# # # #             json.dump(scrape_result['reviews'], f, ensure_ascii=False, indent=2)
        
# # # #         # Print reviews
# # # #         print("\nReviews Found:")
# # # #         for idx, review in enumerate(scrape_result['reviews'], 1):
# # # #             print(f"{idx}. {review[:200]}...")  # Print first 200 chars
        
# # # #         print(f"\nTotal Reviews: {len(scrape_result['reviews'])}")
# # # #     else:
# # # #         print("No reviews could be scraped.")

# # # # # Run the scraper
# # # # if __name__ == "__main__":
# # # #     main()



# # # from selenium import webdriver
# # # from selenium.webdriver.common.by import By
# # # from selenium.webdriver.support.ui import WebDriverWait
# # # from selenium.webdriver.support import expected_conditions as EC
# # # from bs4 import BeautifulSoup
# # # import time
# # # import pandas as pd

# # # # Initialize WebDriver
# # # options = webdriver.ChromeOptions()
# # # options.add_argument("--headless")  # Run in headless mode (no UI)
# # # driver = webdriver.Chrome(options=options)

# # # # Open the webpage
# # # url = "https://www.careers360.com/colleges/dav-institute-of-engineering-and-technology-jalandhar/reviews"
# # # driver.get(url)

# # # # Wait for the page to load
# # # wait = WebDriverWait(driver, 10)

# # # # Scrape Overall Rating
# # # soup = BeautifulSoup(driver.page_source, "html.parser")
# # # overall_rating = soup.find("div", class_="rating_num").text.strip()
# # # total_reviews = soup.find("div", class_="rating_review").text.strip()

# # # print(f"Overall Rating: {overall_rating}")
# # # print(f"Total Reviews: {total_reviews}")

# # # # Scrape Category Ratings
# # # category_ratings = {}
# # # category_elements = soup.find_all("div", class_="rating_bar bar")
# # # for category in category_elements:
# # #     category_name = category.find("div", class_="label").text.strip()
# # #     rating = category.find("div", class_="bars usageMeter").text.strip()
# # #     category_ratings[category_name] = rating

# # # print("Category Ratings:", category_ratings)

# # # # Click on Each Tab (Infrastructure, Academics, etc.)
# # # categories = ["All", "Infrastructure", "Academics", "Placements", "Value for money", "Campus life"]
# # # reviews_data = {cat: [] for cat in categories}

# # # for category in categories:
# # #     try:
# # #         # Click on the category tab
# # #         button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, category)))
# # #         button.click()
# # #         time.sleep(3)  # Allow page to update

# # #         # Scrape Reviews
# # #         soup = BeautifulSoup(driver.page_source, "html.parser")
# # #         reviews = soup.find_all("div", class_="user_reviews_")

# # #         for review in reviews:
# # #             try:
# # #                 title = review.find("h3").text.strip()
# # #                 rating = review.find("div", class_="star-ratings")["title"].split()[0]  # Extract rating
# # #                 content = review.find("p").text.strip() if review.find("p") else "No content"

# # #                 reviews_data[category].append({
# # #                     "Title": title,
# # #                     "Rating": rating,
# # #                     "Review": content
# # #                 })
# # #             except Exception as e:
# # #                 print(f"Error extracting review: {e}")

# # #     except Exception as e:
# # #         print(f"Error clicking on {category}: {e}")

# # # # Close the WebDriver
# # # driver.quit()

# # # # Convert to DataFrame and Save to CSV
# # # df = pd.DataFrame([{**{"Category": cat}, **review} for cat, reviews in reviews_data.items() for review in reviews])
# # # df.to_csv("reviews.csv", index=False)
# # # print("Scraping complete. Data saved to reviews.csv")



# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from bs4 import BeautifulSoup
# # import time
# # import pandas as pd

# # # Initialize WebDriver
# # options = webdriver.ChromeOptions()
# # options.add_argument("--headless")  # Run in headless mode (no UI)
# # driver = webdriver.Chrome(options=options)

# # # Open the webpage
# # url = "https://www.careers360.com/colleges/dav-institute-of-engineering-and-technology-jalandhar/reviews"
# # driver.get(url)

# # # Wait for the page to load
# # wait = WebDriverWait(driver, 10)

# # # Define categories to scrape
# # categories = ["Infrastructure", "Academics", "Placements", "Value for money", "Campus life"]
# # reviews_data = {cat: [] for cat in categories}

# # # Scrape reviews for each category
# # for category in categories:
# #     try:
# #         # Click on the category tab
# #         button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, category)))
# #         button.click()
# #         time.sleep(3)  # Allow page to update

# #         # Scrape Reviews
# #         soup = BeautifulSoup(driver.page_source, "html.parser")
# #         reviews = soup.find_all("div", class_="user_reviews_")

# #         for review in reviews:
# #             try:
# #                 content = review.find("p").text.strip() if review.find("p") else "No review"
# #                 reviews_data[category].append(content)
# #             except Exception as e:
# #                 print(f"Error extracting review: {e}")

# #     except Exception as e:
# #         print(f"Error clicking on {category}: {e}")

# # # Close the WebDriver
# # driver.quit()

# # # Convert to DataFrame and Save to CSV
# # max_len = max(len(reviews) for reviews in reviews_data.values())  # Find the longest list
# # for cat in categories:
# #     reviews_data[cat] += [""] * (max_len - len(reviews_data[cat]))  # Fill shorter lists with empty strings

# # df = pd.DataFrame(reviews_data)
# # df.to_csv("reviews_column_wise.csv", index=False)
# # print("Scraping complete. Data saved to reviews_column_wise.csv")

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time

# # Setup WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# driver = webdriver.Chrome(options=options)

# # Target URL
# url = "https://www.careers360.com/colleges/dav-institute-of-engineering-and-technology-jalandhar/reviews"
# driver.get(url)

# # Categories to scrape
# categories = ["Infrastructure", "Academics", "Placement", "Value for money", "Campus life"]

# # Dictionary to store reviews
# reviews_dict = {category: [] for category in categories}

# # Wait for elements to load
# wait = WebDriverWait(driver, 10)

# for category in categories:
#     try:
#         # Find the tab and scroll to it
#         tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, category)))
#         driver.execute_script("arguments[0].scrollIntoView(true);", tab)
#         time.sleep(1)  # Allow time for scrolling
        
#         # Click the tab (try normal click first, then JS click if intercepted)
#         try:
#             tab.click()
#         except:
#             driver.execute_script("arguments[0].click();", tab)

#         time.sleep(3)  # Wait for reviews to load

#         # Scrape review text under the selected category
#         review_elements = driver.find_elements(By.CLASS_NAME, "review-text")  # Update class name as needed

#         for review in review_elements:
#             reviews_dict[category].append(review.text)

#     except Exception as e:
#         print(f"Error clicking on {category}: {e}")

# # Close the driver
# driver.quit()

# # Ensure equal column lengths by padding with empty strings
# max_reviews = max(len(reviews_dict[cat]) for cat in categories)
# for cat in categories:
#     reviews_dict[cat] += [""] * (max_reviews - len(reviews_dict[cat]))

# # Convert to DataFrame and save as CSV
# df = pd.DataFrame(reviews_dict)
# df.to_csv("reviews_column_wise.csv", index=False)

# print("Scraping complete. Data saved to reviews_column_wise.csv")
