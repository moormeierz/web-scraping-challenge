#!/usr/bin/env python
# coding: utf-8

# In[7]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager


# In[10]:

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # # Scrape Title & Paragraph

    # In[3]:


    # URL that we need to scrape
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)


    # In[4]:


    # Create Beautiful Soup object
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')


    # In[5]:


    # Get title and body paragraph
    mars_news_title = news_soup.find_all('div', class_='content_title')[1].text
    body_par = news_soup.find_all('div', class_='article_teaser_body')[0].text

    print(mars_news_title)
    print(body_par)


    # # Scrape Image

    # In[6]:


    # image url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)


    # In[7]:


    # Create Beautiful Soup object
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')


    # In[8]:


    # Get image url
    image_path = image_soup.find_all('img')[2]['src']
    print(image_path)


    # # Scrape Table

    # In[9]:


    # table url
    table_url = 'https://space-facts.com/mars/'
    browser.visit(table_url)


    # In[10]:


    # Create Beautiful Soup object
    html = browser.html
    table_soup = BeautifulSoup(html, 'html.parser')


    # In[11]:


    # print all scraped tables
    raw_tables = pd.read_html(table_url)
    raw_tables


    # In[12]:


    # Identify the right table
    needed_table = raw_tables[2]
    needed_table


    # In[13]:


    # name columns and set index
    needed_table.columns = ["Description", "Value"]
    needed_table.set_index('Description', inplace = True)
    needed_table


    # In[14]:


    html_table = needed_table.to_html()
    html_table


    # In[15]:


    print(html_table)


    # # Scrape Hemispheres

    # In[16]:


    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)


    # In[17]:


    # Create Beautiful Soup object
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')


    # In[18]:


    # Scrape titles
    titles=hemi_soup.find_all('h3')
    titles[:]=(title.text for title in titles)
    titles[:]=(title.split(" Enhanced")[0] for title in titles)
    titles.remove('Back')
    print(titles)


    # In[19]:


    # Scrape Images
    hemisphere_image_urls=[]
    for title in titles:
        browser.visit(hemi_url)
        browser.links.find_by_partial_text(title).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url=soup.find('div',class_='downloads').ul.li.a['href']
        print(hemi_url+img_url)
        hemisphere_image_urls.append({"title": title, "final_url": hemi_url + img_url})

    print(hemisphere_image_urls)


    # In[20]:


    # put everything into one dictionary
    mars_dict = {'mars_news_title' : mars_news_title, 'body_par' : body_par, 'image_path' : image_path, 'html_table': html_table,
                'hemisphere_image_urls': hemisphere_image_urls}
    mars_dict


    # In[21]:


    # Quit session
    browser.quit()




    return mars_dict