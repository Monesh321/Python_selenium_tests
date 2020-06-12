import itertools

import requests
import bs4
import difflib

url_list1 = ["https://www.sunlife.com.hk/HK?vgnLocale=en_CA"]
url_list2 = ["https://www.sunlife.com.hk/HK/Life+Moments?vgnLocale=en_CA"]


def read_url(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'lxml')
    html = str(soup)
    html_lines = html.splitlines()
    # count = 0
    # for line in html_lines:
    #     print("LINE {}:".format(count), line)
    #     count = count + 1
    return html_lines


count = 0
for url1, url2 in itertools.zip_longest(url_list1, url_list2):
    pass
    url1_lines = read_url(url1)
    url2_lines = read_url(url2)

    difference = difflib.HtmlDiff(wrapcolumn=80, tabsize=8).make_file(url1_lines, url2_lines,
                                                                      fromdesc="stage", todesc="wem")
    with open('HK_difference_report_' + str(count) + '.html', 'w') as htmlfile:
        htmlfile.write(difference)
    count = count + 1
