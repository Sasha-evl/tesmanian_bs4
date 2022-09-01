import requests
from bs4 import BeautifulSoup
import csv

from time import sleep

# Telegram token to access the HTTP API:
TEL_TOKEN = '5345879008:AAFwcrd_0a1kmVoFDfqmTp-KdR9JzXW0SGo'

# All queries to the Telegram Bot API need to be presented
# in this form: https://api.telegram.org/bot<token>/METHOD_NAME.
TEL_URL = 'https://api.telegram.org/bot{token}/sendMessage'
URL = 'https://www.tesmanian.com/blogs/tesmanian-blog'

# def login():
# after login attempt redirect to
# https://www.tesmanian.com/challenge - captcha confirmation page
#     headers = {
#         'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, likeGecko)
#         Chrome/104.0.0.0 Safari/537.36'
#     }
#     login_data = {
#         'form_type': 'customer_login',
#         'customer[email]': 'alexandr.yevlentyev@gmail.com',
#         'customer[password]': '123456789',
#         'return_url': '/account',
#         'recaptcha-v3-token': ''
#     }
#
#     with requests.Session() as s:
#         log_url = 'https://www.tesmanian.com/account'
#         r = s.get(log_url, headers=headers)
#         soup = BeautifulSoup(r.content, 'html.parser')
#         r = s.post(log_url, data=login_data, headers=headers)
#         print(r.url)


def check_post():
    query = requests.get(URL)
    soup = BeautifulSoup(query.text, 'html.parser')
    post_url = soup.find('div', class_='container main content').find('h2').find('a').get('href')

    with open('post.csv', 'r') as file:
        data = csv.DictReader(file)
        prev_post_url = next(data).get('post_url')

    if prev_post_url != post_url:
        post_title = soup.find('div', class_='container main content').find('h2').find('a').text
        absolute_post_url = 'https://www.tesmanian.com/' + post_url
        data = {'post_url': post_url}

        # overwrite link of the last post for next comparison
        with open('post.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

        return tel_send_message(post_title, absolute_post_url)


def tel_send_message(post_title, post_link):
    # Use sendMessage Telegram method with 2 required parameters: chat_id, text
    # to send a message for a new post
    params = {
        'chat_id': '522243417',
        'text': f'{post_title}\n {post_link}'
    }
    query_url = TEL_URL.format(token=TEL_TOKEN)
    query = requests.get(url=query_url, params=params)
    return query


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        check_post()
        sleep(15)




