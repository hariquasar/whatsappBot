from flask import Flask, request
import setting
import services

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def welcome():
    return 'try this again'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == setting.token and challenge != None:
            return challenge
        else: return 'token incorrect', 403
    except Exception as e:
        return e, 403
    
@app.route('/webhook', methods=['POST'])
def recevied_message():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.received_message_whatsapp(message)

        services.administrator_chatbot(text, number, messageId, name)

        # if text == 'hello':
        return "message sent"


    except Exception as e:
        return f'message not sent problem 1\n{e}', 403


if __name__ == '__main__':
    app.run()