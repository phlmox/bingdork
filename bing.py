import sys,requests,getopt
from bs4 import BeautifulSoup

def help():
    print("-h, --help : Help")
    print("-q, --query : Query")
    print("-p, --page : Page number")
    print("-s, --silent : Silent mode")
    print("-u, --url : Print only urls")
    print(48*"-")
    sys.exit(0)

def bing(q,pg):
    o=[]
    u="https://www.bing.com/search?q="+q+"&first=11"
    r = requests.get(u,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
    soup = BeautifulSoup(r.content,"lxml")
    results = soup.findAll("li",attrs={"class":"b_algo"})
    if not silent:
        print("[+] Found {} results in page 1".format(str(len(results))))
    for res in results:
        o.append([res.find("h2").text,res.find("a")["href"]])
    if pg==1:
        return o
    i=len(results)
    for p in range(1,pg):
        u="https://www.bing.com/search?q="+q+"&first="+str((p*i)+1)
        r = requests.get(u,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
        soup = BeautifulSoup(r.content,"lxml")
        results = soup.findAll("li",attrs={"class":"b_algo"})
        if not silent:
            print("[+] Found {} results on page {}".format(str(len(results)),p+1))
        for res in results:
            o.append([res.find("h2").text,res.find("a")["href"]])
    return o

silent=False
onlyUrls=False
query=""
page=1
opts,args = getopt.getopt(sys.argv[1:],"hq:p:su",["help","query","page","silent","url"])

for o,a in opts:
    if o in ("-h","--help"):
        help()
    elif o in ("-q","--query"):
        query=a
    elif o in ("-p","--page"):
        page=int(a)
    elif o in ("-s","--silent"):
        silent=True
    elif o in ("-u","--url"):
        onlyUrls=True

if not silent:
    print("""     _     _                 _            _    
    | |   (_)               | |          | |   
    | |__  _ _ __   __ _  __| | ___  _ __| | __
    | '_ \| | '_ \ / _` |/ _` |/ _ \| '__| |/ /
    | |_) | | | | | (_| | (_| | (_) | |  |   < 
    |_.__/|_|_| |_|\__, |\__,_|\___/|_|  |_|\_\\
                    __/ |                      
                    |___/                       """)
    print(48*"-")

if not len(query):
    help()

for i in bing(query,page):
    if not onlyUrls:
        print(i[0],i[1])
    else:
        print(i[1])