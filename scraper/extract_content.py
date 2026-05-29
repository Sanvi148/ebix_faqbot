import requests
import trafilatura
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def extract_content(url):

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)

    time.sleep(5)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    print("BOD FOUND:", len(soup.select("div.bod")))

    driver.quit()
    chunks = []
    # ==================================================
    # 1. FAQ / Accordion Extraction
    # ==================================================

    faq_cards = soup.find_all("div", class_="card")
    if faq_cards:
        for card in faq_cards:
            question_tag = card.find(["h5", "h6"])
            answer_tag = card.find("div", class_="collapse")
            if question_tag and answer_tag:
                question = question_tag.get_text(" ", strip=True)
                answer = answer_tag.get_text(" ", strip=True)
                faq_chunk = f"Q: {question}\nA: {answer}"
                chunks.append(faq_chunk)

                
    director_cards = soup.select("div.bod")

    for card in director_cards:

        name_tag = card.find("div", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else ""

        designation_tag = card.find(
            "div", class_="designation"
        )
        designation = (
            designation_tag.get_text(strip=True)
            if designation_tag else ""
        )

        profile_link = card.find("a")

        target = ""

        if profile_link:
            target = profile_link.get("href", "")

        # remove #
        target = target.replace("#", "")

        profile_div = soup.find("div", id=target)

        description = ""

        if profile_div:
            paragraphs = profile_div.find_all("p")

            description = " ".join(
                p.get_text(" ", strip=True)
                for p in paragraphs
            )

        chunk = f"""
        Name: {name}

        Designation: {designation}

        Description:
        {description}
        """

        print(chunk)
        chunks.append(chunk)   
# # ==================================================
# # TAB + CONTENT GROUPING
# # ==================================================

#     tabs = soup.find_all("a", class_="nav-link")

#     for tab in tabs:

#         # Get tab heading
#         heading = tab.get_text(" ", strip=True)

#         # Get linked div id from href
#         target = tab.get("href")

#         if not target or not target.startswith("#"):
#             continue

#         # Remove #
#         target_id = target.replace("#", "")

#         # Find matching tab content
#         content_div = soup.find("div", id=target_id)

#         if content_div:

#             content_text = content_div.get_text(" ", strip=True)

#             final_chunk = f"{heading}\n\n{content_text}"

#             if len(content_text) > 50:
#                 chunks.append(final_chunk)
# ==================================================
# TAB + OFFICE EXTRACTION
# ==================================================

    tab_panes = soup.select("div.tab-pane")
    for pane in tab_panes:
        region = pane.get("id", "").replace("-", " ").title()
        office_cards = pane.select("div.col-md-4.col-lg-3.mb-4")
        for office in office_cards:
            city_tag = office.find("h6")
            address_tag = office.select_one("div.office_address p")
            email_tag = office.find("a", href=lambda x: x and "mailto:" in x)
            city = city_tag.get_text(" ", strip=True) if city_tag else ""
            address = (
                address_tag.get_text(" ", strip=True)
                if address_tag else ""
            )
            email = (
                email_tag.get_text(" ", strip=True)
                if email_tag else ""
            )
            if city or address or email:
                chunk = f"""
                    Region: {region}

                    City: {city}

                    Address:
                    {address}

                    Email:
                    {email}
                    """
                chunks.append(chunk)

    # ==================================================
    # 3. Article Extraction (Fallback)
    # ==================================================

    if not chunks:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        if text:
            chunks.append(text)

    print("\nTOTAL CHUNKS:", len(chunks))

    for chunk in chunks[:5]:
        print("\nCHUNK:")
        print(chunk)
    return chunks