from bs4 import BeautifulSoup
from bs4 import NavigableString

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

with open('pg2554-images.html') as html_file:
    soup = BeautifulSoup(html_file.read(), features='html.parser')

    # add style
    head = soup.head
    head.append(soup.new_tag('style', type='text/css'))
    head.style.append('p.m { font-family: Helvetica;font-weight: bold; color: #666666; } p.m b { line-height: 2; font-family: Helvetica; font-weight: bold; color: #111111 } body {background-color:#edd1e0;}')

    for tag in soup.findAll('p'):
        # Remove all <i> tags - TODO: fix this
        if tag.findAll('i') != [] or tag.findAll('br') != [] or tag.findAll('strong') != [] or tag.findAll('a') != []: 
            line = BeautifulSoup.new_tag(soup, 'p')
            line.attrs = tag.attrs
            line.attrs['class'] = line.get('class', []) + ['m']
            array = []
            for child in tag.children:
                if child.name != 'i' and child.name != 'br' and child.name != 'strong' and child.name != 'a':
                    for word in child.get_text().split(' '):
                        array += fixWord(soup, word)
                elif child.name == 'br':
                    array += child
                elif child.name == 'strong' or child.name == 'i' or child.name == 'a':
                    italic = BeautifulSoup.new_tag(soup, child.name)
                    italic.attrs = child.attrs
                    for word in child.get_text().split(' '):
                        italic.extend(fixWord(soup, word))
                    line.extend(array)
                    array = []
                    line.append(italic)
            line.extend(array)
            tag.replace_with(line)
        elif tag.get_text() is not None:
            line = BeautifulSoup.new_tag(soup, 'p')
            line.attrs = tag.attrs
            line.attrs['class'] = line.get('class', []) + ['m']
            for word in tag.get_text().split(' '):
                line.extend(fixWord(soup, word))
            tag.replace_with(line)

    # Store prettified version of modified html
    # soup.smooth()
    new_text = soup.encode()

# Write new contents to test.html
with open('output.html', mode='w') as new_html_file:
    new_html_file.write(new_text.decode())


