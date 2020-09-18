# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {"executable_path" : "chromedriver.exe"}
    browser = Browser("chrome", "chromediriver", headless=False)
    
    news_title, news_paragraph, = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "Mars_hemispheres": Mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Set the executable path and initialize the chrome browser in splinter
# browser = Browser('chrome', **executable_path)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    print(img_url)
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe   
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def Mars_hemispheres(browser):
    # Pulls the 4 Mars hemispheres
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    base_page = soup(html, 'html.parser')
    # Define base part of url
    base_part = 'https://astrogeology.usgs.gov'
    # create loop to get the 4 linking urls and title 
    for thumb in base_page.find_all('div', class_= 'item'):
        # access the page with the .jpg pics and pu tthem and the title in a dictionary
        for item in thumb.find_all('div', class_= 'description'):
            base_url = item.find('a').get('href')
            tit = item.find('h3').get_text()
            #print(base_url)
            #print(tit)
            full_link_url = base_part + base_url
            #print(full_link_url)
            browser.visit(full_link_url)
            new_html = browser.html
            soupy = soup(new_html, 'html.parser')
            to_get = soupy.find('div', class_= 'downloads')
            temp = to_get.find('a').get('href')
            #print(temp)
            dict = {'img_url' : temp, 'title' : tit}
            hemisphere_image_urls.append(dict)
            #browser.back
    return(hemisphere_image_urls)


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())