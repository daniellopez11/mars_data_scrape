# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import html5lib

def scrape():

    # Define a empty dictionary to store all scraped data
    data_scrape_dict = {}   

    # NASA Mars news site scrape
    news_html = ""

    with Browser('chrome', headless=False) as browser:
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        news_html = browser.html
        
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(news_html, 'html.parser')

    results = soup.find_all('li', class_='slide')

    # Loop through returned results to collect the News Title and Paragragh Text
    news_title_all = []
    news_para_all = []

    for result in results:
        try:
            # Retrieve the title text
            title = result.find('h3')
            n_title = title.text
            news_title_all.append(n_title)

            # Retrieve the paragrah text
            para = result.find('div', class_='rollover_description_inner')
            n_para = para.text
            news_para_all.append(n_para)

        except:
            print("This is an error message!")

    # Save the most recent (1st on list) news article to variables and save to data_scrape_dict
    news_title = news_title_all[0]
    news_p = news_para_all[0]

    data_scrape_dict['news_title'] = news_title
    data_scrape_dict['news_p'] = news_p

    # JPL Mars Space Featured Image scrape
    # Url for jpl main site
    jpl_url = 'https://www.jpl.nasa.gov'

    image_html = ""

    with Browser('chrome', headless=False) as browser:
        url = jpl_url + '/spaceimages/?search=&category=Mars'
        browser.visit(url)
        image_html = browser.html
        
    soup = BeautifulSoup(image_html, 'html.parser')

    results = soup.find_all('div', class_='carousel_items')

    # Loop through returned results to collect image data
    for result in results:
        try:
            # Retrieve full image url
            image_link = result.a['data-fancybox-href']
            feat_image_url = jpl_url + image_link

        except:
            print("This is an error message!")

    # Save feat_image_url to data_scrape_dict
    data_scrape_dict['feat_image_url'] = feat_image_url

    # Twitter @MarsWxReport scrape
    weather_html = ""

    with Browser('chrome', headless=False) as browser:
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        weather_html = browser.html
       
    soup = BeautifulSoup(weather_html, 'html.parser')

    results = soup.find('div', class_='js-tweet-text-container')

    # Save the tweet text for the weather report to data_scrape_dict
    mars_weather = results.text.strip()
    data_scrape_dict['mars_weather'] = mars_weather

    # Mars facts url
    facts_url = 'https://space-facts.com/mars/'

    # Use Pandas to automatically scrape any tabular data from facts_url page
    table = pd.read_html(facts_url)

    # Make table scrape into a DataFrame
    df = table[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    # Generate HTML table from DataFrame and strip unwanted new lines and html table tag to clean up the table.
    html_table = df.to_html().replace('\n', '').replace('<table border="1" class="dataframe">', '').replace('</table>', '')

    # Save html_table to data_scrape_dict
    data_scrape_dict['html_table'] = html_table

    # Mar's hemispheres image scrape
    # Urls for hemisphere images
    hemisphere_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
                       'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                       'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                       'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
                      ]

    image_html = ""

    usgs_url = 'https://astrogeology.usgs.gov'

    hemisphere_image_urls = []

    # Obtain images for each of Mar's hemispheres using for loop.
    # The image url string for the full res hemipshere image & title are saved in individual dicts. 
    # Dicts are saved in a list, hemisphere_image_urls.
    for hemi_url in hemisphere_urls:

        with Browser('chrome', headless=False) as browser:
            url = hemi_url
            browser.visit(url)
            image_html = browser.html

        soup = BeautifulSoup(image_html, 'html.parser')
        
        title_results = soup.find('h2', class_ = 'title')
        
        for result in title_results:
            title = title_results.text

        image_results = soup.find_all('img', class_='wide-image')
        
        for result in image_results:
            image_link = result['src']
            image_url = usgs_url + image_link
            
        # Make individal dict for each hemisphere
        img_dict = {
            'title': title,
            'image_url': image_url
        }
        
        # Append dict to hemisphere_image_urls list
        hemisphere_image_urls.append(img_dict)

    # Save hemisphere_image_urls to data_scrape_dict
    data_scrape_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return data_scrape_dict

