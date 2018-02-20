from bs4 import BeautifulSoup
import requests
import re

#Return a list of urls with photo captions to scrape
def gather_valid_urls():
# Loops through the specified page numbers for the analysis: pages for prior to December 1, 2014

    # List for all links
    links = []
    for page in range(6, 31):  # range should end at 31: change later
        page_links = []
        url = "http://www.newyorksocialdiary.com/party-pictures?page=%d" % page

        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        #Extracts all field-content classes and put them in a list
        field_content_list = soup.find_all("span", class_="field-content")

        # Extract valid directory/links from field_content_list
        for i in field_content_list:
            current_field_content = i.find("a")
            if current_field_content == None:
                continue
            else:
                page_links.append(current_field_content)

        # Extract only what's after "href" into the same list
        for i in range(len(page_links)):
            page_links[i] = page_links[i]['href']

        # Append the url path to the domain for every element in list
        for i in range(len(page_links)):
            page_links[i] = "http://www.newyorksocialdiary.com/" + page_links[i]
        links.extend(page_links)

    return links

#Cleaning Parse Algorithm
def gather_valid_names(url):

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    #Parse all divs with class photocaption into a list
    photo_caption_list = soup.find_all("div", class_="photocaption")

    #Mutate all of photo_caption_list to only contain its string contents
    for i in range(len(photo_caption_list)):
        photo_caption_list[i] = photo_caption_list[i].contents

    #Clean strings to extract names: removes titles, commas, ands, etc.
    for i in range(len(photo_caption_list) ):
        try:

            ## PARSING PREPOSITIONS

            # Remove all strings within parentheses
            photo_caption_list[i][0] = re.sub(r'\([^)]*\)', '', photo_caption_list[i][0])
            # Remove all strings within <>
            photo_caption_list[i][0] = re.sub(r'\<[^)]*\>', '', photo_caption_list[i][0])
            #Remove all substrings following "at"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' at ')[0]
            # Remove all substrings following "in"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' in ')[0]
            # Remove all substrings following "for"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' for ')[0]
            # Remove all substrings following "on"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' on ')[0]
            # Remove all substrings following "to"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' to ')[0]
            # Remove all substrings following "of"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' of ')[0]
            # Remove all substrings following "where"
            photo_caption_list[i][0] = photo_caption_list[i][0].split(' where ')[0]
            #Remove all elements in photo_caption_list without a comma or "and": indicates singular person or object/event
            if ',' not in photo_caption_list[i][0]:
                if 'and' not in photo_caption_list[i][0]:
                    photo_caption_list[i].remove(photo_caption_list[i][0])
                    continue
        except:
            break

        pattern = r'Mr. | Mrs. | Dr. | Ms. | M.D. | Mayor | CEO | Chair | Queen | Mayor | Jr. | Co-Chairs | Co-Chair | Composer | composer | Officer | Board |'
        #Remove all instances of common prefixes
        photo_caption_list[i][0] = re.sub(pattern, '', photo_caption_list[i][0], re.IGNORECASE)
        #Split string by: [, and]
        photo_caption_list[i] = re.split(r', | and | with', photo_caption_list[i][0])

        #Remove instances of "and" in strings
        for j in range(len(photo_caption_list[i])):
            if 'and' in photo_caption_list[i][j]:
                photo_caption_list[i][j] = photo_caption_list[i][j].replace('and ', '')

    valid_names_in_url = set()

    for i in photo_caption_list:
        name_set = set(i)
        valid_names_in_url = valid_names_in_url.union(name_set)

    return valid_names_in_url

def filter_whitespace(dirty_set):
    clean_set = set()

    for i in dirty_set:
        print "i:"
        print i
        try:
            clean_set.add(i.strip())
        except:
            continue
    return clean_set

def main():
    valid_urls = gather_valid_urls()
    list_of_names = set()

    for i in range(len(valid_urls)):
        list_of_names = list_of_names.union(gather_valid_names(valid_urls[i]))

    print "amount of names before cleaning: " + str(len(list_of_names))
    print list_of_names
    results = open('results.txt', 'w')
    results.write("Total Names: " + str(len(list_of_names)))

if __name__ == "__main__":
    main()