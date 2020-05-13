 #polling program
#import logging
import telegram
from flask import Flask,request
from telegram.ext import CommandHandler,MessageHandler,Filters,Dispatcher
from telegram import Bot,Update,ReplyKeyboardMarkup,KeyboardButton
#from test import get_reply,fetch_news,topics_keyboard
from testing import states,state_list,query_state,citiesOfState,cityCases,addProblem,latestnews,hindiNews,englishnews



#logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',level=logging.INFO)
#logger=logging.getLogger(__name__)


TOKEN="XXXXXX"
app=Flask(__name__)

@app.route(f'/{TOKEN}',methods=["GET","POST"])
def webhook():
	update=Update.de_json(request.get_json(),bot)
	dp.process_update(update)
	return "OK"

@app.route('/')
def index():
	return "hello anmol"

def start(bot,update):
	print(update)
	author=update.message.from_user.first_name
	lastname=update.message.from_user.last_name
	reply="Hi ! {}".format(author+" "+lastname)+"This Bot can be used: \n->To Track Coronavirus Cases based on StateWise (/selectstate) and City wise(/selectcity) \n->To Register Problem to Higher Authorities (/help)\n->To get Helpline numbers and share your location and contact in case of emergency (/helpline)\n ->Answers To Frequent Asked Questions about COVID19 (/faq)\n->To see the fake news viral in Social Media & read it to verify it in Hindi (/hindifakenewscheck) & in English (/englishfakenewscheck)"
	bot.send_message(chat_id=update.message.chat_id,text=reply)


def _help(bot,update):
    help_txt="Hey! This is a Helpline Call..Check The Pdf containing The Helpline Numbers For Different states By Central Govt.."
    #bot.send_chat_action(chat_id=update.message.chat_id,action=chataction.ChatAction.TYPING)
    #sharing contact and location
    bot.send_message(chat_id=update.message.chat_id,text=help_txt)
    bot.send_document(chat_id=update.message.chat_id,document="https://www.mohfw.gov.in/pdf/coronvavirushelplinenumber.pdf")
    location_keyboard = KeyboardButton(text="send_location", request_location=True)
    contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard,one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id, text="You can share your contact / location with us in Case Of Emergency?", reply_markup=reply_markup)


# this will reply to user
state =None
city=None
problem=None
address=None
phone_number=None


    
def reply_text(bot,update):
	global state
	global city
	global problem
	global address
	global phone_number

	msg=update.message.text

	print(msg)
	if "#PROBLEM:" in msg and problem==None:
		p=msg.split(":")
		if(p[1]!=""):
			problem=p[1]
			ans="Your Problem has been Listed..\nTell me your Full Address with Starting with #ADDRESS:"
			bot.send_message(chat_id=update.message.chat_id,text=ans)
		else:
			ans="Sorry Problem not registered Please try again in given Format.."
			bot.send_message(chat_id=update.message.chat_id,text=ans)
			problem=None

	elif "#ADDRESS:" in msg and address==None and problem!=None:
		a=msg.split(":")
		if(a[1]!=""):
			address=a[1]
			ans="Your Address has been Listed..\nKindly Share your phone_number !!! "
			contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
			custom_keyboard = [[contact_keyboard]]
			reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard,one_time_keyboard=True)
			bot.send_message(chat_id=update.message.chat_id,text=ans, reply_markup=reply_markup)
		else:
			ans="Sorry Address has not been registered Please try again in given Format.."
			bot.send_message(chat_id=update.message.chat_id,text=ans)
			address=None
	elif msg=="YES" and address!=None and problem!=None and phone_number!=None:
		author=update.message.from_user.first_name
		lastname=update.message.from_user.last_name
		username=author+' '+lastname
		addProblem(problem,username,address,phone_number)
		ans="Your Problem has Been registered!!Will get Back To you Soon...Thank You"
		bot.send_message(chat_id=update.message.chat_id,text=ans)
		address=None
		phone_number=None
		problem=None
	elif msg=="NO":
		ans="your Problem is cancelled  .Please Try again later!!!..."
		bot.send_message(chat_id=update.message.chat_id,text=ans)
		address=None
		phone_number=None
		problem=None



	elif msg not in states and state!=None and city==None:
		city=msg
		x=cityCases(state,city)
		bot.send_message(chat_id=update.message.chat_id,text=x)
		city=None
	elif msg in states:
		state=msg
		x=query_state(state)
		bot.send_message(chat_id=update.message.chat_id,text=x)
		print(x)
	else:
		ans="INVALID QUERY!!!"
		
		bot.send_message(chat_id=update.message.chat_id,text=ans)


 
def echo_sticker(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)

#def error(bot,update):
#    logger.error("Update '%s' caused error '%s'",update,update.error)


def statewise(bot,update):
	#print("hello")
	bot.send_message(chat_id=update.message.chat_id,text="CHOOSE STATE TO SEE CASES:!!!",reply_markup=ReplyKeyboardMarkup(keyboard=state_list,one_time_keyboard=True))

