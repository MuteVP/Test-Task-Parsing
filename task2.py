from requests_html import HTML, HTMLSession

session = HTMLSession()

r = session.get('https://www.twitter.com/elonmusk/')  # HTTP запрос

a = 1
links_to_comm = []

r.html.render(scrolldown=4, sleep=5, timeout=20)
for i in range(0, 10):
    # в данном случае использование CSS-селекторов будет связано с ошибками при поиске и огромным количеством
    # дополнительных лишних данных. Использование xpath решает эту проблему, а также гарантирует отсутствие
    # ошибочных данных
    links_to_comm.append(str(r.html.xpath(
        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[' + str(
            i + 1) + ']/div/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/a')[
                                 0].absolute_links)[2:-2])

print(links_to_comm)

twit_text_only = []
norm_links = []
for i in range(0, 10):
    r = session.get(links_to_comm[i])
    r.html.render(scrolldown=2, sleep=5, timeout=20)
    twits_text = r.html.find('article[class="css-1dbjc4n r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh"]',
                             first=True)

    twit_text = str(twits_text.text).split('\n')


    if len(twit_text) > 2:
        twit_text_only.append(twit_text[2])
    else:
        twit_text_only.append('Twit is a picture or unavailable')


    commentators_links = r.html.find('article')
    n = 0
    tmp = []
    for links in commentators_links:
        if n > 0:
            links_1 = links.absolute_links
            for link in links_1:
                if str(link).find('/status/') == -1 and str(link).find('/elonmusk') == -1 and str(link).find(
                        '/photo/') == -1 and str(link).find('help.twitter') == -1 and str(link).find(
                        '/twitter.com/') != -1 and str(link).find(
                        '/t.co/') == -1 and link not in tmp:
                    tmp.append(link)
        n += 1
    norm_links.append(tmp)


for i in range(0, 10):
    print(i + 1, twit_text_only[i])
    print()
    print(norm_links[i][0], '\n', norm_links[i][1], '\n', norm_links[i][2])
    print()
    print()

