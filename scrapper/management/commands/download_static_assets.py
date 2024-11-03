import os
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Download all CSS and JS files required to render a page and save them in the static directory.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL of the page to download assets from.')
        parser.add_argument('--directory', type=str, default='static/trendyol', help='Directory to save downloaded files.')

    def handle(self, *args, **options):
        url = options['url']
        base_directory = options['directory']

        # Create CSS and JS directories
        css_dir = Path(base_directory) / 'css'
        js_dir = Path(base_directory) / 'js'
        css_dir.mkdir(parents=True, exist_ok=True)
        js_dir.mkdir(parents=True, exist_ok=True)

        # Fetch the page HTML
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Download CSS files
        css_files = soup.find_all('link', rel='stylesheet')
        for css in css_files:
            css_url = urljoin(url, css.get('href'))
            self.download_file(css_url, css_dir)

        # Download JS files
        js_files = soup.find_all('script', src=True)
        for js in js_files:
            js_url = urljoin(url, js.get('src'))
            self.download_file(js_url, js_dir)

        self.stdout.write(self.style.SUCCESS('All assets downloaded successfully.'))

    def download_file(self, url, folder):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure the request was successful
            filename = os.path.basename(urlparse(url).path)
            file_path = folder / filename

            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.stdout.write(self.style.SUCCESS(f'Downloaded: {file_path}'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to download {url}: {e}'))
