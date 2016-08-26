import requests, bs4
from PIL import Image
from io import BytesIO
try:
    import cPickle as pickle
except:
    import pickle


def lookup(lst,  dbase, l):

    if l in dbase:
        for letter in dbase[l].keys():
            char_array = dbase[l][letter]
            char_array
            if char_array == lst:
                return letter    
        print(l, dbase[l].keys())
        return '?'
    else:
        return '?'      


def decyper(url, dbase):
    
    re = requests.get("https://who.is/" + url)
    if re.status_code == requests.codes.ok:
        im = Image.open(BytesIO(re.content))
    else:
        return "?"
    x,y  = im.size
    x = int(x/7)
    s = ""
    for i in range(x):
        lst = []
        crp = im.crop((i*7,0,i*7+7,13))
        for i in range(7):
            for j in range(13):
                pix = crp.getpixel((i,j))  
                if pix == (0,0,0):
                    lst.append(0)
                else:
                    lst.append(1)
        lst
        l = crp.getcolors()[0][0]
        s += lookup(lst , dbase, l)
    return s
    
    
    
def getpg(domain):
    s = 'https://who.is/whois/'+domain
    res = requests.get(s)
    if res.status_code == requests.codes.ok:
        doc = bs4.BeautifulSoup(res.text, "html.parser")
    else :
        return []
    dbase = pickle.load(open( "dictionary.p", "rb" ) )
    k = doc.select('.col-md-offset-1')
    val = doc.select('.col-md-7')
    for i in range(len(k)):
        t = str(k[i])
        k[i] = t[38:-6]
        t = str(val[i])
        val[i] = t[22:-6]
        if k[i] == "Email":
           temp = t[32:-9]
           val[i] = decyper(temp, dbase)
    return k,val
    
def convert(k, l):
    diction = {}
    for i in range(len(l)):
        diction[k[i]] = l[i]
    return diction  
    
if __name__ == "__main__":
    k,val = getpg(input("Enter Domain name : "))
    dct =  convert(k,val)
    print(dct)
