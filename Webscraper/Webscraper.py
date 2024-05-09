from urllib.request import urlopen
import re
import os
import html as ht
from random import randint
from time import sleep


sitemap = "http://www.lincoln.ac.uk/sitemap-en.xml" #url of the sitemap

sitemap_page = urlopen(sitemap) #read the sitemap
sitemap_html_bytes = sitemap_page.read()
sitemap_html = sitemap_html_bytes.decode("utf-8") #decode it in utf-8 characters
sitemap_addresses = re.findall("<loc>.*?</loc>", sitemap_html) #find every loc tag
sitemap_addresses_no_tags = re.sub("<.*?>", "", str(sitemap_addresses))
sitelist = sitemap_addresses_no_tags.replace("[", "") #format all the data to remove tags and have a pure comma separated string
sitelist = sitelist.replace("'", "")
sitelist = sitelist.replace(" ", "")
sitelist = sitelist.replace("]", "")
webpage_array = re.split('/,', sitelist) #split into a list but because of the school of design it has to be /,

for x in webpage_array: #iterate through every page
    print(x) #make it seem like it's doing something so give each page as it searches
    if 'https://www.lincoln.ac.uk/course' in x:
        page = urlopen(x)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        title_index = html.find("<title>")
        start_index = title_index + len("<title>")
        end_index = html.find("</title>")

        title = html[start_index:end_index] #find the title tags and the text to store in title

        main_index = html.find('<main id="skip-to-content">')
        main_start_index = main_index + len('<main id="skip-to-content">')
        main_end_index = html.find("</main>")

        main = html[main_start_index:main_end_index] #take the main as one string

        all_content = re.findall("<h.*?>.*?</h.*?>|<p.*?>.*?</p.*?>", main) #just get headers and paragraphs
        no_tags = re.sub("<.*?>", "", str(all_content))
        just_text = re.sub("',.*?'", "\n", str(no_tags))
        just_text = ht.unescape(just_text) #remove special characters
        just_text = just_text.replace('\\', '')
        just_text = re.sub(r"(\s+(‌\s+)+)", "", str(just_text))
        just_text = just_text.replace("['", title)
        just_text = just_text.replace("']", "")
        just_text = (just_text.encode('ascii', 'ignore')).decode("utf-8") #ignore encoded characters but place it back into encode so it can be read properly


        Sections_Of_Url = x.count("/") #depth of the page

        if Sections_Of_Url < 4:
            filename = "Overview.txt"
        else:
            if Sections_Of_Url < 5:
                full_last_section = re.search('.uk/course/(.*)', x)
                filename = full_last_section.group(1) + ".txt"
                print(filename)
            else:
                full_last_section = re.search('.uk/course/(.*)/', x)
                filename = full_last_section.group(1) + ".txt"
                print(filename)

        with open(filename, "a") as file: #create or append file and then add the text with 3 lines afterwards
            file.write(just_text + "\n\n\n")

        file.close #close the file

