 # -*- coding: utf-8 -*-
from __future__ import print_function
import urllib

link = "https://api.thingspeak.com/channels/715296/feeds/last.json"
link2 = "https://api.thingspeak.com/channels/715322/feeds/last.json"
link3="https://api.thingspeak.com/channels/716958/feeds/last.json"
link5="https://api.thingspeak.com/channels/721259/feeds/last.json"

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session']) 
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    link1= "https://api.thingspeak.com/channels/715296/feeds.json?api_key=WTIBFRVXST20KJRH&results=2"
    if intent_name =="status":
        return read_data(intent, session, link,link2)
    elif intent_name == "healthtips":
        return get_tips(intent, session)
    elif intent_name =="checkdoctor":
        return get_doctorlist(intent, session)
    elif intent_name =="confirm":
        return get_confirmation(intent, session,link5)
    elif intent_name == "report":
        return get_report(intent, session,link3)
    elif intent_name == "skintips":
        return get_skintips(intent, session,link2)
    elif intent_name == "DoctorAppointment":
        return set_doctor(intent, session)
    elif intent_name == "food":
        return get_food(intent, session,link2)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome ." \
                    "Here are Some options." \
                    "Just ask me to tell whats is my health status."\
                    "Or ask me for health tips."
    reprompt_text = "try again"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank You. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# Run the read data
def read_data(intent, session,link,link2):
    session_attributes = {}
    reprompt_text = None
    should_end_session = False
    f = urllib.urlopen(link) # Get your data
    a = f.read()
    sys=a.split('"')[9]
    dia=a.split('"')[13]
    pulse=a.split('"')[17]
    f = urllib.urlopen(link2) # Get your data
    a = f.read()
    weight=a.split('"')[9]
    height=a.split('"')[13]
    skin=a.split('"')[17]
    dummy1=weight
    dummy2=height
    dummy1=float(dummy1)
    dummy2=float(dummy2)
    bmi =dummy1/(dummy2*dummy2)
    bmi=round(bmi)
    print(bmi)
    if pulse > 60:
        comment = " That sounds good."
    elif pulse > 30:
        comment = " It seems somewhat lacking to me."
    elif pulse > 10:
        comment = " Wow, that stinks!"
    elif pulse < 11 :
        comment = " That's terrible!"
    if bmi <= 18:
        comment +="  and Your BMI is"+str(bmi)+" which means you are underweight."
    elif bmi > 18 and bmi < 25:
        comment +=" and Your BMI is "+str(bmi)+" which means you are normal."
    elif bmi >= 25 and bmi < 30:
        comment +="and  your BMI is "+str(bmi)+" which means overweight."
    elif bmi >= 30:
        comment +="and  Your BMI is "+str(bmi)+" which means you are obese."
    speech_output = " your bp status was "+str(sys)+"/"+str(dia)+",your skin type is "+skin+" ,Your Pulse was " +str(pulse)+" ticks per second"
    speech_output +=comment
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Run the read data


