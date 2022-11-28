import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()


def check_post():
    # Get last post url
    post_title, absolute_post_url = '', ''
    URL = os.getenv('URL')
    query = requests.get(URL)
    soup = BeautifulSoup(query.text, 'html.parser')
    post_url = soup.find('div', class_='container main content').find('h2').find('a').get('href')

    # Open a .csv file that stores the last post url
    with open('post.csv', 'r') as file:
        data = csv.DictReader(file)
        prev_post_url = next(data).get('post_url')

    # Compare link from a .csv file with the link received from the site
    # If the links don't match then prepare a message for telegram
    if prev_post_url != post_url:
        post_title = soup.find('div', class_='container main content').find('h2').find('a').text
        absolute_post_url = 'https://www.tesmanian.com/' + post_url
        data = {'post_url': post_url}

        # Overwrite link of the last post for next compare
        with open('post.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    # Return Post title and link to it as a result of function
    return post_title, absolute_post_url



def tel_send_message(post_title, post_link):
    # Telegram token to access the HTTP API:
    TEL_TOKEN = os.getenv('TEL_TOKEN')

    # All queries to the Telegram Bot API need to be presented
    # in this form: https://api.telegram.org/bot<token>/METHOD_NAME.
    tel_url = 'https://api.telegram.org/bot{token}/sendMessage'
    CHAT_ID = os.getenv('URL')

    # Use sendMessage Telegram method with 2 required parameters: chat_id, text
    # to send a message for a new post
    params = {
        'chat_id': CHAT_ID,
        'text': f'{post_title}\n {post_link}'
    }
    query_url = tel_url.format(token=TEL_TOKEN)
    query = requests.get(url=query_url, params=params)
    return query


def main():
    while True:
        post_title, post_url = check_post()
        if post_title and post_url:
            status = tel_send_message(post_title, post_url)
        sleep(15)


if __name__ == '__main__':
    main()




