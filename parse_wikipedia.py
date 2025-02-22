import xml.etree.ElementTree as ET
import re

url_pattern = re.compile(r"\[\[.*?]]") # identify links
link_to_file_pattern = re.compile(r"File.+\..+") # identify when a link is to a file, these should be ignored
coordinate_pattern = re.compile(r"\[-?[0-9]+.[0-9]+,-?[0-9]+.[0-9]+]") # identify when a link is just a coordinate

references_header = "==References=="

tag_prefix = "{http://www.mediawiki.org/xml/export-0.11/}"
page_tag = tag_prefix + "page"
title_tag = tag_prefix + "title"
revision_tag = tag_prefix + "revision"
text_tag = tag_prefix + "text"


article_count = 0
link_count = 0

def clean_links(links):
    cleaned = []
    for link in links:
        link = link[2:-2]  # Remove brackets
        if "|" in link:
            link = link.split("|")[0]  # Use article title instead of link text
        if (
            not link_to_file_pattern.match(link)
            and not coordinate_pattern.match(link)
            and len(link) != 0
        ):
            cleaned.append(link)

    #print(f"Links: {cleaned}")
    cleaned = list(set(cleaned)) # Remove duplicates
    #print(f"Cleaned links: {cleaned}")
    return cleaned

def parse_xml(file_path):
    global article_count, link_count
    #print(f"Processing file: {file_path}")
    for event, elem in ET.iterparse(file_path, events=("start", "end")):
        #print(event, elem.tag)
        if event == "end" and elem.tag == page_tag:

            title = elem.find(title_tag).text
            revision = elem.find(revision_tag)
            text = revision.find(text_tag).text

            if text:
                text = text.split(references_header)[0] # Ignore references section and beyond

                links = url_pattern.findall(text)
                # print(f"Title: {title}")
                links = clean_links(links)

                # some links are just an alias for the actual page, like AccessibleComputing -> Computer accessibility
                if len(links) != 1:
                    article_count += 1
                    link_count += len(links)
                    with open("wikipedia_data/parsed/articles.txt", "a") as f:
                        f.write(f"{title}->")
                        for link in links:

                            f.write(f"|||{link}")
                        f.write("\n")



            # Clear processed elements to avoid crashing computer when processing large files
            elem.clear()

parse_xml("wikipedia_data/raw/enwiki.xml")
print(f"Article count: {article_count}, Link count: {link_count}")

