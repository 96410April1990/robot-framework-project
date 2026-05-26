import requests
import json
import asyncio
import websockets
import ssl
import time

def retrieve_kafka_lenses_data(userId, password, user_id_val):
    return asyncio.run(get_kafka_lenses_data(userId, password, user_id_val))

async def get_kafka_lenses_data(userId, password, user_id_val):
    #API endpoints
    lensesLoginUrl = ''
    lensesQueryExecuteUrl = ''
    #Declare the headers
    headers = {'Content-Type': 'application/json'}
    #Request payloads 
    dataOne = {"user": userId, "password": password}
    #Execute the first API call
    responseOne = requests.post(lensesLoginUrl, headers=headers, data=json.dumps(dataOne), verify=False)
    if responseOne.status_code == 200:
        print("Login successful")
        getResponse = responseOne.content
        getResponse = getResponse.decode('utf-8')
        dataTwo = {"token": getResponse, "stats": 2, "sql": "USE `kafka`; SELECT * FROM CMS_WMT_consent_audit_data_qa WHERE user.id_value = '"+user_id_val+"' LIMIT 100;", "live": False}
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        #Execute the websocket call
        async with websockets.connect(lensesQueryExecuteUrl, ssl=ssl_context) as websocket:
            while True:
                await websocket.send(json.dumps(dataTwo))
                time.sleep(5)
                responseTwo = await websocket.recv()
                print(responseTwo)
                if "ccr_id" in responseTwo:
                    print(f"Received: {responseTwo}")
                    responseJson = json.loads(responseTwo)
                    ccr_id = responseJson['data']['value']['ccr_id']
                    return str(ccr_id)
                else:
                    print('The ccr_id is not available in the response payload. Please try again.')
                    time.sleep(10)
    else:
        print("Login failed. Please try again.")