#!/usr/bin/python

# -*- coding: utf-8 -*-

import time
import smtplib
import requests
from BeautifulSoup import BeautifulSoup

REFRESH_INTERVAL_SECONDS = 30
GMAIL_USER = 'EDIT_ME' # The emails originate from here
# Note - when using gmail from an external app, you need to generate an app-specific password
# See https://support.google.com/mail/answer/1173270?hl=en
GMAIL_PASSWORD = 'EDIT ME'

TARGET_EMAIL = 'EDIT ME' # Where the new apartments should be sent

DBA_URL = 'EDIT ME' # For example, http://www.dba.dk/boliger/andelsbolig/andelslejligheder/vaerelser-3/?soeg=andelsbolig&vaerelser=4&vaerelser=5&vaerelser=6&boligarealkvm=(70-)&sort=listingdate-desc&pris=(1500000-2499999)&pris=(1000000-1499999)&soegfra=1060&radius=5
BOLIGA_URL = 'EDIT ME' # For example, http://www.boliga.dk/soeg/resultater/a194d60c-e272-4c09-a7fd-899763577c58?sort=liggetid-a')


class User(object):
    def __init__(self, email, dba_url, boliga_url=None):
        self.email = email
        self.dba_url = dba_url
        self.boliga_url = boliga_url
        self.seen_urls = set()

def send_email(headline, url, recipient):
    smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465) # Change if not using gmail
    smtp_obj.login(GMAIL_USER, GMAIL_PASSWORD)
    FROM = GMAIL_USER
    TO = [recipient] #must be a list
    SUBJECT = headline
    TEXT = url
    
    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    smtp_obj.sendmail(FROM, TO, message)
    smtp_obj.close()

def crawl_dba(user):
    session = requests.Session()
    session.encoding = 'utf-8'
    r = session.get(user.dba_url)
    soup = BeautifulSoup(r.text, convertEntities=BeautifulSoup.HTML_ENTITIES)
    listings = soup.findAll('tr', 'dbaListing')
    for listing in listings:
        link = listing.find('a', 'listingLink')['href'].encode('utf-8')
        headline = listing.find('span', 'headline')
        if headline is not None:
            headline = headline.text.encode('utf-8')
        else:
            headline = link
        if link not in user.seen_urls:
            send_email(headline, link, user.email)
            user.seen_urls.add(link)

def crawl_boliga(user):
    session = requests.Session()
    session.encoding = 'utf-8'
    r = session.get(user.boliga_url)
    soup = BeautifulSoup(r.text.encode('utf-8'), convertEntities=BeautifulSoup.HTML_ENTITIES)
    listings = soup.findAll('tr', 'pRow')
    for listing in listings:
        link_element = listing.findAll('a')[1]
        headline = link_element['title'].encode('utf-8')
        url = ('http://www.boliga.dk' + link_element['href']).encode('utf-8')
        if url not in user.seen_urls:
            send_email(headline, url, user.email)
            user.seen_urls.add(url)

def main():
    user = User(email=TARGET_EMAIL,
                dba_url=DBA_URL,
                boliga_url=BOLIGA_URL)

    while True:
        try:
            crawl_dba(user)
            crawl_boliga(user)
            time.sleep(REFRESH_INTERVAL_SECONDS)
        except Exception as e:
            print e

main()
