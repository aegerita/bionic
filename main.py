from bs4 import BeautifulSoup
from bs4 import NavigableString

def fixWord(soup, line, word):
    word = list(word)

    bold_part = BeautifulSoup.new_tag(soup, 'b')
    pre = NavigableString('')
    post = NavigableString('')

    # append first half to bold part
    counter = 0
    for char in word:
        if counter == 0 and not char.isalpha():
            pre += char
        elif counter < len(word)//2:
            counter += 1
            bold_part.append(char)
        else:
            post += char
    if bold_part.get_text() == '': line.extend([pre, post, ' '])
    else: line.extend([pre, bold_part, post, ' '])

with open('input.html') as html_file:
    soup = BeautifulSoup(html_file.read(), features='html.parser')

    # add style
    head = soup.head
    head.append(soup.new_tag('style', type='text/css'))
    head.style.append('p.m { font-family: Helvetica;font-weight: bold; color: #666666; } p.m b { line-height: 2; font-family: Helvetica; font-weight: bold; color: #111111 } body {background-color:#edd1e0;}')

    for tag in soup.findAll('p'):
        # Remove all <i> tags - TODO: fix this
        if tag.string is None and tag.findAll('i') == []: continue
        line = BeautifulSoup.new_tag(soup, 'p')
        line.attrs = tag.attrs
        line.attrs['class'] = 'm'
        for word in tag.get_text().split(' '):
            fixWord(soup, line, word)
        tag.replace_with(line)

    # Store prettified version of modified html
    soup.smooth()
    new_text = soup.encode()

# Write new contents to test.html
with open('output.html', mode='w') as new_html_file:
    new_html_file.write(new_text.decode())


