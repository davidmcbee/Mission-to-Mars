#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': "./Resources/chromedriver.exe"}
browser = Browser('chrome', **executable_path)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# ### Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df
df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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
        browser.back
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()