def get_tips(intent, session):
  
    import random
    session_attributes = {}
    card_title = "Welcome"
    dummy=["Whole eggs are so nutritious that they're often referred to as nature's multivitamin.","Instead of going on a diet, try adopting a healthier lifestyle. Focus on nourishing your body, instead of depriving it.","Lifting weights leads to massive improvements in metabolic health, including improved insulin sensitivity ","Lifting weights is one of the best things you can do to strengthen your body and improve your body composition.","olive oil is loaded with heart-healthy monounsaturated fats and powerful antioxidants that can fight inflammation","Extra virgin olive oil is the healthiest fat on the planet.","Eating plenty of protein has also been shown to lower blood sugar and blood pressure levels ","A high protein intake can boost metabolism significantly, while making you feel so full that you automatically eat fewer calories. It can also cut cravings and reduce the desire for late-night snacking","Protein is particularly important for weight loss, and works via several different mechanisms ","Eating enough protein is incredibly important, and many experts believe that the recommended daily intake is too low.","Vegetables are loaded with prebiotic fiber, vitamins, minerals and all sorts of antioxidants, some of which have potent biological effects.","Meat can be a nutritious and healthy part of the diet. It is very high in protein, and contains various important nutrients.","Coffee has been unfairly demonized. The truth is that it's actually very healthy.","All the processed junk foods in the diet are the biggest reason the world is fatter and sicker than ever before.","Aim to drink around 4-5 litres a day to keep your body hydrated all the time." ,"Avoid eating when distracted, eat slowly, take your time and do not over-eat. " ,"Getting into bed by 10 pm or 10:30 pm ensures you get enough sleep which also benefits you in the long run.","Avoid any kind of addiction like drug, alcohol or tobacco for a healthy and disease-free life."]

    speech_output = str(random.choice(dummy))
   
    reprompt_text = "I Didnt get yoy Please tell again" 
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def get_doctorlist(intent, session):
  
    session_attributes = {}
    card_title = "Welcome"
    reprompt_text = "" 
    should_end_session = False
    speech_output="list of avalibale doctorts are"
    speech_output+="Balaji,"
    speech_output+="Ravi Shanker Reddy,"
    speech_output+="Chandrashekar Reddy,"
    speech_output+="Nageshwaraiah,"
    speech_output+=" Ashok Kumar Reddy, "
    speech_output+="surya"
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_skintips(intent, session,link2):
  
    import random
    session_attributes = {}
    reprompt_text = None
    should_end_session = False
    f = urllib.urlopen(link2) # Get your data
    a = f.read()
    skin=a.split('"')[17]
    comment=""
    speech_output=""
    if(str(skin)=="DrySkin" or str(skin)=="Dry Skin"):
        dummy=["If dry skin is on another area of the body, applying aloe vera gel liberally and allowing it to soak in may achieve a similar effect.","Aloe vera gel may help provide relief from dry skin","Coconut oil improves skin hydration and increase the number of lipids fats on the surface of the skin."]
        comment =str(random.choice(dummy))
    elif(str(skin)=="NormalSkin"):
        dummy=["Make a paste of gram flour with milk. Rub this paste gently onto your face then let it sit there for fifteen minutes. Wash it off with clean water. This will make your skin soft. Another ancient time natural beauty tip for normal skin.","squeeze out juice from one grated fresh potato. Mix it with little quantity of lemon juice. Pour a small quantity of this mix on a clean piece of cotton and apply on your face. Let it be there for five to ten minutes and wash it off.","Use a mild, oil based moisturizer under your make up to retain normal moisture","Apply a thin film of home-made moisturizer at night to keep your skin’s normal moisture"]
        comment=str(random.choice(dummy))
    elif(str(skin)=="OilySkin"):
        dummy=["Rub slices of cucumber on your face before hitting the sack.Let it sit overnight before using warm water to wash it off","Grate an apple and apply its shreds on your face. Leave on for 10-15 minutes prior to a lukewarm water rinse.","After cutting a tomato in half, simply give your face a good rub with it ina circular motion. Let the residue sit for 10-15 minutes before using cold water to rinse it off.","Mix 1 tablespoon each of honey and yogurt and to this blend add oatmeal. Give your face a good application with this mixture for 5-10 minutes before using warm water to rinse it off.","In 2 tablespoon of water mix 1 tablespoon of lime juice. Now, apply this on your face and let it dry for 5-10 minutes before using warm water to wash it off.","Apply one whipped egg white on your faceleave it on for 10-15 minutes before washing it with warm water.","you should wash your face twice a day, but donot overdo it."]
        comment=str(random.choice(dummy))
    elif(str(skin)=="SensitiveSkin"):
        dummy=["Keep Track Of Your Allergens. Allergy and sensitive skin are arch rivals","Amla or Indian gooseberry is a rich source of vitamin C. Clean, steam, and eat one amla a day to give your skin that extra dose of nourishment. ","Water is essential to keep your skin hydrated and moisturized from within. It also helps in flushing out the toxins."]
        comment=str(random.choice(dummy))
    elif(str(skin)=="CombinationSkin"):
        dummy=[" applying aloe vera gel liberally and allowing it to soak in may achieve a similar effect.","Rub slices of cucumber on your face before hitting the sack.Let it sit overnight before using warm water to wash it off","Grate an apple and apply its shreds on your face. Leave on for 10-15 minutes prior to a lukewarm water rinse.","Keep Track Of Your Allergens. Allergy and sensitive skin are arch rivals","Amla or Indian gooseberry is a rich source of vitamin C. Clean, steam, and eat one amla a day to give your skin that extra dose of nourishment. ","Water is essential to keep your skin hydrated and moisturized from within. It also helps in flushing out the toxins."]
        comment=str(random.choice(dummy))
    #speech_output +=comment
    speech_output+=" Since your skin type is "+skin+" try out the following "+comment
    reprompt_text=""
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def get_food(intent, session,link2):
  
    import random
    session_attributes = {}
    reprompt_text = None
    should_end_session = False
    f = urllib.urlopen(link2) # Get your data
    a = f.read()
    weight=a.split('"')[9]
    height=a.split('"')[13]
    dummy1=weight
    dummy2=height
    dummy1=float(dummy1)
    dummy2=float(dummy2)
    bmi =dummy1/(dummy2*dummy2)
    bmi=round(bmi)
    comment=""
    if bmi <= 18.5:
       dummy=["Add extras to your dishes for more calories — such as cheese in casseroles and scrambled eggs, and fat-free dried milk in soups and stews.","Exercise, especially strength training, can help you gain weight by building up your muscles. Exercise may also stimulate your appetite.","As part of an overall healthy diet, choose whole-grain breads, pastas and cereals; fruits and vegetables; dairy products; lean protein sources; and nuts and seeds."]
       comment="since you are underweight follow the recommendations "+str(random.choice(dummy))

    elif bmi > 18.5 and bmi < 25:
       dummy=["Limits saturated and trans fats, sodium, and added sugars","Includes lean meats, poultry, fish, beans, eggs, and nuts in your diet ","Emphasizes vegetables, fruits, whole grains, and fat-free or low-fat dairy products."]
       comment="since you are normal,good u may follow the below tip to stay fit "+str(random.choice(dummy))

    elif bmi >=25 and bmi < 30:
        dummy=[" Restricting calories does not guide you what to eat, but it is important that you eat a balanced diet that includes foods like whole grains, vegetable, fruits, lean meat, low fat dairy products and limit saturated fats, salt.","The most successful dieters take a grazing approach to weight loss. Rather than cut out meals, a more effective approach is to spread out the calories into about five meals per day. Three small meals with two healthy snacks would be the norm. "]
        comment=" since you are  overweight follow the recommendations "+str(random.choice(dummy))

    elif bmi >= 30:
         dummy=["Make opportunities during the day for even just 10 or 15 minutes of some calorie-burning activity, such as walking around the block or up and down a few flights of stairs at work. Again, every little bit helps. ","Choose whole grain foods such as brown rice and whole wheat bread. Avoid highly processed foods made with refined white sugar, flour and saturated fat.","Eat five to six servings of fruits and vegetables daily. A vegetable serving is one cup of raw vegetables or one-half cup of cooked vegetables or vegetable juice. A fruit serving is one piece of small to medium fresh fruit, one-half cup of canned or fresh fruit or fruit juice, or one-fourth cup of dried fruit."]
         comment="since you are obese, your strictly recommended to follow this "+str(random.choice(dummy))
    
    
   
    speech_output =comment
    reprompt_text=""
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



