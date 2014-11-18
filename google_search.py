from GoogleScraper import scrape_with_config, GoogleSearchError

def scrape(query):
    config = {
        'SCRAPING': {
            'use_own_ip': 'True',
            'keyword': query
        },
        'SELENIUM': {
            'sel_browser': 'chrome',
            'manual_captcha_solving': 'True'
        },
        'GLOBAL': {
            'do_caching': 'True'
        }
    }

    try:
        # scrape() and scrape_with_config() will return a handle to a sqlite3 database with the results
        db = scrape_with_config(config)

        return (db.execute('SELECT * FROM link').fetchall())

    except GoogleSearchError as e:
        print(e)

if __name__ == "__main__":
    scape("Hello World")
