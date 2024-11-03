from django import forms

class ScraperSettingsForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.TextInput(attrs={'placeholder': 'Enter the URL to scrape'}))
    max_items = forms.IntegerField(label='Max Items', initial=100)
    price_range = forms.CharField(label='Price Range (min-max)', required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g., 10-50'}))
    category = forms.CharField(label='Categories (comma-separated)', required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g., TS,SB'}))
    preview_option = forms.ChoiceField(label='Preview Option', choices=[('tabular', 'Tabular'), ('html', 'HTML')], initial='tabular')
    headless = forms.BooleanField(label='Headless Mode', required=False)
    driver_path = forms.CharField(label='ChromeDriver Path', widget=forms.FileInput())


class ScrapeForm(forms.Form):
    url = forms.URLField(label='Enter URL to scrape', required=True)

class URLForm(forms.Form):
    url = forms.URLField(label='Enter URL to Scrape', required=True)
