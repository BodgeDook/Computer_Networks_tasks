from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

EMAIL = "yourCNNemail@example.com"
PASSWORD = "yourCNNpassword"

def parse_page(url: str):

    driver = webdriver.Firefox()
    driver.get(url) # https://edition.cnn.com/account/log-in (out goal site for parsing)
    wait = WebDriverWait(driver, 10)

    # cookie banner closing:
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept All')]")))
        cookie_button.click()
        print('Banner was passed...\n')
        time.sleep(2)
    except Exception:
        print("Cookie banner didn't appear...\n")

    # authorization:
    email_input = wait.until(EC.element_to_be_clickable((By.NAME, "loginEmail")))
    email_input.send_keys(EMAIL)

    password_input = wait.until(EC.element_to_be_clickable((By.NAME, "loginPassword")))
    password_input.send_keys(PASSWORD)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign in')]")))
    login_button.click()
    time.sleep(5)

    driver.get("https://edition.cnn.com/business")
    time.sleep(2)

    news_hrefs = list(set([a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, "a[data-link-type='article']")]))
    news_hrefs = news_hrefs[:10]

    news_headliners = []
    publishing_dates = []
    news_authors = []
    sources = []

    for news_href in news_hrefs:
        driver.get(news_href)
        time.sleep(2)
        
        news_headliner = driver.find_element(By.CSS_SELECTOR, "h1[data-editable='headlineText']").text
        publish_date = driver.find_element(By.CSS_SELECTOR, "div[data-uri*='_components/timestamp/']").text
        news_author = driver.find_element(By.CSS_SELECTOR, "div[class^='byline__name']").text

        author_parts = news_author.rsplit(" ", 1)
        news_author = author_parts[0]
        source = author_parts[1] if len(author_parts) > 1 else 'CNN'
        
        publishing_dates.append(publish_date)
        news_headliners.append(news_headliner)
        news_authors.append(news_author)
        sources.append(source)
        
        print(f'{news_headliner} -> {publish_date} -> {news_author} -> {source}\n')
    
    print('done')
    driver.quit()

    # authors cleaning:
    clean_authors = []
    for author in news_authors:
        author = author.replace("By ", "").strip(",").strip()
        if author.lower() == "by" or not author:
            author = "Author wasn't found"
        clean_authors.append(author)

    results = []
    for headline, date, author, source in zip(news_headliners, publishing_dates, clean_authors, sources):
        results.append({
            "headline": headline,
            "date": date,
            "author": author,
            "source": source
        })

    return results