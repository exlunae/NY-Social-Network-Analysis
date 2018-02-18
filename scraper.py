from bs4 import BeautifulSoup
import requests 

#Loops through the specified page numbers for the analysis: pages for prior to December 1, 2014
for i in range(6, 10): #range should end at 31: change later
    url = "http://www.newyorksocialdiary.com/party-pictures?page=%d" %i 

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    #extracts all field-content classes and put them in a list
    field_content_list = soup.find_all("span", class_="field-content")

    links = []

    #Extract valid directory/links from field_content_list
    for i in field_content_list:
        current_field_content = i.find("a")
        if current_field_content == None:
            continue
        else:
            links.append(current_field_content)

    #Extract only what's after "href" into the same list
    for i in range(len(links)):
        links[i] = links[i]['href']

    #Append the url path to the domain for every element in list 
    for i in range(len(links)):
        links[i] = "http://www.newyorksocialdiary.com/" + links[i]
    print links
