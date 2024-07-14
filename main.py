from flask import Flask, request, redirect,  session
from replit import db
from datetime import datetime, timedelta
import requests, json, os,  time, random
import datetime


app = Flask(__name__, static_url_path="/static")


#Setting sessions to store data.




app.secret_key = os.environ["session_key"]


#db["salt"] = "123456"
#db["detail"] = {"name": "owais", "password": os.environ["password"]}

print(db["detail"]["password"])
#print(db.keys())



#Function to add entries in main page and avoid repetation.

def journal():
  keyse = db.keys()
  fi = open("file.doc", "w")

  #Retrieving data from data base.
  
  for k in keyse:
    if k != "salt":
      if k != "detail":
        fi.write(str(db[k]["contents"]))
      #print("NONE!")
 
  
  fi.close()
  g = open("file.doc", "r")
  age = (g.read())
  g.close()
  return age

def scraper():
  
  #SCRApping part!
  
  url = "https://api.quotable.io"
  want = "random"
  response = requests.get(f"{url}/{want}")
  quote = response.json()["content"]
  A_name = response.json()["author"]
  qoute_d = f'''{quote}\n'Author : {A_name}'''
  
  return qoute_d


def feorm():
  p = open("form.html", "r")
  page = p.read()
  return page


@app.route('/')

#Login page
def index():

  #Authentication, if user has already logged in. Then user will be diirected to user interface.
  
  if session.get("username"): 
    return redirect("/home")
  
  else:
    f = open("login.html", "r")
    page = f.read()
    return page

#Note:
# =====   understood     
#   ==========================================   #




@app.route('/logon',  methods=["POST"])

 #login validation
def leo():
  
  response = request.form
  username = response['username']
  password = response["password"]
  salt = db["salt"] 
  
  if session.get("username"):
    return redirect("/home")
  
  else:
    if db["detail"]["password"] == password and db["detail"]["name"] == username:
      session["username"] = username
      return redirect("/home")
    
    else:
      return "wrong username or password."
  #return "hello!"

      #Note:
      # =====   understood
      #   ==========================================   #





@app.route('/home')
#Home page or userinterface, all the entries will be displayed on this page, and a form to plan your day.

def hiomme():
  
  
  if session.get("username"):
    
    f = open("flexbox.html", "r")
    page = f.read()
    page = page.replace("task", journal())
    page = page.replace("quote", scraper())
    page = page.replace("entry", feorm())
    return page
  
  else:
    return redirect("/")




#Note:
# =====   understood
#   ==========================================   #





@app.route('/1', methods=["POST"])

#This page will make changes in the template, in accordance with the form entries, and from there it will be send to page /2.

def home():
  
  #to avoid loopholes, and improve security we have added authentication. 
  #on this page we have two part's, i will explain both seprately.
  
  if session.get("username"):
    
    #First Part
    #In first part we make changes in html based template of our task's list, replace tasks with actual entries from form's entered by user as their tasks. Html file "template.html also work as a form to fill check boxes." 
    
    date = str(datetime.date.today())
    day = str(datetime.datetime.now().strftime("%A"))
    
    
    response = request.form
    
    f = open("template.html", "r")
    page = f.read()
    
    page = page.replace("t1", response["t1"]) 
    page = page.replace("t2", response["t2"])
    page = page.replace("t3", response["t3"])
    page = page.replace("t4", response["t4"])
    page = page.replace("t5", response["t5"])
    page = page.replace("date", date)
    page = page.replace('day', day)

    
#Second Part  
#in second part, we open same kind of template like we did in first part, but difference is that, it has no form elements. it is just used to save tasks obtained in part 01. later we can use this file to update our status of taks, and reflections in page "/2".
    
    g = open("basictemplate.html", "r")
    age = g.read()
    age = age.replace("t1", response["t1"])
    age = age.replace("t2", response["t2"])
    age = age.replace("t3", response["t3"])
    age = age.replace("t4", response["t4"])
    age = age.replace("t5", response["t5"])
    age = age.replace("date", date)
    age = age.replace('day', day)
   

    #Formation of file "tissue.doc remains undefined. I can't figure out, why it is being used??"
    
    h = open("tissue.doc", "w")
    h.write(str(age))
    h.close()
    return page
  
  
  else:
    return redirect("/")

@app.route('/2', methods=["POST"])

#on this page it will update status of tasks. Finally it will be added to database for access.

def two():
  
  date = str(datetime.date.today())

  
  f = open("tissue.doc", "r")
  response = request.form
  page = f.read()

  page = page.replace("status01", response["status01"])
  page = page.replace("status02", response["status02"])
  page = page.replace("status03", response["status03"])
  page = page.replace("status04", response["status04"])
  page = page.replace("status05", response["status05"])
  
  page = page.replace("reflections", response["reflections"])

  
  chabi = db.keys()
  
  g = open("tissue.doc", "r")
  age = g.read()
  
  age = page.replace("status01", response["status01"])
  age = page.replace("status02", response["status02"])
  age = page.replace("status03", response["status03"])
  age = page.replace("status04", response["status04"])
  age = page.replace("status05", response["status05"])
  age = page.replace("reflections", response["reflections"])
  age = page.replace("HOME", "")


  #I am undoing, date condition just for experiment.

  #REMINDER AGAIN: DATE CONDITION SHOULD BE REMOVED AFTER TESTING.  
  
  #if date not in chabi:

    #structur of our entries in database is, DATE as main key and "contents" as sub key. To avoid duplication we are using DATE as our main key.
    
  db[str(date)] = {"contents":str(age)}
    
  
  #finally task along with their updated status with reflections will be displayed, and saved in database.
  
  return page





@app.route('/reset')
def rset():
  if session.get("username"):
    session.clear()
    return redirect("/")
  else:
    return redirect("/home")



app.run(host='0.0.0.0', port=81)
