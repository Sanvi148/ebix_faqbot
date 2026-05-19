import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://ebixcash.com/"


def get_all_urls(base_url):
    """
    Crawls website and returns all internal URLs.
    """

    visited = set()
    to_visit = [base_url]

    while to_visit:

        url = to_visit.pop()

        if url in visited:
            continue

        visited.add(url)

        try:
            response = requests.get(url, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):

                full_url = urljoin(base_url, link["href"])

                if full_url.startswith(base_url):

                    if full_url not in visited:
                        to_visit.append(full_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    return list(visited)
