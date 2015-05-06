from bs4 import BeautifulSoup as bs
from collections import defaultdict
import csv
from datetime import date as d
import urllib.request as req, urllib.request


def build_url(exchange, company):
	exchange = exchange.upper()
	company = company.upper()
	return 'https://www.google.com/finance/company_news?q=' + exchange + '%3A' + company + '&ei=0_A2VZuwF4PMrgHL5oC4Bg&start=0&num=100000'


def get_soup_from_url(url):
		page = req.urlopen(url)
		return bs(page)


def make_date_absolute(date):
	dates = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
	if 'hour' in date or 'minute' in date or 'sec' in date:
		date = str(d.today().month) + '/' + str(d.today().day) + '/' + str(d.today().year)
	else:
		date = date.split(' ')
		date = str(dates[date[0]]) + '/' + str(date[1].strip(',')) + '/' + str(date[2])
	return date


def build_row(headline, date, article_content):
	headline = headline.replace(u'\xa0', u' ')
	date = date.replace(u'\xa0', u' ')
	date = make_date_absolute(date)
	#return [headline, date, article_content]
	return [headline]


def scrape_article(headline_url):
	article_content = []
	try:
		article_soup = get_soup_from_url(headline_url)
		article_ps = article_soup.find_all('p')
		if article_ps:
			article_content = [p.get_text().strip() for p in article_ps]
		else:
			article_content = ['NO CONTENT']
	except:
		article_content = ['NO CONTENT']

	return ' '.join(article_content).replace('\n', ' ')


def alt_scrape_articles(headline_url):
	article_content = []
	url = 'http://boilerpipe-web.appspot.com/extract?url=' + headline_url + '&extractor=ArticleExtractor&output=text&extractImages='
	print(url)
	print(headline_url)
	try:
		article_soup = get_soup_from_url(headline_url)
		article_content = article_soup.get_text()
		print(article_content)
	except:
		article_content = ['NO CONTENT']


def do_scraping(url, scrape_articles):
	headlines = []
	soup = get_soup_from_url(url) 
	news_divs = soup.find_all('div', {'class': 'news'})
	count = len(news_divs)
	counter = 1
	for div in news_divs:
		name = div.find('span', {'class': 'name'})
		print('Headline/Article', counter, 'of', count)
		counter += 1
		if name:
			headline = name.find('a').contents[0]
			if scrape_articles:
				headline_url = name.find('a')['href']
				article_content = alt_scrape_articles(headline_url)
			else:
				article_content = 'NO CONTENT'
			date = div.find('span', {'class': 'date'}).contents[0]
			headlines.append(build_row(headline, date, article_content))
	return headlines


def build_output_csv(file_name, headlines, company):
	if not headlines:
		raise ValueError('Error: no available headlines; company (' + company + ') is likely invalid')
	with open(file_name, 'a') as file:
		writer = csv.writer(file)
		writer.writerow(['COMPANY:', company])
		writer.writerows(headlines)


def get_inputs(file_name):
	stocks = defaultdict(list)
	exchange = ''
	with open(file_name) as file:
		reader = csv.reader(file)
		for line in reader:
			if line[0] == 'exchange':
				exchange = line[1]
			else:
				stocks[exchange].append(line[0])
	return dict(stocks)


def run_scraper(inputs, output_file_name, scrape_articles):
	for exchange,companies in inputs.items():
		num = len(companies)
		counter = 1
		for company in companies:
			print('scraping for', company, 'headlines...', counter, 'of', num)
			url = build_url(exchange, company)
			headlines = do_scraping(url, scrape_articles)
			try:
				build_output_csv(output_file_name, headlines, company)
				print('...finished scraping', company)
			except ValueError:
				print()
				print('Error: Company (', company, ') doesn\'t seem to be valid')
				print()
			counter += 1


if __name__ == '__main__':

	print()
	print('Headline/Article scraper for Google Finance...')
	print()
	print()
	print('Input file must be a csv in the form of:')
	print('    exchange:,[name of exchange]')
	print('    [company ticker symbol')
	print('    ...')
	print()

	input_file = str(input('Enter name of input file (defaults to company_symbols.csv, will fail if doesn\'t exist):'))
	print()

	output_file = str(input('Enter name of output file (defaults to data.csv, will be created if it doesn\'t exist):'))
	print()
	scrape_articles = str(input('Scrape articles as well as headlines (default is false)?'))
	print()

	input_file = input_file if input_file else 'company_symbols.csv'
	output_file = output_file if output_file else 'data.csv'
	scrape_articles = bool(scrape_articles)

	inputs = get_inputs(input_file)
	run_scraper(inputs, output_file, scrape_articles)

	print('Finished')
	print()

