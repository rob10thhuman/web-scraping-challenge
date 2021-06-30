from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import sys

def scrape():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://mars.nasa.gov/news/')
    news_title = driver.find_elements_by_class_name('list_text')
    news_p = driver.find_elements_by_class_name('article_teaser_body')

    news_list = []
    news_p_list = []

    for x in news_title:
    	news_list.append(x.get_attribute("textContent"))

    for y in news_p:
    	news_p_list.append(y.get_attribute("textContent"))

    driver.quit()

    # print(news_list)

    driver2 = webdriver.Chrome(ChromeDriverManager().install())
    driver2.get('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    featured_image_url = driver2.find_elements_by_tag_name('img')
    images = []
    for image in featured_image_url:
        images.append(image.get_attribute('src'))
    driver2.quit()

    # print(images)

    matches = [match for match in images if 'featured' in match]
    # print(matches)

    driver_mars_facts = webdriver.Chrome(ChromeDriverManager().install())
    driver_mars_facts.get('https://space-facts.com/mars')
    mars_facts = driver_mars_facts.find_elements_by_class_name('column-1')
    mars_facts2 = driver_mars_facts.find_elements_by_class_name('column-2')
    facts = []
    facts2 = []
    for x in mars_facts:
        facts.append(x.text)
    for x in mars_facts2:
        facts2.append(x.text)
    driver_mars_facts.quit()

    # print(facts)
    # print(facts2)

    marsFacts = pd.DataFrame(facts)

    marsFacts[1] = pd.DataFrame(facts2)

    marsFacts = marsFacts.drop([0, 1, 2, 3, 4, 5, 6, 7, 8])

    # print(marsFacts)

    marsTable = marsFacts.to_html()
    marsTable = marsTable.replace('\n','')

    import time 
    driver_mars_hemi = webdriver.Chrome(ChromeDriverManager().install())
    driver_mars_hemi.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    names = []
    urls = []

    for i in range(4):
        time.sleep(3)
        hemisphere = driver_mars_hemi.find_elements_by_tag_name('h3')
        hemisphere[i].click()
        time.sleep(5)
        hemi_title = driver_mars_hemi.find_element_by_tag_name('h2')
        hemi_url = driver_mars_hemi.find_element_by_class_name('wide-image')
        names.append(hemi_title.text)
        urls.append(hemi_url.get_attribute('src'))
        driver_mars_hemi.back()
        time.sleep(3)

    driver_mars_hemi.quit()

    # print(names)
    # print(urls)
    hemisphere_img_urls = {names[i]: urls[i] for i in range(len(names))}
    hemisphere_img_urls = [{'title':i, 'img_url':j} for i, j in hemisphere_img_urls.items()]
    # print(hemisphere_img_urls)

    mars_data = ({
       "featured_image_url": matches,
       "table": marsTable,
       "hemispheres": hemisphere_img_urls,
       "news_title": news_list,
       "news_body": news_p_list
    })

    print(mars_data)

    return(mars_data)


# if __name__ == '__main__':
#     globals()[sys.argv[1]]()
