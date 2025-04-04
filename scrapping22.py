import requests
from bs4 import BeautifulSoup

def Scraping(id, page):
    # url = f"https://engineering.careers360.com/colleges/reviews?page={page}&college_id={id}"
    url = f"https://www.careers360.com/colleges/reviews?page={page}&college_id={id}"

    # Send request without proxies for testing
    try:
        response = requests.get(url, timeout=10)  # Added timeout to avoid hanging requests
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return [], [], [], [], []

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return [], [], [], [], []

    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='detail_content_review')

    College_Infrastructure = []
    Academics = []
    Placements = []
    Campus_Life = []
    Anything_Else = []

    for div in divs:
        heading = div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraph = div.find('p')

        if heading and paragraph:
            text = heading.get_text(strip=True)
            review = paragraph.get_text(strip=True)

            if text == "College Infrastructure":
                College_Infrastructure.append(review)
            elif text == "Academics":
                Academics.append(review)
            elif text == "Placements":
                Placements.append(review)
            elif text == "Campus Life":
                Campus_Life.append(review)
            elif text == "Anything Else":
                Anything_Else.append(review)
    
    return College_Infrastructure, Academics, Placements, Campus_Life, Anything_Else


def scrap(id):
    data = {
        "College_Infrastructure": [],
        "Academics": [],
        "Placements": [],
        "Campus_Life": [],
        "Anything_Else": []
    }

    for i in range(1, 10):  # Scraping first 10 pages
        College_infra, Academic, Placement, Campus_Lyf, Any_Else = Scraping(id, i)

        if not College_infra and not Academic and not Placement and not Campus_Lyf and not Any_Else:
            print(f"No data found on page {i}. Stopping further requests.")
            break  # Stop further scraping if pages are empty

        data["College_Infrastructure"] += College_infra
        data["Academics"] += Academic
        data["Placements"] += Placement
        data["Campus_Life"] += Campus_Lyf
        data["Anything_Else"] += Any_Else

    return data
