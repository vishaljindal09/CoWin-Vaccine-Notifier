# -*- coding: utf-8 -*-
"""
Created on Sat May 15 14:40:46 2021

@author: visha
"""

import requests

from datetime import datetime, timedelta
#
def telegram_bot_send_text(bot_message):
            bot_token = 'api'
            bot_chat_id = 'group id starts with -ve sign'
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message
            
            print(send_text)
        
            response = requests.get(send_text)
        
            return response.json()
        


age = 55
pinCodes = ["110085"]
num_days = 2

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0   

    for pinCode in pinCodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pinCode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            
            result = requests.get( URL, headers=header )
            # print('-------------------------------------------------------------')
            # print(result.text)
            # print('-------------------------------------------------------------')

            if result.ok:
                response_json = result.json()
                
                #print(response_json)

                flag = False
                if response_json["centers"]:            
                    if(print_flag.lower() =='y'):

                        for center in response_json["centers"]:
                            # print('-------------------------------------------------------------')
                            # print(center)
                            # print('-------------------------------------------------------------')

                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    message = 'Pincode: ' + pinCode
                                    message = message + "\nAvailable on:" + str(session["date"])
                                    message = message + "\nSite: " + str(center["name"])
                                    #print("\t", center["block_name"])
                                    #print("\t Price: ", center["fee_type"])
                                    message =message +"\nAvailablity : "+str(session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        
                                        response_telegram = telegram_bot_send_text(message)

                                    counter = counter + 1
                                else:
                                    pass                                    
                else:
                    pass        
                          
            else:
                print("No Response!")

                
    if(counter == 0):
        print("No Vaccination slot avaliable!")
    else:
        print("Search Completed!")
