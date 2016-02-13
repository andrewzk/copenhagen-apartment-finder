# copenhagen-apartment-finder
Scrape DBA and Boliga periodically for newly-listed apartments in Copenhagen, emailing you when one matches your search criteria.

## How to run
- Configure the variables at the top of the script (GMAIL_USER, etc)
- `python setup.py install`
- `python apartment_crawler.py`

If DBA/Boliga change their frontend, the parsing will need to be updated.
