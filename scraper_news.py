from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import logging
import asyncio
import uuid


def setup_driver():
    '''
    This function initializes the Selenium WebDriver with headless Chrome options for running without GUI.
    '''
    
    options = Options()
    options.add_argument('--headless') # Utiliser chrome_driver sans interface graphique
    options.add_argument('--no-sandbox') # Pour éviter les problèmes de sécurité dans certains environnements
    options.add_argument('--disable-dev-shm-usage') # Pour éviter les erreurs de mémoire dans des environnements limités
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#Chargement des articles  
def load_more_articles(driver):
    '''
    This function clicks the "load more" button up to 50 times to fetch more articles from the page.
    '''

    for _ in range(50):
        try:
            load_more = driver.find_element(By.ID, 'justin-load-more-button')
            load_more.click()
        except (NoSuchElementException, ElementClickInterceptedException):
            break


#Extraire les articles sur le site
async def extract_articles(article):
    '''
    This async function extracts the title, date, and link from a single article element. 
    It skips video links and returns a dictionary.
    '''

    try:
        link = article.find_element(By.CLASS_NAME, 'c-timeline-items__article__link').get_attribute('href')
        if '/watch-' not in link and '/video/' not in link:
            date = article.find_element(By.CLASS_NAME, 'c-item-date').text
            time = article.find_element(By.CLASS_NAME, 'c-item-time').text + ' GMT+1'
            title = article.find_element(By.TAG_NAME, 'h2').text
            
            return {
                'title': title,
                'link': link,
                'date_time': f"{date} {time}"
            }
    except NoSuchElementException as e:
        print("error", e)


#Recuperation du contenu des articles
async def get_article_content(driver, article):
    '''
    This async function visits the article link, extracts all text paragraphs from the article body,
    and returns a dictionary with article metadata and content.
    '''

    try:
        logging.info(f"Extraction de {article['link']}")
        driver.set_page_load_timeout(130)
        driver.get(article['link'])
        paragraphs = driver.find_elements(By.XPATH, '//*[@id="poool-content"]/p')
        body = " ".join(paragraph.text for paragraph in paragraphs)
        if body != "":
            article_id = str(uuid.uuid4())
            logging.info("extraction reussi")
            return{  
                'Id': article_id,
                'Url': article['link'],
                'Date': article['date_time'],
                'Headline': article['title'],
                'Body': body
            }
        else: 
            print("pas de body dans l'article")
            return None
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'article : {e}")
        return {}


#Fonction principale
async def scraper_news():
    '''
    This is the main asynchronous function. It sets up the driver, loads more articles,
    extracts summaries and full content, and writes results to a CSV file.
    '''
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers={
            logging.FileHandler('scraping.log'),
            logging.StreamHandler()
        }
    )
    try:
        logging.info('Configuration du driver')
        driver = setup_driver()

        logging.info('Requete vers la page a scraper')
        driver.get('https://www.euronews.com/just-in')
        # driver.find_element(By.ID, 'didomi-notice-agree-button').click() #accepter les cookies
        
        logging.info('Chargement des articles')
        load_more_articles(driver)

        logging.info('Extraction des articles')
        article_elements = driver.find_elements(By.CLASS_NAME, 'c-timeline-items__content')
        article_tasks = [extract_articles(article) for article in article_elements]
        articles = await asyncio.gather(*article_tasks)

        logging.info('Recuperation du contenu des article')
        news_tasks = [get_article_content(driver, article) for article in articles]
        scraped_news = await asyncio.gather(*news_tasks)
        
        # Filtrer les entrées None
        valid_news = [article for article in scraped_news if article is not None]
        df = pd.DataFrame(valid_news)
        df.dropna(axis=0, inplace=True)
        
        # Supprimer les doublons basés sur l'URL
        print(f'\nnombre de lien unique{df['Url'].nunique()}\n')
        df.drop_duplicates(subset=['Url'], inplace=True)
        print(df)
        df.to_csv('data/scraped_news.csv', index=False)
       
       #Fermetture du navigateur
        driver.quit()
    except Exception as e:
        logging.error(f"Une erreur s'est produite: {str(e)}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(scraper_news())