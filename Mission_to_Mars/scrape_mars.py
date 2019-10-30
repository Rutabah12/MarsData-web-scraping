#!/usr/bin/env python
# coding: utf-8

# In[13]:


from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 


# In[14]:


# In[ ]:





# In[15]:



def scrape(): 

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser=Browser('chrome', **executable_path, headless=False)
    mars_info = {}

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p


    # ## NASA MARS NEWS

    # ## MARS Image 

    # In[16]:



    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    img = image_soup.select_one("figure.lede a img")
    img_url = img.get("src")
    
    mars_info["img_url"]= base_url + img_url


    # ## Weather Data 

    # In[17]:



    # Visit the Mars Weather Twitter Account
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    
    # Parse Results HTML with BeautifulSoup
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    
    # Find a Tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
    # Search Within Tweet for <p> Tag Containing Tweet Text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    
    mars_info["mars_weather"]=mars_weather


    # In[ ]:





    # ## Mars Facts 

    # In[18]:



    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[1]


    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()
    
    mars_info["data"]=data


    # ## Mars Hempisphere 

    # In[19]:


    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hem = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hem.append({"title" : title, "img_url" : img_url})
        
        mars_info["hem"]=hem

    


        # In[ ]:





        # In[ ]:


    browser.quit()


# In[ ]:


    return mars_info




# In[ ]:



