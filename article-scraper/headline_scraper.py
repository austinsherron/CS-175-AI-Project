from bs4 import BeautifulSoup as bs
from collections import defaultdict
import csv
from datetime import date as d
import urllib.request as req, urllib.request
from subprocess import check_output
from io import StringIO
import datetime

def build_url(exchange, company):
	exchange = exchange.upper()
	company = company.upper()
	return 'https://www.google.com/finance/company_news?q=' + exchange + '%3A' + company + '&ei=0_A2VZuwF4PMrgHL5oC4Bg&start=0&num=100000'


def get_soup_from_url(url):
	page = req.urlopen(url)
	return bs(page)

def get_stock_price_for_date(company, date1, date2):
	try:
		url = ('http://ichart.yahoo.com/table.csv?'
				's={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d&ignore=.csv').format(
				company,
				str(date1.month - 1),
				str(date1.day),
				str(date1.year),
				str(date2.month - 1),
				str(date2.day),
				str(date2.year))
		s = str(req.urlopen(url).read()).replace('\\n', '\n')
		f = StringIO(s)
		r = csv.reader(f, delimiter=',', quotechar='"')
		correctRow1 = None
		correctRow2 = None
		for row in r:
			if row[0] == str(date1.year) + '-' + ('%02d' % date1.month) + '-' + ('%02d' % date1.day):
				correctRow1 = row
			if row[0] == str(date2.year) + '-' + ('%02d' % date2.month) + '-' + ('%02d' % date2.day):
				correctRow2 = row
		return [correctRow1, correctRow2]
	except Exception:
		return None


def make_date_absolute(date):
	dates = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
	if 'hour' in date or 'minute' in date or 'sec' in date:
		date = str(d.today().month) + '/' + str(d.today().day) + '/' + str(d.today().year)
	else:
		date = date.split(' ')
		date = str(dates[date[0]]) + '/' + str(date[1].strip(',')) + '/' + str(date[2])
	return date


def build_row(headline, date, company):
	headline = headline.replace(u'\xa0', u' ')
	date = date.replace(u'\xa0', u' ')
	date = make_date_absolute(date)
	#return [headline, date, article_content]
	'''if type(article_content) != str:
		article_content = article_content.decode('utf-8')
	article_content = article_content.replace('\xa0', ' ')
	article_content = article_content.replace('\xc2', ' ')
	article_content = article_content.replace('\n', ' ')'''
	parts = date.split('/')
	month = int(parts[0])
	day = int(parts[1])
	year = int(parts[2])
	date = datetime.date(year, month, day)
	skip_length = 3
	saturday = 5
	if date.weekday() + skip_length >= saturday:
		skip_length += 2
	res = get_stock_price_for_date(company, date, date + datetime.timedelta(skip_length))
	score = ''
	if not res:
		score = 'none'
	else:
		first = res[0]
		last = res[1]
		if not first or not last:
			score = 'none'
		else: 
			score = (float(last[4]) - float(first[1])) / float(last[1])
	return [headline, str(score)]


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
	article_content = ''
	try:
		article_content = check_output(['java', 'Main', headline_url])
	except:
		article_content = 'NO CONTENT'
	return article_content 


def do_scraping(url, scrape_articles, company):
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
			'''if scrape_articles:
				headline_url = name.find('a')['href']
				#article_content = alt_scrape_articles(headline_url)
				#article_content = scrape_article(headline_url)
			else:
				article_content = 'NO CONTENT'
			'''
			date = div.find('span', {'class': 'date'}).contents[0]
			headlines.append(build_row(headline, date, company))
	return headlines


def build_output_csv(file_name, headlines, company):
	if not headlines:
		raise ValueError('Error: no available headlines; company (' + company + ') is likely invalid')
	with open(file_name, 'a') as file:
		writer = csv.writer(file)
		#print(headlines)
		#writer.writerow(['COMPANY:', company])
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
			headlines = do_scraping(url, scrape_articles, company)
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
	print('		exchange:,[name of exchange]')
	print('		[company ticker symbol')
	print('		...')
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

