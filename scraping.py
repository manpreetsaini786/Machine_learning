# import requests
# from bs4 import BeautifulSoup

# def Scraping(id,page):
#     # url = f"https://www.careers360.com/colleges/reviews?page={page}&college_id={id}"
#     url=f"https://www.careers360.com/colleges/reviews?page={page}&college_id={id}"
#     # f"https://www.careers360.com/colleges/reviews?page={1}&college_id={12}"
    
    
#     proxy={
#             "http": "http://pehgjxwr:j7u0qyb1xux8@198.23.239.134:6540",
#             "https": "http://pehgjxwr:j7u0qyb1xux8@198.23.239.134:6540",
#             "http": "http://pehgjxwr:j7u0qyb1xux8@207.244.217.165:6712",
#             "https": "http://pehgjxwr:j7u0qyb1xux8@207.244.217.165:6712"
#         }

#     response = requests.get(url,proxies=proxy)    
#     College_Infrastructure = []
#     Academics = []
#     Placements = []
#     Campus_Life = []
#     Anything_Else = []

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         divs = soup.find_all('div', class_='detail_content_review')
#     else:
#         print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

#     for div in divs:
#         # Access <h> tags (assuming it could be any heading tag like <h1>, <h2>, etc.)
#         heading = div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
#         paragraph = div.find('p')
#         if heading and paragraph:
#             if heading.get_text() == "College Infrastructure":
#                 College_Infrastructure.append(paragraph.get_text())
#             elif heading.get_text() == "Academics":
#                 Academics.append(paragraph.get_text())
#             elif heading.get_text() == "Placements":
#                 Placements.append(paragraph.get_text())
#             elif heading.get_text() == "Campus Life":
#                 Campus_Life.append(paragraph.get_text())
#             elif  heading.get_text() == "Anything Else":
#                 Anything_Else.append(paragraph.get_text())

#     return College_Infrastructure,Academics,Placements,Campus_Life,Anything_Else


# def scrap(id):
#     try:
#         College_Infrastructure = []
#         Academics = []
#         Placements = []
#         Campus_Life = []
#         Anything_Else = []
#         for i in range(1,10):
#             College_infra,Academic, Placement,Campus_Lyf,Any_Else = Scraping(id,i)
#             College_Infrastructure += College_infra
#             Academics += Academic
#             Placements += Placement
#             Campus_Life += Campus_Lyf
#             Anything_Else += Any_Else
#     except:
#         pass
#     data = {}
#     data["College_Infrastructure"] = College_Infrastructure
#     data["Academics"] = Academics
#     data["Placements"] = Placements
#     data["Campus_Life"] = Campus_Life
#     data["Anything_Else"] = Anything_Else
#     return data


import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def Scraping(id, page):
    url = f"https://www.careers360.com/colleges/reviews?page={page}&college_id={id}"
    
    # More robust proxy configuration
    proxies = [
        {"http": "http://pehgjxwr:j7u0qyb1xux8@198.23.239.134:6540"},
        {"http": "http://pehgjxwr:j7u0qyb1xux8@207.244.217.165:6712"}
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    College_Infrastructure = []
    Academics = []
    Placements = []
    Campus_Life = []
    Anything_Else = []

    for proxy_config in proxies:
        try:
            response = requests.get(url, proxies=proxy_config, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.find_all('div', class_='detail_content_review')

            if not divs:
                logger.warning(f"No reviews found on page {page} with proxy {proxy_config}")
                continue

            for div in divs:
                heading = div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                paragraph = div.find('p')
                
                if heading and paragraph:
                    text = paragraph.get_text().strip()
                    if text:  # Only add non-empty texts
                        if heading.get_text() == "College Infrastructure":
                            College_Infrastructure.append(text)
                        elif heading.get_text() == "Academics":
                            Academics.append(text)
                        elif heading.get_text() == "Placements":
                            Placements.append(text)
                        elif heading.get_text() == "Campus Life":
                            Campus_Life.append(text)
                        elif heading.get_text() == "Anything Else":
                            Anything_Else.append(text)

            if College_Infrastructure or Academics or Placements or Campus_Life or Anything_Else:
                logger.info(f"Successfully scraped reviews from page {page}")
                break

        except requests.RequestException as e:
            logger.error(f"Request failed with proxy {proxy_config}: {e}")

    return College_Infrastructure, Academics, Placements, Campus_Life, Anything_Else

def scrap(id):
    all_reviews = {
        "College_Infrastructure": [],
        "Academics": [],
        "Placements": [],
        "Campus_Life": [],
        "Anything_Else": []
    }

    max_pages = 10
    reviews_found = False

    for page in range(1, max_pages + 1):
        College_infra, Academic, Placement, Campus_Lyf, Any_Else = Scraping(id, page)
        
        all_reviews["College_Infrastructure"].extend(College_infra)
        all_reviews["Academics"].extend(Academic)
        all_reviews["Placements"].extend(Placement)
        all_reviews["Campus_Life"].extend(Campus_Lyf)
        all_reviews["Anything_Else"].extend(Any_Else)

        # Stop if no new reviews are found
        if College_infra or Academic or Placement or Campus_Lyf or Any_Else:
            reviews_found = True
        elif reviews_found:
            break

    if not any(all_reviews.values()):
        logger.warning(f"No reviews found for college ID {id}")

    return all_reviews