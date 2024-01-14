#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Data Extraction


# In[6]:


get_ipython().system('pip install requests bs4')


# In[7]:


import urllib.request as urllib2
from bs4 import BeautifulSoup


# In[8]:


get_ipython().system('pip install selenium')


# In[23]:


get_ipython().system('pip install tabulate')


# In[10]:


### This code has a potential delay in displaying output due to the large number of movie values being scraped from the website


# In[15]:


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate  # Import tabulate

# Initialize the Selenium WebDriver without specifying executable_path
driver = webdriver.Chrome()

# Step 1: Access the URL
url = "https://www.rottentomatoes.com/browse/movies_at_home/"
driver.get(url)

# Initialize a WebDriverWait with a timeout
wait = WebDriverWait(driver, 10)

# Click the "Load More" button repeatedly until all content is loaded
while True:
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="dlp-load-more-button"]')))
        load_more_button.click()
        time.sleep(3)  # Add a delay to allow the content to load
    except Exception as e:
        break

# Extract the page source after loading all content
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Extract movie information as before
movie_elements = soup.find_all(['a', 'div'], attrs={'data-track': 'scores', 'data-qa': 'discovery-media-list-item-caption'})

movie_names = []
tomatometer_values = []
audience_scores = []

for movie_element in movie_elements:
    # Extract movie name
    movie_name = movie_element.find('span', attrs={'data-qa': 'discovery-media-list-item-title'}).text.strip()
    movie_names.append(movie_name)

    # Extract tomatometer value
    score_pairs = movie_element.find('score-pairs')
    tomatometer = score_pairs['criticsscore']
    tomatometer_values.append(tomatometer)

    # Extract audience score
    audience_score = score_pairs['audiencescore']
    audience_scores.append(audience_score)


# In[16]:


# Data Transformation


# In[17]:


# Step 3: Store the scraped data in a DataFrame
data = {'Movie Name': movie_names, 'Tomatometer Value': tomatometer_values, 'Audience Score': audience_scores}
df = pd.DataFrame(data)


# In[18]:


df


# In[19]:


# Data Presentation


# In[22]:


# Step 4: Create and display a table using tabulate

# Convert DataFrame to a list of dictionaries
data_dict = df.to_dict(orient='records')

# Print the data as a table using tabulate
table = tabulate(data_dict, headers='keys', tablefmt='grid')

# Display the table
print(table)

