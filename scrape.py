from bs4 import BeautifulSoup
import requests

url = "http://www.marathonrunnersdiary.com/races/europe-marathons-list.php"

def scrape():
    results = []
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    
    for i in doc.find_all("div", {"itemtype": "http://schema.org/Event"}):
        temp = []
        temp.append(i.contents[0].contents[1])
        temp.append(i.contents[1].get_text())
        temp.append(i.contents[2].find("div", {"class","leftregion"}).get_text())
        results.append(temp)

    for j in results:
        print(j)
        print()
scrape()