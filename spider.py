from selenium import webdriver
import matplotlib.pyplot as plt
from time import sleep
from progress.bar import Bar
from bs4 import BeautifulSoup
import networkx as nx



def get_hrefs( driver , main_url):
    try:
        driver.get(main_url)
        #sleep depends on internet velocity, if internet is faster sleep can be slower
        sleep(1)
        webpage_content = driver.find_element_by_xpath("/html")
        content = webpage_content.get_attribute("innerHTML")
        soup = BeautifulSoup(content , "lxml")
        elements_with_hrefs = soup.find_all("a")
        hrefs = []
        for i in elements_with_hrefs:
            link = i['href']
            try:
                if(link[0]== "/"):
                    link = main_url+link
            except:
                pass
            try:
                if(link[0]!= "h"):
                    link = main_url+"/"+link
            except:
                pass
            hrefs.append(link)
        return(hrefs)
    except:
        return([])

def check_list(elem , lista):
    for i in lista:
        if(elem == i["son"]):
            return(False)
    return(True)

def recursively_scrawl(driver , main_url , deph):
    start = get_hrefs(driver , main_url)
    first = []
    for i in start:
        father = main_url
        son = i
        couple = {
            "father":father,
            "son":son
        }
        first.append(couple)

    for i in range(deph-1):
        print("\n {} recursion".format(i+1))
        bar = Bar("progress..." , max=len(first))
        for num in range ( len(first)):
            bar.next()
            j = first[num]
            hrefs = get_hrefs(driver, j["son"])
            for k in hrefs:
                if(check_list(k , first)):
                    father = j
                    son = k
                    couple = {
                        "father":father,
                        "son":son
                    }
                    first.append(couple)
            #print(len(first) , i+1 )
    return(first)

def generate_graph(son_father_list):
    touples = []
    G = nx.Graph()
    for i in son_father_list:
        left = i["father"]
        right = i["son"]
        touple = (left,right)
        touples.append(touple)
        try:
            G.add_edges_from(touples)
        except Exception as e:
            print("error in {} , error:{}".format(touple,e))
            touples.remove(touple)
    print(touples)
    nx.draw(G)
    plt.show()





driver = webdriver.Chrome()
cont = recursively_scrawl(driver , "https://tmedweb.tulane.edu/content_open" , 2 )
generate_graph(cont)
driver.close()

