from bs4 import BeautifulSoup
import requests
import re

#Return a list of urls with photo captions to scrape
def gather_valid_urls():
# Loops through the specified page numbers for the analysis: pages for prior to December 1, 2014

    # List for all future links
    links = []
    for i in range(6, 7):  # range should end at 31: change later
        url = "http://www.newyorksocialdiary.com/party-pictures?page=%d" % i

        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        # extracts all field-content classes and put them in a list
        field_content_list = soup.find_all("span", class_="field-content")

        # Extract valid directory/links from field_content_list
        for i in field_content_list:
            current_field_content = i.find("a")
            if current_field_content == None:
                continue
            else:
                links.append(current_field_content)

        # Extract only what's after "href" into the same list
        for i in range(len(links)):
            links[i] = links[i]['href']

        # Append the url path to the domain for every element in list
        for i in range(len(links)):
            links[i] = "http://www.newyorksocialdiary.com/" + links[i]

    print "Links to go through: "  #DELETE
    print links                 #DELETE
    return links

def gather_valid_names(url):
    html = requests.get(url)
    print "----------------------"
    soup = BeautifulSoup(html.text, 'html.parser')

    #Parse all divs with class photocaption into a list
    photo_caption_list = soup.find_all("div", class_="photocaption")

    #Mutate all of photo_caption_list to only contain its string contents
    for i in range(len(photo_caption_list)):
        photo_caption_list[i] = photo_caption_list[i].contents

    #Clean strings to extract names: removes titles, commas, ands, etc.
    for i in range(len(photo_caption_list)-1):
        #Remove all strings within parentheses
        print photo_caption_list[i][0]
        print "------"
        photo_caption_list[i][0] = re.sub(r'\([^)]*\)', '', photo_caption_list[i][0])
        #Remove all instances of common prefixes
        photo_caption_list[i][0] = re.sub(r'Mr. | Mrs. | Dr. | Ms. | M.D. | CEO | Chair | Queen | co-chair | friend | friends', '', photo_caption_list[i][0], re.IGNORECASE)
        #Split string by: [, and]
        photo_caption_list[i] = re.split(r', | and', photo_caption_list[i][0])

    valid_names_in_url = set()

    for i in photo_caption_list:
        name_set = set(i)
        print name_set
        valid_names_in_url = valid_names_in_url.union(name_set)

    print "valid names:"
    print valid_names_in_url
    return valid_names_in_url

def main():
    valid_urls = gather_valid_urls()
    list_of_names = set()
    for i in range(len(valid_urls)):
        list_of_names = list_of_names.union(gather_valid_names(valid_urls[i]))



if __name__ == "__main__":
    main()
