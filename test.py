import requests
import json
from grade import grading

Count = 200
apikey = "c1d40892018e844a6b1e09dbeac4f808"
accept = "application/json"
book_num = 0
summation = 0
total = 0
tables = []
# AVENGERS PHASE 1: !---------------
def phase_one(id):
    URL = "https://api.elsevier.com/content/search/scopus"
    Query = f"AU-ID({str(id)})"
    PARAMS = {'apiKey': apikey, 'Accept': accept, 'query': Query, 'count': Count}

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    # print(data)
    num = len(data["search-results"]["entry"])

    for i in range(num):
        var1 = data["search-results"]["entry"][i]["dc:title"]
        tables.append(var1)
        phase_two(var1)
# ----!

# AVENGERS PHASE 2: !-----
def phase_two(var):
    global var2, book_num
    URL = "https://api.elsevier.com/content/search/scopus"
    Query = f"TITLE({var})"
    PARAMS = {'apiKey': apikey, 'Accept': accept, 'query': Query, 'count': Count}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    first_key = list(data.keys())[0]
    if first_key == 'service-error':
        return
    else:
        if first_key == 'search-results':
            try:
                var2 = data['search-results']['entry'][0]['prism:issn']
                phase_three(var2)
            except KeyError:
                try:
                    var2 = data['search-results']['entry'][0]['prism:eIssn']
                    phase_three(var2)
                except KeyError:
                    var2 = data['search-results']['entry'][0]['prism:isbn'][0]['$']
                    book_num += 1
                    print("books: ", book_num)


def phase_three(var):
    global summation, total, book_num
    URL = "https://api.elsevier.com/content/serial/title"
    idssn = var
    view = "CITESCORE"
    PARAMS = {'apiKey': apikey, 'Accept': accept, 'View': view, 'issn': idssn, }
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    num = len(data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreYearInfo'])
    print("break")
    for i in range(num):
        date = int(data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreYearInfo'][i]['@year'])
        if date<2018:
            break
        else:
            num2 = data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreYearInfo'][i] \
                ['citeScoreInformationList'][0]['citeScoreInfo'][0]['citeScoreSubjectRank'][0]['percentile']
            num2 = int(num2)
            compare2 = grading(num2)
            summation += compare2
            print(date,":",num2,":",compare2)
        continue

# phase_one("37661593100")
total = (book_num * 0.5) + summation
print("summation: ", summation)
print("Total: ", total)
print(tables)
