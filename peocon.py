#建立人物列表
import urllib.request as req
url=" https://zh.m.wikipedia.org/zh-tw/%E5%80%9A%E5%A4%A9%E5%B1%A0%E9%BE%8D%E8%A8%98%E8%A7%92%E8%89%B2%E5%88%97%E8%A1%A8 "
with req.urlopen(url) as response:
    data=response.read().decode("utf-8")
#print(data)

import bs4
soup = bs4.BeautifulSoup(data, "html.parser")
temps = soup.find_all("th")

path = 'names.txt'
with open(path, 'w', encoding="utf-8") as f:
    for i in range(0, len(temps)):
        if temps[i].a !=None and temps[i].a.string!=None :
            print(temps[i].a.string)
            f.write(temps[i].a.string+"\n")
        elif temps[i].string !=None and temps[i].string !="角色\n" and temps[i].string !="簡介\n":
                print(temps[i].string)
                if(temps[i].string[-1]=="\n"):
                    f.write(temps[i].string)
                else:
                    f.write(temps[i].string+"\n")

#f=open("graph.json","a",encoding="utf-8")aaaa