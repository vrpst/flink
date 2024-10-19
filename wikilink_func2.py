import requests
import time
session = requests.Session()
base_url = "https://en.wikipedia.org/w/api.php"
headers = {'User-Agent': open("ua.txt", 'r').readline()}  # hide contact info in file for privacy

def getPageText(title):
    url_params = {
        "action": "parse",
        "page": f"{title}",
        "prop": "wikitext",
        "format": "json",
        "formatversion": "2"
    }

    response = session.get(url=base_url, headers=headers, params=url_params)
    #print(response)
    if response.status_code == 200:
        response_data = response.json()
        return response_data['parse']['wikitext']

def findLink(text):  # FINDS THE RAW FIRST LINK IN THE PAGE AND THE STARTING SENTENCE
    first_link_found = False
    sentence_ended = False
    char_counter = 0
    open_curly_counter = 0
    close_curly_counter = 0
    open_square_counter = 0
    close_square_counter = 0
    open_bracket = 0
    close_bracket = 0
    first_sentence = ""
    sentence_start = 0
    sentence_start_needed = True
    valid_nextchars = [10, 91, 123]  # line break, [, {
    redirect_bool = not checkRedirect(text)
    while not first_link_found or not sentence_ended:
        #print(open_curly_counter, close_curly_counter, open_bracket, close_bracket, open_square_counter, close_square_counter, sentence_start, sentence_ended, char_counter)
        if not first_link_found:
            if text[char_counter] == "{":
                open_curly_counter += 1 

            if text[char_counter] == "}":
                close_curly_counter += 1

            if text[char_counter] == "(":
                open_bracket += 1
            
            if text[char_counter] == ")":
                close_bracket += 1

            if text[char_counter] == "[":
                if open_square_counter == close_square_counter and open_curly_counter == close_curly_counter:
                    link_start = char_counter
                open_square_counter += 1

            if text[char_counter] == "]":
                close_square_counter += 1
                if open_square_counter == close_square_counter and open_curly_counter == close_curly_counter and open_bracket == close_bracket:
                    link_end = char_counter+1
                    link_test = text[link_start:link_end]
                    if ":" not in link_test:  # no interlinks
                        first_link_found = checkNotFile(link_test)
            
        # THE FIRST CHARACTER NOT IN A TEMPLATE OR A LINK IS THE START OF PROSE
        if redirect_bool:
            if sentence_start_needed:  # start of the sentence (before the link is found)
                if open_curly_counter == close_curly_counter and open_square_counter == close_square_counter and open_bracket == close_bracket:
                    if 65 <= ord(text[char_counter]) <= 90 or ord(text[char_counter]) == 39:  # capital letter or bold
                        sentence_start = char_counter
                        sentence_start_needed = False
            
            if first_link_found and not sentence_ended:  # when the link is found but not the full stop
                if open_square_counter == close_square_counter and open_curly_counter == close_curly_counter and open_bracket == close_bracket:  #  in case a template starts between the link and period
                    if text[char_counter:char_counter+2] == ". " and 65 <= ord(text[char_counter+2]) <= 90 or text[char_counter:char_counter+3] == ".  ":  # if it's a period followed by a space and a cap letter
                        first_sentence = text[sentence_start:char_counter+1]
                        sentence_ended = True
                    elif text[char_counter:char_counter+5] == ".<ref" or (text[char_counter] == "." and ord(text[char_counter+1]) in valid_nextchars): # refs
                        first_sentence = text[sentence_start:char_counter+1]
                        sentence_ended = True
        else:  #  if the page is a redirect just skip the sentence
            sentence_ended = True
        
        # bypass html comments
        if text[char_counter:char_counter+4] == "<!--":
            while text[char_counter-3:char_counter] != "-->":       
                char_counter += 1
        else:
            char_counter += 1
    
    link = splitLink(link_test[2:-2])
    return [link, first_sentence]

def checkNotFile(link):
    #print(link)
    if "Image:" in link or "File:" in link:
        return False
    else:
        return True

def splitLink(link_to_split):  # SPLIT LINK INTO DISPLAYED TEXT AND REAL LINK
    if "|" in link_to_split:
        pipe_index = link_to_split.index("|")
        link_display = link_to_split[pipe_index+1:]
        link_real = link_to_split[:pipe_index]
    else:
        link_display = link_to_split
        link_real = link_to_split

    if "#" in link_real:  # get rid of sections
        link_real = link_real[0:link_real.index("#")]

    return [link_display, link_real]

def checkRedirect(page):
    if "#REDIRECT" in page or "#redirect" in page:
        return True
    else:
        return False

