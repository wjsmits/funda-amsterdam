import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', ['id', 'date', 'street', 'city', 'postcode', 'livingspace', 'otherspace', 'price'])

city = 'den bosch'
minPrice=str(200000)
maxPrice=str(400000)
minOpp=str(75)

fundaUrl = 'http://www.funda.nl'
# startUrl = fundaUrl + '/koop/' + city + '/' + minPrice + '-' + maxPrice + '/' + minOpp + '+woonopp' + '/' + 'appartement' + '/' + 'bestaande-bouw' + '/'
startUrl = fundaUrl + '/koop/' + city +  '/' + 'appartement' + '/' + 'bestaande-bouw' + '/'
baseUrl = startUrl + 'p'

html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)

# get number of pages
pages = soup.findAll(attrs={'id' : 'ctl00_CPHResultaat_ZoekResultaatLijst_ctl00_ctl30_ha'})
numberOfpages = int(pages[len(pages) - 2].string)

items = []
today = datetime.date.today()

for pageNo in range(1, numberOfpages + 1):
 
    nextUrl = baseUrl + str(pageNo)
    print 'page: ' + nextUrl
    html = scraperwiki.scrape(nextUrl)
    soup = BeautifulSoup.BeautifulSoup(html)
    
    for tr in soup.findAll('tr', 'nvm'):
        realItem = {'date' : today}
        
        for item in tr.findAll('a', 'item'):
            realItem['street'] = item.string
            realItem['id'] = fundaUrl + item['href']
        
        for spec in tr.findAll('p', 'specs'):
            realItem['postcode'] = spec('span', limit=2)[0].string.strip()
            realItem['city'] = spec('span', limit=2)[1].string.strip()
            if spec.find(title='Woonoppervlakte'):
                realItem['livingspace'] = spec.find(title='Woonoppervlakte').string.replace('&nbsp;m&sup2;', '').strip()
            else:
                realItem['livingspace'] = ''
            if spec.find(title='Perceeloppervlakte'):
                realItem['otherspace'] = spec.find(title='Perceeloppervlakte').string.replace('&nbsp;m&sup2;', '').strip()
            else:
                realItem['otherspace'] = ''
        for price in tr.findAll('span', 'price'):
            realItem['price'] = price.string.replace('&euro;&nbsp;', '').strip().replace('.', '')
        
        items.append(realItem)
        scraperwiki.datastore.save(unique_keys=['id'], data=realItem)
        print 'items saved: ' + str(len(items))
