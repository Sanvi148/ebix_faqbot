import trafilatura

def extract_main_content(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text