def get_report(intent, session, link3):
    session_attributes = {}
    reprompt_text = None
    should_end_session = False
    f = urllib.urlopen(link3) # Get your data
    a = f.read()
    report=a.split('"')[9]
   
    
    
    speech_output = " your report status  "+report
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def set_doctor(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    print(intent['slots'])
    if "Balaji" == intent['slots']['doct']['value']:
        slotStatus="YOUR appointment will be confirmed from Dr.Balaji soon"
    
    elif "Ravi shanker reddy" == intent['slots']['doct']['value']:
        slotStatus="YOUR appointment will be confirmed from Dr.Ravi shanker reddy soon"
    elif "Chandrasekhar reddy" == intent['slots']['doct']['value']:
        slotStatus="YOUR appointment will be confirmed from Dr.Chandrasekhar reddy soon"
    elif "Ashok Kumar reddy" == intent['slots']['doct']['value']:
        slotStatus="YOUR appointment will be confirmed from Dr.Ashok Kumar reddy soon"
    elif "Surya" == intent['slots']['doct']['value']:
        slotStatus="YOUR appointment will be confirmed from Dr.Surya soon"
    elif "nageshwaraiah" == intent['slots']['doct']['value']:
        slotStatus="YOUR appointment will be confirmed from Dr.nageshwaraiah soon"
    else:
        slotStatus="Sorry I cant confirm your Appointment"
    speech_output = slotStatus
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_confirmation(intent, session, link5):
    session_attributes = {}
    reprompt_text = None
    should_end_session = False
    f = urllib.urlopen(link5) # Get your data
    a = f.read()
    date=a.split('"')[9]
    #dt=date[0:1]
    #mt=date[1:6]
    #yr=date[6:]
    time=a.split('"')[13]
    hr=time[0:2]
    mn=time[2:4]
    status=a.split('"')[17]

    speech_output = "Your appointment is "+status+" on "+date+ " at  "+hr+":"+mn
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
