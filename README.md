# Mission-to-Mars
## Background and Purpose
Robin is interested in getting a job with NASA as she has always been interested in Mars. To help her fulfil this dream she
has decided to build a website to collect and display various information about Mars. Her hopes are that this will get
noticed by NASA and thus help her in her quest to become a NASA employee.

## Project Overview
To create this website Robin accomplished the following steps:
1. Robin used python. Using Jupyter Notebook to create her scraping she went to the following websites to scrape relevant data.
* to collect the latest news regarding Mars she went to https://mars.nasa.gov/news/
* To collect featured images she went to https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
* To provide basic facts on Mars she went to http://space-facts.com/mars/
2. To scrape parts from each of these websites she used Splinter, which automates the scraping process. This required the use of
chromedriver. Along with Splinter she used BeautifulSoup. BeautifulSoup helps to locate the parts of html that will be scraped.
Additionally, she used Pandas to help collect and organize her data in Jupyter notebook
3. Once the data is collected she will store it in a Mongo database. The choice for using Mongo DB is because the data she
collects is not structured. There are tables, articles and images.
4. to tie the scraping retrieval, the storage and to display this data in a webpage, Robin used Flask.
This environment can be logically viewed in Figure 1. Below
![](https://github.com/davidmcbee/Mission-to-Mars/blob/master/images/fig_1_env.png)


## Results
Lets look at the results as the process of scraping, storage and displaying occurs.

### Scraping
The scraping python code was developed in Jupyter Notebook and is available to view here
(ipynb file)
1. the news article was scraped by using Splinter and beautifulSoup to get the content title and the article_teaser_body
2. The Feature image was scraped by using Splinter and beautifulSoup to get the src (the image url) by filtering on figure.lede and a img.
This relative path url was joined to the base url.
3. The Mars facts were scraped and put into a dataframe and then converted to html.
4. The four Mars hemispheres were scraped by:
 a. getting the titles from the h3 tags.
 b. first finding the thumbnail image links to the full resolution images.
 c. the thumbnail relative urls were joined with the base url and then the code navigated to the page with those full resolution images.
 d. the full resolution images were found filtering to "div", class "downloads" and from there to "a" and "href".
 c. the full resolution images were pulled and joined to the base urls.
 d. the image titles and the full resolution images were put into a list of dictionaries.
 e. This code was moved and cleaned into a scraping.py file so it could be used by the app.py file
### Storing
The app file was created, viewable here
(app.py file)
This code uses Flask and PyMongo (so the python can interact with the Mondo DB).
the file does the following:
1. imports the scraping file.
2. configures the Mongo DB.
3. Creates the web page
 a. Creates the homepage route
 b. Creates the scraping route
The app. py file is the file that is executes. it uses the scraping file to do the scraping and it stores the scraped information in
the Mongo DB. It uses the homepage route along with the index.html file to create the web page.

### The Web Page
the index.html file was created to configure the web page and display the scraped information from Mongo DB. Relevant parts are:
1. Creates a head that configures the overall page and provides a title.
2. Creates a jumbotron container. This is where the title and a button to "Scrape Ne Data" goes.
3. Adds a section for the Mars news
4. Adds a section for the featured image and the Mars fact table
5. Adds a section for the four Mars hemisphere images and titles

## The End Product
The top half of the web page is shown here in figure 2
![](top half)

Figure 2

### Top Area
The jumbotron area can be seen as the light grey area with the title "Mission to Mars. It also hold the "Scrape New Data" button.
When the button is clicked the app.py app will direct the scraping app to update the data from the three websites.
Below the jumbotron is the latest news article - "Latest Mars News."
Below the news article is the featured image and to its right is the Mars Fact Table.
#### Deliverable 3 Bootstrap items
To make this view as clean and crisp as possible, BootStrap functionality was used to:
1. change the "Scrape New Data" button black. To do this the index.html file was modified to add a style for the new button look.
The black better matches the look of the web page.
2. The Facts Table was modified. prior to this image, Figure 2. The facts table was to close to the featured image and the title
was to small as compared to the featured image title. The fact table was put into a container with a class of container-fluid. This
allowed its movement to better align the table within the right 4 columns in the grid. The title was changed to "h2." this made it consistent with the featured image title.
3. You can also see from figure 3, that this page will work with mobile devices.
![](mobile)

Figure 3
### Bottom Area
The bottom half of the web page, shown here in figure 4
![](bottom half

Figure 4

Each of the four Martian hemispheres are shown along with their titles. I thought of creating four thumbnail sized images so that they would all be in a row but
I left them as four larger images to see the full value from their high resolution
