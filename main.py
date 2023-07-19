from bs4 import BeautifulSoup

def fixWord(soup, line, word):
    word = list(word)

    bold_part = BeautifulSoup.new_tag(soup, 'b')
    pre = BeautifulSoup.new_tag(soup, 'span')
    post = BeautifulSoup.new_tag(soup, 'span')
    # bold_part['class'] = 'bd'
    pre['class'] = 'txt'
    post['class'] = 'txt'

    # append first half to bold part
    counter = 0
    for char in word:
        if counter == 0 and not char.isalpha():
            pre.append(char)
        elif counter < len(word)//2:
            counter += 1
            bold_part.append(char)
        else:
            post.append(char)
    line.extend([pre, bold_part, post, ' '])

with open('input.html') as html_file:
    soup = BeautifulSoup(html_file.read(), features='html.parser')

    # add style
    head = soup.head
    head.append(soup.new_tag('style', type='text/css'))
    head.style.append('b { line-height: 2; font-family: Helvetica; font-weight: bold; } .txt { font-family: Helvetica;font-weight: bold; color: #666666; } body {background-color:#edd1e0;}')

    for tag in soup.findAll('p'):
        # Remove all <i> tags - TODO: fix this
        if tag.string is None and tag.findAll('i') == []: continue
        line = BeautifulSoup.new_tag(soup, 'p')
        line.attrs = tag.attrs
        for word in tag.get_text().split(' '):
            fixWord(soup, line, word)
        tag.replace_with(line)

    # Store prettified version of modified html
    soup.smooth()
    new_text = soup.encode()

# Write new contents to test.html
with open('output.html', mode='w') as new_html_file:
    new_html_file.write(new_text.decode())


