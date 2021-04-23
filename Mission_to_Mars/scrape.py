from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    url=("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    driver.get(url)
    html = driver.page_source
    soup = bs(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    featured_image = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars3.jpg'

    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)

    mars_facts_df = tables[2]
    mars_facts_df.columns = [" ", "Mars"]
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')

    primary_url = 'https://astrogeology.usgs.gov'
    url=("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    driver.get(url)
    html = driver.page_source
    soup = bs(html, 'html.parser')

    mars_hemisphere= soup.find('div',class_='collapsible results')
    hemispheres= mars_hemisphere.find_all('div',class_='item')
    hemisphere_urls = []

    for h in hemispheres:
        hemisphere = h.find('div',class_='description')
        title = hemisphere.h3.text
        
        hemi_image = hemisphere.a["href"]  
        driver.get(primary_url + url)
        html=driver.page_source
        soup=bs(html,'html.parser')
        image_src=soup.find('li').a['href']
        
        hemisphere_dict={
            'title':title,
            'image_url':image_src
            }
        hemisphere_urls.append(hemisphere_dict)


    return_data = {"title": news_title, 
                    "paragraph": news_p, 
                    "featured_image": featured_image, 
                    "html_table": mars_html_table, 
                    "hemisphere_images": hemisphere_urls }
    driver.close()
    return return_data
    

    if __name__ == "__main__":
    print(scrape_info() )