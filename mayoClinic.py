import csv

from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def getsoup(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup


def getnextpage(soup):
    page = soup.find('nav', {'class': 'access-pagination'}).find('ol')
    if page.find('a', {'id': 'pagination-next'}):
        url = "https://www.mayoclinic.org" + page.find('a', {'id': 'pagination-next'})['href']
        return url
    else:
        return


def getdata(soup):
    trever = soup.find('ol', {'class': 'result-items'})
    # print(trever)
    templist = []

    for li in trever:
        if li.find('a') == -1:
            continue
        name = li.find('a').text.split(',')[0]
        sp_ol = li.find('ol', {'class': 'speciality'})
        specialities = []
        if sp_ol is not None:
            specialities = [li.text for li in sp_ol.find_all('li')]
        local_dict = {'Doctor': name, 'Specialities': ', '.join(specialities)}
        templist.append(local_dict)

    return templist


def append_csv(data):
    with open('MayoClinic.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['Doctor', 'Specialities'])
        writer.writerows(data)


def main():
    url = "https://www.mayoclinic.org/appointments/find-a-doctor/search-results?searchterm=&page=1#edd114075cc94f35b9bccc081668c123"
    while True:
        soup = getsoup(url)
        data = getdata(soup)
        append_csv(data)
        url = getnextpage(soup)

        if not url:
            break
        print(url)


if __name__ == '__main__':
    main()
