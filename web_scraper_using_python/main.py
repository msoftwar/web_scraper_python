from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '')

        try:
            scraped_data = scrape_website(url)
            return render_template('index.html', url=url, scraped_data=scraped_data)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')

def scrape_website(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad requests

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data from the HTML
    images = [img['src'] if 'src' in img.attrs else 'No src attribute' for img in soup.find_all('img')]
    links = [a['href'] for a in soup.find_all('a', href=True)]
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    # Add more data extraction logic as needed

    # Combine all data into a dictionary
    scraped_data = {
        'Images': images,
        'Links': links,
        'Paragraphs': paragraphs,
        'Headings': headings,
        # Add more keys for additional data types
    }

    return scraped_data


if __name__ == '__main__':
    app.run(debug=True)
