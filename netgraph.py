#建圖
import json
import collections
import networkx as nx
import urllib.request as req
import matplotlib.pyplot as plt
def getdata(url):
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
        return data
# print(data)



#main
if __name__ == '__main__':
    url=" http://big5.quanben-xiaoshuo.com/n/yitiantulongji/1.html "
    #print(data)
    import bs4
    G = nx.Graph()                                                      #建無向圖

    path ='names.txt'                                                   #建點
    with open(path, 'r', encoding="utf-8") as f:
        while True:                                                 #有吃到names
            name1=f.readline()
            if not name1 :
                break
            #print(name1)
            G.add_node(name1.strip(),value=0)                       #remove \n
        #print(list)
        #G.add_node(list)
        #print(G.nodes.data())
    while True:
        data=getdata(url)
        soup = bs4.BeautifulSoup(data, "html.parser")
        temp = soup.find("div", class_ = "articlebody")
        contents = temp.find_all("p")
        if data is None or temp is None or contents is None:
            break
        for i in range(len(contents)):
            #print(contents[i].string)                                      #contents是小說一段內容
            #print("lalala")
            #list=[]                                                        #建點用
            partlist=[]                                                     #存關聯
            #print(contents[i])
            with open(path, 'r', encoding="utf-8") as f:       #wiki names
                #for content in contents:
                while True:                                    #有吃到names
                    name1=f.readline()
                    #print(name1)
                    #print(contents[i])
                    if not name1 :
                        break
                    if contents[i].string.count(name1.strip()) > 0:
                        partlist.append(name1.strip())
                        G.nodes[name1.strip()]['value']+=contents[i].string.count(name1.strip())
                        #print(G[name1.strip()])                                                #????

            #print(G.nodes.data())
            #print(partlist)
            for j in range(len(partlist)):
                #print(j)
                for k in range(j+1,len(partlist)):
                    #print(k)
                    if G.has_edge(partlist[j], partlist[k]):    # 兩點已經存在一條邊
                        G[partlist[j]][partlist[k]]["weight"] += 1
                    else: 
                        G.add_edge(partlist[j], partlist[k], weight=1)
            #print(G.nodes.data())
            #print(G.edges.data())
        #print("end!!!!")
        temp=soup.find("div",class_="tc").find("a",rel="next")
        if temp is None:
            break
        #print(temp)
        url="http://big5.quanben-xiaoshuo.com"+temp["href"]
        
        print(url)
    print("all done!!!")
    #print(G.nodes.data())
    #print(G.edges.data())
    f=open("graph.json","w",encoding="utf-8")
    nodes=list()
    links=list()
    for u,v in G.nodes(data='value'):
        if v>200: 
            color="red"
        elif v>100:
            color="orange"
        elif v>50:
            color="yellow"
        elif v>25:
            color="green"
        elif v>0:
            color="blue"
        else:
           color="gray"
        nodes.append({"id": u, "color": color, "value": v})
        print(u,color,v)
    for na1,na2,w in G.edges(data='weight'):
        links.append({"sourcr": na1, "target": na2, "weight": w})
        print(na1,na2,w)
    sortna = sorted(nodes, key=lambda k: k['value'], reverse=True)
    sortga = sorted(links, key=lambda k: k['weight'], reverse=True)
    json_data = {"nodes": sortna, "links": sortga}
    json.dump(json_data,f,ensure_ascii=False,indent=4)