def SelectCity(bot,update):

	if state in states or state!='Total':
		lis=citiesOfState(state)
		print(lis)
		bot.send_message(chat_id=update.message.chat_id,text="CHOOSE CITY OF SELECTED STATE TO SEE CASES:!!!",reply_markup=ReplyKeyboardMarkup(keyboard=lis,one_time_keyboard=True))
	if state not in states or state=='Total'or state==None :
		ans="You Have not Selected Any State...Please Select State From Given List...."
		print("hello")
		bot.send_message(chat_id=update.message.chat_id,text=ans)
		statewise(bot,update)


def pic(bot,update):
	print('pic sent by someone')
	print(state=update.message.photo)

def FAQ(bot,update):
	#https://www.mohfw.gov.in/pdf/FAQ.pdf
    help_txt="Hey This PDF Contains The Frequent Asked Questions Related To COVID-19"
    #bot.send_chat_action(chat_id=update.message.chat_id,action=chataction.ChatAction.TYPING)
    #sharing contact and location
    bot.send_message(chat_id=update.message.chat_id,text=help_txt)
    bot.send_document(chat_id=update.message.chat_id,document="https://www.mohfw.gov.in/pdf/FAQ.pdf")


def contact_callback(bot, update):
	global phone_number
	contact = update.effective_message.contact
	phone = contact.phone_number
	phone_number=phone
	ans="Your Mobile no has been Listed."
	bot.send_message(chat_id=update.message.chat_id,text=ans)
	custom_keyboard = [["YES", "NO"]]
	reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard,one_time_keyboard=True)
	ans="Now Choose YES/NO To Confirm To Register The Problem to Authorities.."
	bot.send_message(chat_id=update.message.chat_id,text=ans, reply_markup=reply_markup)



	

def need_help(bot,update):
	global problem
	global phone_number
	global address
	problem=None
	phone_number=None
	address=None
	help_txt="Write About the Problem in brief you are Facing During this Disastrous Situation in the Given Format.\n #PROBLEM:"
	bot.send_message(chat_id=update.message.chat_id,text=help_txt)


def getnews(bot,update):
	lis=latestnews()
	for i in lis:
		news="TITLE:- "+i[0]+'\nDESCRIPTION:- '+i[1]+'\nLINK TO READ MORE :- '+i[2]
		bot.send_message(chat_id=update.message.chat_id,text=news)
	txt="For more News related To COVID19, Kindly Visit This site - https://www.indiatoday.in/coronavirus-covid-19-outbreak?page&view_type=list"
	bot.send_message(chat_id=update.message.chat_id,text=txt)


def hindifakenews(bot,update):
	print("hindifakenews")
	lis=hindiNews()[:10]
	for i in lis:
		news='\nDESCRIPTION:- '+i[0]+'\nLINK TO READ MORE :- '+i[1]
		bot.send_message(chat_id=update.message.chat_id,text=news)
	txt="For more News, Kindly Visit This site - https://www.bhaskar.com/no-fake-news/"
	bot.send_message(chat_id=update.message.chat_id,text=txt)

def englishfakenews(bot,update):
	print("englishfakenews")
	lis=englishnews()[:10]
	for i in lis:
		news='\nDESCRIPTION:- '+i[0]+'\nLINK TO READ MORE :- '+i[1]
		bot.send_message(chat_id=update.message.chat_id,text=news)
	txt="For more info on this , Kindly Visit This site - https://timesofindia.indiatimes.com/times-fact-check"
	bot.send_message(chat_id=update.message.chat_id,text=txt)



def about(bot,update):
	msg=""":PROBLEM STATEMENT:
	As the Coronavirus pandemic spreads,people all over the globe are turning to find trusted health information and advice.
Our bot has been designed to answer questions from the public about Coronavirus, 
and to give prompt, reliable and official information 24 hours a day, worldwide. 
Social media and news channels are the primary outlets through which people get to know about the virus.
However, it is often difficult to find answers to specific doubts that may persist within a context applicable to them. 
Moreover, people tend to mass-forward messages they receive without verifying the contents, often leading to false or incorrect information being spread.
Thus it also provide us Reality Check of the news.This will also serve government decision-makers by providing the latest numbers and situation reports.

	"""
	bot.send_message(chat_id=update.message.chat_id,text=msg)



bot=Bot(TOKEN)
try:
	bot.set_webhook("XXXXXXXXXXX/"+TOKEN)
except Exception as e:
	print(e)
dp=Dispatcher(bot,None)
dp.add_handler(CommandHandler("about",about))
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("helpline",_help))#
dp.add_handler(CommandHandler("help",need_help))#
dp.add_handler(CommandHandler("selectstate",statewise))
dp.add_handler(CommandHandler("selectcity",SelectCity))
dp.add_handler(CommandHandler("faq",FAQ))
dp.add_handler(CommandHandler("latestnews",getnews))#
dp.add_handler(CommandHandler("hindifakenewscheck",hindifakenews))#
dp.add_handler(CommandHandler("englishfakenewscheck",englishfakenews))#
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.photo,pic))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_handler(MessageHandler(Filters.contact, contact_callback))
#dp.add_handler(MessageHandler(Filters.location, location_callback))


if __name__=='__main__':
	app.run(port=8443)

