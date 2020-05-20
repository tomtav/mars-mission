# import dependencies
import os
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def scrape():

    # configure browser path for MacOS
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    # NASA Mars News
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'

    # visit website
    browser.visit(url)

    # wait a few seconds for page to fully load
    sleep(10)

    # retrieve the latest news titles from the page
    latest_news_title = browser.find_by_css(
        '.slide').first.find_by_css('.content_title').first.value

    # retrieve the latest news descriptions for the latest news titles from the page
    latest_news_caption = browser.find_by_css(
        '.slide').first.find_by_css('.article_teaser_body').first.value

    # close browser
    browser.quit()

    # JPL Mars Space Images
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # visit website
    browser.visit(url)

    # click through to full image page
    browser.click_link_by_partial_text('FULL IMAGE')

    # click through to the details page
    browser.click_link_by_partial_text('more info')

    # retrieve
    featured_image_url = browser.links.find_by_partial_href(
        'largesize').first['href']

    # close browser
    browser.quit()

    # Mars Weather

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)

    # parse the html retrieved
    soup = BeautifulSoup(response.text, 'html.parser')

    # retrieve the latest tweet
    mars_weather = soup.find('div', class_='tweet', attrs={'data-screen-name': 'MarsWxReport'}).find(
        'p', 'tweet-text').text.replace('\n', ' ').split('pic.twitter.com/')[0]

    # Mars Facts
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    # scrape any tabular data from the page and select the first table
    mars_facts = pd.read_html(url)[0]

    # rename columns
    mars_facts = mars_facts.rename(
        columns={0: 'Description', 1: 'Value'}).set_index('Description')

    # convert pandas dataframe to html table
    mars_facts_table = mars_facts.to_html().replace('\n', '')

    # Mars Hemispheres
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # visit main page
    browser.visit(url)

    # array to store hemisphere image urls
    hemisphere_image_urls = []

    # generate list of each hemisphere's detail page url
    links = [item.find_by_tag('a').first['href'] for item in browser.find_by_css(
        '.results').find_by_css('.description')]

    # loop through each detail page by visiting each url
    try:
        for link in links:
            browser.visit(link)
            title = browser.find_by_css('.title').first.text
            img_url = browser.links.find_by_text('Original').first['href']
            hemisphere_image_urls.append(
                {'title': title.replace(' Enhanced', ''), 'img_url': img_url})
            sleep(3)

    except ElementDoesNotExist:
        print("hemispheres data scraping completed")

    # close browser
    browser.quit()

    # python dictionary of all scraped data
    return {
        'news': {
            'title': latest_news_title,
            'caption': latest_news_caption
        },
        'featured_image_url': featured_image_url,
        'weather': mars_weather,
        'facts': mars_facts_table,
        'hemispheres': hemisphere_image_urls
    }
