from bs4 import BeautifulSoup
from bs4 import NavigableString
import re

def fixWord(soup, word):
    bold_part = BeautifulSoup.new_tag(soup, 'b')
    pre = NavigableString('')
    post = NavigableString('')

    # append first half to bold part
    counter = 0
    for char in list(word):
        if counter == 0 and not char.isalpha() and not char.isupper():
            pre += char
        elif counter < len(word)//2:
            if char.islower(): counter += 1
            bold_part.append(char)
        else:
            post += char
    if counter == 0: return [NavigableString(word + ' ')]
    else: return [pre, bold_part, post, ' ']

with open('crimeandpunishment.html') as html_file:
    soup = BeautifulSoup(html_file.read(), features='html.parser')

    # add style
    head = soup.head
    head.append(soup.new_tag('style', type='text/css'))
    head.style.append('p.m { font-family: Helvetica; font-weight: bold; color: #666666; } p.m b { line-height: 2; font-family: Helvetica; font-weight: bold; color: #111111 } body { background-color:#edd1e0; }')

    for tag in soup.findAll('p') + soup.findAll(re.compile("^h[1-6]$")) + soup.findAll('span'):
        # Remove all <i> tags - TODO: fix this
        line = BeautifulSoup.new_tag(soup, tag.name)
        line.attrs = tag.attrs
        line.attrs['class'] = tag.get('class', []) + ['m']
        if tag.findAll('i') + tag.findAll('br') + tag.findAll('strong') + tag.findAll('a') + tag.findAll('code')+ tag.findAll('em'):
            array = []
            for child in tag.children:
                if child.name not in ['br', 'code', 'strong', 'i', 'a', 'em']:
                    for word in child.get_text().split(' '):
                        array += fixWord(soup, word)
                elif child.name == 'br':
                    array += child
                elif child.name in ['strong', 'a', 'code', 'i', 'em']:
                    italic = BeautifulSoup.new_tag(soup, child.name)
                    italic.attrs = child.attrs
                    for word in child.get_text().split(' '):
                        # if child.name == 'code':
                        #     italic.append(word)
                        # else:
                            italic.extend(fixWord(soup, word))
                    line.extend(array)
                    array = []
                    line.append(italic)
            line.extend(array)
            tag.replace_with(line)
        elif tag.string is not None:
            for word in tag.get_text().split(' '):
                line.extend(fixWord(soup, word))
            tag.replace_with(line)

    # Store prettified version of modified html
    # soup.smooth()
    new_text = soup.encode()

# Write new contents to test.html
with open('crimeandpunishment_output.html', mode='w') as new_html_file:
    new_html_file.write(new_text.decode())


