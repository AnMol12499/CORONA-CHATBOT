states=['Total',
 'Maharashtra',
 'Delhi',
 'Tamil Nadu',
 'Rajasthan',
 'Madhya Pradesh',
 'Telangana',
 'Gujarat',
 'Uttar Pradesh',
 'Andhra Pradesh',
 'Kerala',
 'Jammu and Kashmir',
 'Karnataka',
 'Haryana',
 'West Bengal',
 'Punjab',
 'Bihar',
 'Odisha',
 'Uttarakhand',
 'Himachal Pradesh',
 'Chhattisgarh',
 'Assam',
 'Jharkhand',
 'Chandigarh',
 'Ladakh',
 'Andaman and Nicobar Islands',
 'Goa',
 'Puducherry',
 'Manipur',
 'Tripura',
 'Mizoram',
 'Arunachal Pradesh',
 'Dadra and Nagar Haveli',
 'Nagaland',
 'Meghalaya',
 'Daman and Diu',
 'Lakshadweep',
 'Sikkim']

state_list=[['Total', 'Maharashtra'],
 ['Delhi', 'Tamil Nadu'],
 ['Rajasthan', 'Madhya Pradesh'],
 ['Telangana', 'Gujarat'],
 ['Uttar Pradesh', 'Andhra Pradesh'],
 ['Kerala', 'Jammu and Kashmir'],
 ['Karnataka', 'Haryana'],
 ['West Bengal', 'Punjab'],
 ['Bihar', 'Odisha'],
 ['Uttarakhand', 'Himachal Pradesh'],
 ['Chhattisgarh', 'Assam'],
 ['Jharkhand', 'Chandigarh'],
 ['Ladakh', 'Andaman and Nicobar Islands'],
 ['Goa', 'Puducherry'],
 ['Manipur', 'Tripura'],
 ['Mizoram', 'Arunachal Pradesh'],
 ['Dadra and Nagar Haveli', 'Nagaland'],
 ['Meghalaya', 'Daman and Diu']]

def query_state(statename=None):
    import requests as req
    url1="https://api.covid19india.org/data.json"
    r=req.get(url1)
    r1=r.json()
    states=r1['statewise']
    for i in states:
        if i['state']==statename:
            state=i['state']
            active=i['active']
            confirmed=i['confirmed']
            deaths=i['deaths']
            recovered=i['recovered']
            if statename=="Total":
                ans='TOTAL CASES TILL NOW IN INDIA\n\nACTIVE CASES: '+active+'\n\nCONFIRMED CASES: '+confirmed+'\n\nDEATHS CASES: '+deaths+'\n\nRECOVERED: '+recovered
            else:
                ans="STATE:"+state+'\n\nACTIVE CASES: '+active+'\n\nCONFIRMED CASES: '+confirmed+'\n\nDEATHS CASES: '+deaths+'\n\nRECOVERED: '+recovered
            return ans
            
def citiesOfState(city):
    import requests as req
    url2="https://api.covid19india.org/state_district_wise.json"
    r2=req.get(url2)
    cities=r2.json()
    dic={}
    for c,d in cities.items():
        l=[]
        x=list(d['districtData'].keys())
        dic.update({c:x})
    lis=[[i] for i in dic[city]]
    return lis

def cityCases(state,city):
    import requests as req
    url3="https://api.covid19india.org/v2/state_district_wise.json"
    r=req.get(url3)
    data=r.json()
    cities=None
    for i in data:
        if i['state']==state:
            cities=i['districtData']
            break
    for i in cities:
        if i['district']==city:
            s='STATE: '+state+"\n\n CITY: "+city+"\n\n CONFIRMED CASES:"+str(i['confirmed'])
            return s
            break

def currentTime():
    import datetime
    import pytz
    Timezone= pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(Timezone)
    current_time = now.strftime("%H:%M:%S")
    return current_time

def currentdate():
    import datetime
    import pytz
    Timezone= pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(Timezone)
    return now.strftime("%d-%m-%Y")

#add data to google sheets
def addProblem(problem,username,phone_no,address):
    import gspread as gs
    from oauth2client.service_account import ServiceAccountCredentials as sac
    scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials=sac.from_json_keyfile_name('XXXXXX.json',scope)
    gc=gs.authorize(credentials)
    wks=gc.open('xxxxx').worksheet('Sheet3')
    lis=[currentdate(),currentTime(),problem,username,phone_no,address]
    wks.append_row(lis)
    return "data is added"

#news from https://www.indiatoday.in/coronavirus-covid-19-outbreak?page&view_type=list
def latestnews():
    import requests  as req
    from bs4 import BeautifulSoup as bs
    urlbase='https://www.indiatoday.in'
    r=req.get("https://www.indiatoday.in/coronavirus-covid-19-outbreak?page&view_type=list")
    soup = bs(r.content,'lxml') 
    #print(soup.prettify()) 
    src=soup.find_all('div',{'class':'view-content'})
    w=src[0].find_all('div',{'class':'catagory-listing'})
    lis=[]
    for i in w:## title,description,link
        l=[]
        l.append(i.find('a').text)
        l.append(i.text)
        l.append(urlbase+i.find('a').attrs['href'])
        lis.append(l)
    return lis

def englishnews():
    from bs4 import BeautifulSoup
    import requests
    url1="https://timesofindia.indiatimes.com/times-fact-check"
    h1 = requests.get(url1).text
    s1 = BeautifulSoup(h1,'lxml')
    lis=[]
    for link in s1.findAll("a"):
        if (len(link.text.split(" ")) > 5):
            l=[]
            l.append(link.text)
            l.append(url1+str(link.get('href')))
            lis.append(l)
    return lis




def hindiNews():
    from bs4 import BeautifulSoup
    import requests
    url="https://www.bhaskar.com/no-fake-news/"
    h = requests.get(url).text
    s = BeautifulSoup(h,'lxml')
    lis=[]
    for link in s.findAll("a"):
        if (len(link.text.split(" ")) > 5):
            l=[]
            l.append(link.text)
            l.append(url+link.get('href'))
            lis.append(l)
    return lis






