#!/usr/bin/env python3

"""piclister"""

import sys
#import string
import re
import os
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser #, HTMLParseError
#from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    """my html parser"""
    # pylint: disable=missing-function-docstring

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_script = 0
        self.urls = []

    def reset(self):
        HTMLParser.reset(self)
        self.urls = []
        self.in_script = 0

    #def handle_comment(self, data):
    #    print 'comment', data

    def do_div(self, attrs):
        #print "DIV",attrs
        href = [v for k, v in attrs if k in ('data-image', 'data-lazy')]
        if href and not self.in_script:
            self.urls.extend(href)

    def do_script(self, _attrs):
        self.in_script = 1
        #print 'script start'

    def end_script(self):
        self.in_script = 0
        #print 'script end'

    def do_a(self, attrs):
        #print 'do_a'
        href = [v for k, v in attrs if k=='href']
        #print href, attrs
        if href and not self.in_script:
            self.urls.extend(href)

        onclick = [v for k, v in attrs if k=='onclick']
        if onclick and not self.in_script:
            self.urls.extend(onclick)

    def do_area(self, attrs):
        href = [v for k, v in attrs if k=='href']
        #print href
        if href and not self.in_script:
            self.urls.extend(href)

    def do_embed(self, attrs):
        href = [v for k, v in attrs if k=='src']
        #print href
        if href and not self.in_script:
            self.urls.extend(href)

    def do_link(self, attrs):
        href = [v for k, v in attrs if k=='href']
        #print href
        if href and not self.in_script:
            self.urls.extend(href)

    def do_img(self, attrs):
        #print "IMG",attrs
        src = [v for k, v in attrs if k=='src']
        #print src
        if src and not self.in_script:
            self.urls.extend(src)

    def do_frame(self, attrs):
        src = [v for k, v in attrs if k=='src']
        #print src
        if src and not self.in_script:
            self.urls.extend(src)

    def do_iframe(self, attrs):
        src = [v for k, v in attrs if k=='src']
        #print src
        if src and not self.in_script:
            self.urls.extend(src)

    def do_option(self, attrs):
        value = [v for k, v in attrs if k=='value']
        #print value
        if value and not self.in_script:
            self.urls.extend(value)

    def do_body(self, attrs):
        background = [v for k, v in attrs if k=='background']
        #print background
        if background and not self.in_script:
            self.urls.extend(background)

    def do_td(self, attrs):
        background = [v for k, v in attrs if k=='background']
        #print background
        if background and not self.in_script:
            self.urls.extend(background)

    #def do_title(self, attr):
    #    print "do_title"

    def handle_starttag(self, tag, attrs):
        #print 'Encountered the beginning of a <%s> tag' % tag
        #print attrs
        # pylint: disable=multiple-statements
        if tag == 'a':      self.do_a(attrs)
        if tag == 'area':   self.do_area(attrs)
        if tag == 'embed':  self.do_embed(attrs)
        if tag == 'link':   self.do_link(attrs)
        if tag == 'img':    self.do_img(attrs)
        if tag == 'frame':  self.do_frame(attrs)
        if tag == 'iframe': self.do_iframe(attrs)
        if tag == 'option': self.do_option(attrs)
        if tag == 'body':   self.do_body(attrs)
        if tag == 'script': self.do_script(attrs)
        if tag == 'td':     self.do_td(attrs)
        if tag == 'div':    self.do_div(attrs)
        #if tag == 'title':  self.do_title(attrs)

    def handle_endtag(self, tag):
        #print 'Encountered the end of a </%s> tag' % tag
        if tag == 'script':
            self.end_script()

    #def handle_data(self, data):
        #print "handle_data -[%d] %s" % (len(data), repr(data))
        #for x in data:
        #    print x

    def handle_charref(self, name):
        pass
        #if name.startswith('x'):
        #    c = chr(int(name[1:], 16))
        #else:
        #    c = chr(int(name))
        #print "Num ent  :", c

    def handle_entityref(self, name):
        print("entityref",name)
        #c = unichr(name2codepoint[name])
        #print "Named ent:", c

    def clear_hrefs(self):
        self.urls = []

    def get_links(self):
        return self.urls


def piclister(url1):
    """piclister - not called internally"""
    #usock = urllib.request.urlopen(url)
    with urllib.request.urlopen(url1) as usock:
        parser = MyHTMLParser()
        parser.feed(usock.read())
        parser.close()
    #usock.close()
    ret_urls = []
    #print parser.urls
    for url in parser.urls:
        if url.find('avascript') > 0:
            url2 = url[url.find("'"):url.find(",")]
            print('\n',url2,'\n')
            ret_urls.append(url2[url2.find("'")+1:url2.rfind("'")])
            print('javascript--', url2[url2.find("'")+1:url2.rfind("'")])
        else:
            ret_urls.append(url)
    return ret_urls

def piclister_main(html, _url):
    """piclister_main"""
    #print "main()"
    output=[]
    try:
        #for l in html.split('\n'):
        #    if l.find('Cote') > -1:
        #        print l
        parser = MyHTMLParser()
        parser.clear_hrefs()
        parser.feed(html)

    except AttributeError:
        #print "AttributeError"
        #sock.close()
        raise
        #return []

    #except HTMLParseError:
    #    print('HTMLParser.HTMLParseError processing %s' % (url), file=sys.stderr)
    #    raise

    except Exception:
        #print os.path.join(self.basedir, filename)
        print('exception returned', sys.exc_info()[0])
        #sock.close()
        raise
        #return []

    else:
        #print 'else', parser.get_links()
        for link in parser.get_links():
            if link.find('avascript') > 0:
                url2=link[link.find("'"):link.find(",")]
                #print '\n',url2,'\n'
                output.append(url2[url2.find("'")+1:url2.rfind("'")])
                #print 'javascript--', url2[string.find(url2,"'")+1:string.rfind(url2,"'")]

            else:
                #ret_urls.append(url)
                output.append(link)
        #sock.close()

    return output

    #for u in output:
    #    #print url, ':- ', u
    #    print u



def printresults(output):
    """print results"""
    for line in output:
        #print url, ':- ', u
        print(line)



def main():
    """main version 2"""

    if len(sys.argv) > 1:
        for url in sys.argv[1:]:
            #print "call piclister_main()"
            print("[DEBUG] {url}\n")
            if os.path.exists(url):
                #html = open(url, 'r').read()
                with open(url, 'r', encoding='utf-8') as furl:
                    html = furl.read()
            else:
                try:
                    #html_bytes = urllib.request.urlopen(url).read()
                    with urllib.request.urlopen(url) as furl:
                        html_bytes = furl.read()
                        html = str(html_bytes, 'utf-8').replace('! -', '!-')
                except TypeError:
                    print("Exception Raised:  TypeError")
                    print(url)
                    #print(urllib.request.urlopen(url).read())
                    with urllib.request.urlopen(url) as furl:
                        print(furl.read())
                    raise
            #html = html.replace('&#039;','').replace('&#8217;','')
            found = True
            while found:
                match = re.search('&#[0-9]*;', html)
                if match is not None:
                    print(match.group(0))
                    html = html.replace(match.group(0),'')
                else:
                    found = False
            html = html.replace('&bull;','') #.replace(';','')
            html = html.replace('"!</','"></')
            out = piclister_main(html, url)
            printresults(out)
    else:
        html = sys.stdin.read()
        out = piclister_main(html.replace(';',''), "stdin")
        printresults(out)


if __name__ == "__main__":
    main()
