import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from helpers.driver import chrome_driver
from helpers.image import resize_image, save_image_from_url
from helpers.url import get_hostname
from providers.provider import Provider, ProviderData


class MalayMail(Provider):
    def __init__(self, url):
        super().__init__(url)
        self.fetch_data()

    def fetch_data(self):
        driver = chrome_driver()
        driver.get(self.url)

        # Wait for page load
        time.sleep(2)

        # Fetch title
        title = driver.find_element(By.CLASS_NAME, "article-title").text
        
        # Fetch author (always the last word in the third <p> element in the article body)
        author_element = driver.find_elements(By.CSS_SELECTOR, ".article-body p")[-3]  # Last 3rd <p> element
        author = author_element.text.split()[-1]  # Last word in the <p> (assuming it's the author's name)
        author = f"<p>By {author}</p>"

        # Fetch article body
        articles = driver.find_elements(By.CLASS_NAME, "article-body p")
        articles = list(map(lambda x: x.text, articles))  # Get the text of each <p> element
        # Fetch article body and add a <br> after each <p>
        articles_string = '<br>'.join([f"<span>{article}</span>" for article in articles])

        # Fetch article image (within the article image gallery and layout ratio)
        image_url = None
        try:
            image_tag = driver.find_element(By.CSS_SELECTOR, '.article-image-gallery .layout-ratio picture img')
            image_url = image_tag.get_attribute('src')
        except:
            print("No image found or failed to locate image.")

        image = save_image_from_url(image_url)
        scaled_image = resize_image(image)

        # Construct the content and source
        articles_string = '\n'.join(articles)
        # Get the second-to-last part of the URL
        paths = self.url.split('/')
        path = paths[-2]  # This gets the second-to-last segment
        source_p = f"""
        <p>
             <strong>Source: </strong><a href="{self.url}">{path}</a>
        </p>
        """
        content = f"<p>{author}</p>{articles_string}&nbsp;{source_p}"

        # Excerpt (first paragraph)
        excerpt = articles[0] if articles else "No content available."

        # Tags (empty as per your instruction)
        tags = ""

        # Store the scraped data
        self.data = ProviderData(
            title=title,
            content=content,
            image=scaled_image,
            excerpt=excerpt,
            tags=tags
        )


if __name__ == '__main__':
    url = 'https://www.malaymail.com/some-article'  # Replace with a real article URL
    provider = MalayMail(url)

    # The data is stored in provider.get_data(), no need to print unless you need to use the data.
    data = provider.get_data()

    # You can use the `data` object for further processing or store it as needed, but no print required here.
