# Read in
import lxml.html
import httpx 
import pandas as pd
import re
import json

# Libby Functions

def compile_aldermen_for_wards(ul_element, ward_number, aldermen_dict):
    """
    Gather each the ward aldermen for wards whose aldermen are listed as bullet oints. 
    
    inputs:
        ul_element: element known to contain bullet points
        ward_number: str associated with number of ward
        aldermen_dict: dictionary to contain ward_numbers as the key, values 
        will be a list of dictionaries. Key is an alderman's name, value is any 
        link associated with them
    
    outputs: 
        aldermen_dict: dictionary to contain ward_numbers as the key, values 
        will be a list of dictionaries. Key is an alderman's name, value is any 
        link associated with them
    
    """
    ward_aldermen = []
    bullet_points = ul_element.cssselect("li")
    for bullet in bullet_points:
        links = bullet.cssselect('a')
        profile_link = None        
        if links is not None:
            for element in links:
                # Wikipedia will often link to a file or its bibliography. I 
                # only want a link if it has the person's biography there
                href = element.get('href')
                if re.search("File", str(href), re.IGNORECASE) or \
                    re.search("cite_note", str(href), re.IGNORECASE):
                    continue
                else:
                    profile_link = "https://en.wikipedia.org/" + href
                    break
        # Now I should create a dictionary with the indivudual as the key and 
        # the links as the value
        # I will then add this dictionary to a list. This list will then be the 
        # value of final dictionary where the key is the ward
        
# clean name courtesy of: 
# https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
        clean_name = re.sub(r'\([^)]*\)', '', bullet.text_content())
        person_tuple = (str.strip(clean_name), profile_link)
        ward_aldermen.append(person_tuple)
    
    aldermen_dict[ward_number] = ward_aldermen
    
    return aldermen_dict

def find_ward():

    aldermen_dict = {}
    url = "https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923"
    url_text = httpx.get(url)
    root = lxml.html.fromstring(url_text.text)

    body_content = root.cssselect('div.mw-body-content')[0]
    heading = body_content.cssselect('div.mw-heading.mw-heading3')

    for ward_number in heading:
        num = re.findall("\\d+", ward_number.text_content())
        ward = num[0]
        
        # Each part of the page is structured a bit differently. 
        # Sometimes, I a ul element is found immediately after the heading. Other 
        # times, they have figures or paragraphs after the heading and before the 
        # list of aldermen. For that reason, I grab the next five elements.
        
        sibling_1 = ward_number.getnext()
        sibling_2 = sibling_1.getnext()
        sibling_3 = sibling_2.getnext()
        sibling_4 = sibling_3.getnext()
        sibling_5 = sibling_4.getnext()
        
        for element in [sibling_1, sibling_2, sibling_3, sibling_4, sibling_5]:
            if re.search("table", str(element), re.IGNORECASE):
                # if there's a table associated with this ward, I don't care about
                # it, so I move onto the next ward
                break
            elif re.search("ul", str(element), re.IGNORECASE):
                aldermen_dict = \
                    compile_aldermen_for_wards(element, ward, aldermen_dict)
                break
            else:
                continue

    return aldermen_dict
        
def find_alder_link(aldermen_dict):
    aldermen_dates_dict = {}
    for ward, aldermen_and_links in aldermen_dict.items():
        all_info = []
        for tup in aldermen_and_links:
            alderperson = tup[0]
            link = tup[1]
            # we have a series of different labels for dates so we can evaluate 
            # what has happened
            if link is not None:
                dates = "link exists"
                resp = httpx.get(link)
                if resp.status_code == 200:
                    root = lxml.html.fromstring(resp.text)
                    # This is the box that has the in office dates, but sometimes 
                    # it doesn't exist
                    info_box = root.cssselect("table.infobox.vcard")
                    if len(info_box) == 1:
                        info_elements = info_box[0].cssselect('th.infobox-header')
                        for element in info_elements:
                            # we want to find the row header that is associated 
                            # with being a Chicago alderperson — and not the 
                            # council president                             
                            if re.search("ward", element.text_content(), \
                                re.IGNORECASE) or re.search("alder", \
                                element.text_content(), re.IGNORECASE) or \
                                re.search("Chicago City Council", \
                                element.text_content(), re.IGNORECASE) and \
                                re.search("^ President", element.text_content(), \
                                    re.IGNORECASE):
                                # We also want to see if they have the correct
                                # ward listed -- if there is one. 
                                if re.search("\\d+", element.text_content(), 
                                        re.IGNORECASE) is None or ward in \
                                            element.text_content():
                                # We want to find the row itself this is 
                                # associated  with rather than the actual header     
                                    row_parent = element.getparent()
                                # The header we want is in the next two rows
                                    header_option1 = row_parent.getnext()
                                    header_option2 = header_option1.getnext()
                                    if re.search("office", \
                                        header_option1.text_content(), \
                                            re.IGNORECASE):
                                        dates_raw = header_option1.text_content()
                                        dates_raw = re.sub("In office", "", \
                                            dates_raw)
                                        dates_raw = re.sub("Assumed office", \
                                            "", dates_raw)
    # clean name courtesy of: 
    # https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
                                        dates_raw = re.sub(r'\([^)]*\)', ' ', \
                                            dates_raw)
                                        dates_raw = re.sub(r'\xa0', ' ', \
                                            dates_raw)
                                        dates = str.strip(re.sub(r'\[[^)]*\]', \
                                            ' ', dates_raw))
                                    elif re.search("office", \
                                    header_option2.text_content(), re.IGNORECASE):
                                        dates_raw = header_option2.text_content()
                                        dates_raw = re.sub("In office", "", \
                                            dates_raw)
                                        dates_raw = re.sub("Assumed office", \
                                            "", dates_raw)
    # clean name courtesy of: 
    # https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
                                        dates_raw = re.sub(r'\([^)]*\)', \
                                            ' ', dates_raw)
                                        dates_raw = re.sub(r'\xa0', ' ', \
                                            dates_raw)
                                        dates = str.strip(re.sub(r'\[[^)]*\]', \
                                            '', dates_raw))
                                    else:
                                        dates = "unknown from link"
                                    break
                    else:
                        dates = "ERROR, BOX ELEMENT"
                    
                else:
                    dates = "ERROR, BAD LINK"       
            else:
                dates = "Unknown"
                
            person_tup = (alderperson, dates)
            all_info.append(person_tup)
            
        aldermen_dates_dict[ward] = all_info
            
    return aldermen_dates_dict

