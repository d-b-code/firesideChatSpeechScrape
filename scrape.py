#make imports
import requests
from bs4 import BeautifulSoup
import csv

#setting up initial url parse and scrape
url = 'https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/fireside-chats-f-roosevelt'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#find the table with links to the speeches
table =soup.find('table', class_="views-table cols-3 table table-striped")

#extract containers with links
links = table.find_all('a')
targets = []

#Iterate over list of containers to extract specific links
for link in links:
    site = link.get('href')
    targets.append(site)

#using the links from the targets list, go to each one and scrape that site for the date, text of the speech, and link
final_list =[]
for target in targets:
    webpage = requests.get(target)
    content = BeautifulSoup(webpage.content, 'html.parser')
    date = content.find('span', class_='date-display-single')
    texts = content.find('div', class_='field-docs-content')
    date = date.text
    texts = texts.text
    entry = [date, texts, target]
    final_list.append(entry)

#make a csv of the resulting data
fields = ['date', 'speech', 'link']
filename = 'fireside speeches v2.csv'
with open(filename, 'w', newline ='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(final_list)