def cleanFirstSentence(text):
    # get rid of bold
    char_counter = 0
    while "'''" in text:
        bold = text.index("'''")
        if bold > 0:
            text = text[:bold] + text[bold+3:]
        else:
            text = text[3:]
    # get rid of refs
    while "<ref" in text:  # to account for <ref name=.....>
        ref_open = text.index("<ref")
        ref_close = text.index("</ref>")
        text = text[:ref_open] + text[ref_close+6:]

    # NESTED BRACKETS
    open_bracket_counter = 0
    closed_bracket_counter = 0
    char_counter = 0
    bracket_open = 0
    while "(" in text:
        if text[char_counter] == "(":
            open_bracket_counter += 1
            if open_bracket_counter == 1:
                bracket_open = char_counter
        elif text[char_counter] == ")":
            closed_bracket_counter += 1
        if open_bracket_counter == closed_bracket_counter and open_bracket_counter != 0:
            text = text[:bracket_open] + text[char_counter+1:]
            open_bracket_counter = 0
            closed_bracket_counter = 0
            char_counter = 0  # reset since indices have shifted
        char_counter += 1
    
    # NESTED TEMPLATES
    open_template_counter = 0
    closed_template_counter = 0
    char_counter = 0
    template_open = 0
    while r"{" in text:
        if text[char_counter] == r"{":
            open_template_counter += 1
            if open_template_counter == 2:
                template_open = char_counter
        elif text[char_counter] == r"}":
            closed_template_counter += 1
        if open_template_counter == closed_template_counter and open_template_counter != 0:
            text = text[:template_open-1] + text[char_counter+1:]
            open_template_counter = 0
            closed_template_counter = 0
            char_counter = 0  # reset since indices have shifted
        char_counter += 1

    while "[[" in text:
        char_counter = text.index("[[")
        while text[char_counter:char_counter+2] != "]]":
            char_counter += 1
        link_to_clean = text[text.index("[[")+2:char_counter]
        if "|" in link_to_clean:
            cleaned_link = splitLink(link_to_clean)[0]
        else:
            cleaned_link = link_to_clean
        text = text[:text.index("[[")] + cleaned_link + text[char_counter+2:]

    while "<!--" in text:
        comment_open = text.index("<!--")
        comment_closed = text.index("-->")
        text = text[:comment_open] + text[comment_closed+3:]

    while "  " in text:
        dubsp = text.index("  ")
        text = text[:dubsp] + text[dubsp+1:]

    while " , " in text:  # get rid of space before comma from removing templates
        commaspace = text.index(" , ")
        text = text[:commaspace] + text[commaspace+1:]

    if text[-2] == " ":  # clean up accidental space
        text = text[:-2] + text[-1]
    return text
        # clean up the first sentence of the page; remove <ref> tags, templates, and bold, also watch for wikilinks, rm brackets

def run():
    linkloop = False
    real_link_list = []
    real_link_list_cap = []
    display_link_list = []
    fs_list = []
    pagetofind = "Pennsylvania"
    va_list = ["the arts", "earth", "human", "human history", "life", "mathematics", "philosophy", "science", "society", "technology"]
    while not linkloop:
        pagetext = getPageText(pagetofind)  # get the text of the page
        currentpage = pagetofind
        links = findLink(pagetext)  # find the link
        pagetofind = links[0][1]  # prep the next page
        time.sleep(0.2)
        if not checkRedirect(pagetext):  # if THE CURRENT PAGE NOT PAGE TO FIND IS NOT A REDIRECT
            fs_list.append(cleanFirstSentence(links[1]))  # add the sentence to the list
            if pagetofind.lower() in real_link_list:  # if it's not a redirect but is in the list, it's a loop
                real_link_list.append(currentpage.lower())
                real_link_list_cap.append(currentpage)
                display_link_list.append(links[0][0])
                linkloop = True
            elif pagetofind.lower() in va_list:  # if the next page is a VA
                real_link_list.append(currentpage.lower())
                real_link_list_cap.append(currentpage)
                real_link_list.append(pagetofind)
                real_link_list_cap.append(pagetofind)
                display_link_list.append(links[0][0])
                linkloop = True                
            else:
                real_link_list.append(currentpage.lower())
                real_link_list_cap.append(currentpage)
                display_link_list.append(links[0][0])

    for i in range(len(real_link_list_cap)):
        if ord(real_link_list_cap[i][0]) > 96:
            real_link_list_cap[i] = real_link_list_cap[i].capitalize()
    
    #print(real_link_list_cap, display_link_list)
    #for i in fs_list:
    #    print(i, "\n")
    return (real_link_list_cap, display_link_list, fs_list)