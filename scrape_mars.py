
# coding: utf-8

# In[245]:

#import dependencies
from bs4 import BeautifulSoup as bs
from splinter.exceptions import ElementDoesNotExist
from splinter import Browser
from selenium import webdriver
import pandas as pd
import os
import time
import datetime as dt


# In[246]:
def scrape():
    # browser = init_browser()

    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    # get_ipython().system('which chromedriver/')



    # visit the NASA Mars News site and scrape headlines
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)


    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    import time
    time.sleep(1)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")


    # In[88]:


    # save the most recent article, title
    news_title  = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    # print(f"Title: {news_title}")
    # print(f"Para: {news_paragraph}")
    # Create a dictionary for all of the scraped data
    mars_dict = {}
    mars_dict["news_title"] = news_title
    mars_dict["news_paragraph"] = news_paragraph

    # # JPL Mars Space Images - Featured Image

    # In[90]:


    # Visit the JPL Mars URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Setting up splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    #visiting the page
    browser.visit(url)
    import time
    # Moving through the pages
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)


    # In[91]:


    #using bs to write it into html
    html = browser.html
    soup = bs(html, "html.parser")

    # Get featured image
    results = soup.find("article")
    extension = results.find("figure", class_="lede").a["href"]
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension
    # print(featured_image_url)

    mars_dict["featured_image_url"] = featured_image_url

    # # Mars Weather

    # In[253]:


    #Get mars weather, THE INSTRUCTIONS SAY SPECIFICALLY TO SCRAPE THE DATA

    url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    # twitter_soup = bs(twitter_response, 'html.parser')


    # In[257]:



    # #temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    # print(mars_weather)
    #temp

    
    # In[258]:

    
    for i in range(30):
        tweets = mars_weather[i].text
#         global weather
        if "Sol " in tweets:
            weather =tweets
#         print(tweets)
            break
    # mar_weather=weather
    # mars_dict["mar_weather"] = mar_weather

    mar_weather=weather
    mars_dict["mar_weather"] = mar_weather
    # print(mar_weather)

    # # Mars Facts

    # In[260]:


    #Mars Facts....visit webpage, use pandas to scrape the page for facts, 
    #convert pandas table to html table string. 
    mars_facts_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(mars_facts_url)
    mars_fact_df=mars_table[0]
    


    # In[262]:


    # Setting columns and index
    mars_fact_df.columns = ["Parameter", "Values"]
    mars_fact_df = mars_fact_df.set_index(["Parameter"])

    # Converting to Html
    mars_html_table = mars_fact_df.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    # mars_html_table


    # OSX Users can run this to open the file in a browser, 
    # or you can manually find the file and open it in the browser
    
    #!open mars_html_table.html

    # Empty dictionary for info
    mars_dict["mars_html_table"] = mars_html_table

    # # Mars Hemispheres

    # In[243]:


    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")
    
    
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        import time
        time.sleep(2)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})


# In[244]:

    mars_dict["mars_hemisphere"] = mars_hemisphere
    mars_dict["TimeStamp"]=dt.datetime.now()
    return mars_dict
