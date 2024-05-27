import os
import time

try:
    from flask import Flask, request, jsonify
    from g4f.client import Client
    from flask_cors import CORS
    import subprocess
    import Quartz
except:
    try:
        os.system("pip3 install flask g4f flask_cors pyobjc-framework-Quartz")
    except:
        os.system("python3 -m pip install flask g4f flask_cors pyobjc-framework-Quartz")
    os.system("clear")
finally:
    from flask import Flask, request, jsonify
    from g4f.client import Client
    from flask_cors import CORS
    import subprocess
    import Quartz


app = Flask(__name__)
CORS(app, origins='*', allow_headers='*')
client = Client()

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    fulltask = data.get('fulltask', '')

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"I will next provide you with a question in a language. Strictly follow its instructions for replying. Do NOT reply with elaborate answers or things not requested. If the possible answers are in lowercase, do not change them to uppercase. Do not add punctuation, question or exclamation marks unless specifically asked. Reply in the SAME language as the question (Spanish) with short answers, no punctuation. Here is the question: {fulltask}"}]
        )
        answer = response.choices[0].message.content
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'answer': answer})


@app.route('/type', methods=['POST'])
def type():
    
    data = request.json
    fixedString = data.get('fixedString', '')
    
    try:
        
        def get_chrome_window():
            result = subprocess.run(['osascript', '-e', 'tell app "System Events" to get name of every process whose background only is false'], stdout=subprocess.PIPE)
            running_apps = result.stdout.decode('utf-8').split(', ')
            
            for app_name in running_apps:
                if "Chrome" in app_name:
                    return app_name
            
            return None

        def send_text(text):
            event = Quartz.CGEventCreateKeyboardEvent(None, 0, True)
            Quartz.CGEventKeyboardSetUnicodeString(event, len(text), text)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            time.sleep(0.3)
            
            enter_down = Quartz.CGEventCreateKeyboardEvent(None, 36, True)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, enter_down)
            time.sleep(0.3)

            enter_up = Quartz.CGEventCreateKeyboardEvent(None, 36, False)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, enter_up)
            time.sleep(0.3)


        chrome_window_name = get_chrome_window()

        if chrome_window_name:
            print("Found Chrome window:", chrome_window_name)
            subprocess.run(['osascript', '-e', f'tell application "{chrome_window_name}" to activate'])
            send_text(fixedString)
        else:
            print("Chrome window not found.")

        return jsonify({'Answer typed': fixedString})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
