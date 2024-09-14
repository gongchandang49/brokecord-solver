import os
import time

def imports():
    import flask # known issues if not imported
    from flask import Flask, request, jsonify
    from g4f.client import Client
    from flask_cors import CORS
    import pygetwindow as gw
    import time
    import keyboard
    

try:
    os.system("pip install flask g4f flask_cors pygetwindow keyboard")
    os.system("cls")
    imports()
except:
    raise
finally: # win32 is so troublesome...
    try:
        os.system("pip install win32")
        os.system("cls")
        import win32api
    except:
        try:
            os.system("pip install pywin32")
            os.system("cls")
            import win32api
        except:
            try:
                os.system("pip install pypiwin32")
                os.system("cls")
                import win32api
            except:
                pass


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
        print(e)
        return jsonify({'error': str(e)}), 500

    return jsonify({'answer': answer})


@app.route('/type', methods=['POST'])
def type():
    
    data = request.json
    fixedString = data.get('fixedString', '')
    
    try:
        
        def send_text(text):
            time.sleep(3)
            keyboard.write(text, delay=0.1)
            time.sleep(0.3)
            keyboard.press_and_release('enter')
            time.sleep(0.3)



        def get_chrome_window():
            
            chrome_windows = [window for window in gw.getAllTitles() if "discord" or "chrome" in window.lower()]
                            # you can replace "chrome" with brave/edge/opera/chromium/etc
            if chrome_windows:
                chrome_window_title = chrome_windows[0]
                print(f"Found Chrome window: {chrome_window_title}")
                hwnd = win32gui.FindWindow(None, chrome_window_title)
                if hwnd:
                    # Disabled these options because they were giving errors, try at your own risk
                    #win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore the window if minimized
                    #win32gui.SetForegroundWindow(hwnd)  # Activate the window
                    return True
                else:
                    print("Failed to find window handle.")
                    return False
            else:
                print("Chrome window not found")
                return False
        
        get_chrome_window()
        send_text(fixedString)
        return jsonify({'Answer typed': fixedString})
    
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
