import requests
import setting
import json

def received_message_whatsapp(message):
    if 'type' not in message:
        text = 'message is not recognize'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['body']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']
    else:
        text = 'message is not recognize error 401'
    return text

def sent_message_whatsapp(data):
    try:
        whatsapp_token = setting.whatsapp_token
        whatsapp_url = setting.whatsapp_url
        headers ={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + whatsapp_token
        }
        print("sent ok!", data)
        response = requests.post(whatsapp_url,
                                 headers=headers,
                                 data=data)
        if requests.status_codes == 200:
            return 'message sent', 200
        else: return "error message not sent problem 2", requests.status_codes
    except Exception as e:
        return f'message not sent problem 3\n{e}', 403

def text_Message(number,text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append({
            "type" : "reply",
            "reply":{
                "id": sedd + "_btn_" + str(i+1),
                "title": option
            }
        })

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append({
            "if" : sedd + "_row_" + str(i+1),
            "title": option,
            "description": ""
        })

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "see options",
                    "sections": [
                        {
                            "title": "sections",
                            "rows": rows
                        },
                    ]
                }
            }
        }
    )
    return data

def replyRection_message(number, messageId, emoji):
    data = json.dumps({
        "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction" :{
                "message_id": messageId,
                "emoji": emoji
            }
    })

def replyText_message(number, messageId, text):
    data = json.dumps({
        "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            "type": "text",
            "text" :{
                "body":text
            }
    })


def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrator_chatbot(text,number,messageId, name):
    text = text
    list = []

    markRead = markRead_Message(messageId)
    list.append(markRead)

    if "hi" in text:
        # body = "你好! 我是一個chatbot"
        # footer = "power by harry"
        # options = ["有問題?", "要搵專人?", "web", "Booking"]
        # replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        # list.append(replyButtonData)
        body = "你好! 我是一個chatbot"
        footer = "power by harry"
        options = ["要搵專人?", "web", "Booking"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2", messageId)
        list.append(replyButtonData)
    elif "web" in text:
        body = "以下是你想要的網頁"
        footer = "power by harry"
        options = ["Google", "YouTube"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2", messageId)
        list.append(replyButtonData)
    elif "Google" in text:
        textMessage = text_Message(number, "這是你想要的網頁")
        body = "www.google.com"
        footer = "power by harry"
        options = ["麻煩曬"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)
    elif "YouTube" in text:
        textMessage = text_Message(number, "這是你想要的網頁")
        sent_message_whatsapp(text_Message)
        body = "www.youtube.com"
        footer = "power by harry"
        options = ["麻煩曬"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4", messageId)
        list.append(replyButtonData)
    elif "booking" in text:
        body = "你想約咩星期幾?"
        footer = "power by harry"
        options = ["📅 星期一","📅 星期三","📅 星期五", "麻煩曬"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed5", messageId)
        list.append(replyButtonData)
    elif "麻煩曬" in text:
        textMessage = text_Message(number, "好，咁我走先")
        list.append(textMessage)
    else:
        data = text_Message(number, "我唔係好明你講咩")
        list.append(data)
    
    for item in list:
        sent_message_whatsapp(item)
