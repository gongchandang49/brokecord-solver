<img width="400" alt="brokecord" src="https://github.com/gongchandang49/brokecord-solver/assets/170948611/4256b138-ebbe-40dd-89ea-299ea2feceef">

# BrokeCord - free hCaptcha solver

*A free, single-threaded, self-hosted, browser-based hCaptcha solver that can run on any computer with low specs. It is NOT an API that you can integrate with DMDGO or similar tools: it needs a real browser to work.*

### ⚠️ HEADS UP: This is only a captcha solver for now. A specific mass DM tool will be released for it very soon. Right now, please test that it solves captchas correctly. If you are having issues, refer to the Tutorial video below and the Telegram support server.

## Requirements
- Windows/Mac with lastest Python version installed.
- Any Chromium-based browser (Chrome, Edge, Brave, Opera...)
  * **Note**: Does not work on Firefox, Chromium or Chromedriver.

## How to install
- Download and run the Python Flask server specific to your OS. *The window needs to be open (in the background) at all times. Otherwise it will not solve captchas.*
  - **Windows:** [server_win.py](src/server_win.py)    `py server_win.py`
  - **Mac:** [server_mac.py](src/server_mac.py)        `python3 server_mac.py`
- Download the [Tampermonkey extension](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo).
- Visit the extension options (chrome://extensions/?id=dhdgffkkebhmkfjojejmpbldmpobfkfo) and **enable it on incognito mode**.
- *Suggestion: do the same (install and incognito) for the [Discord Token Login](https://chromewebstore.google.com/detail/discord-token-login/ealjoeebhfijfimofmecjcjcigmadcai) extension (useful for logging into tokens quickly).*
- Open Tampermonkey dashboard, click "add new script [+]" and copy-paste the contents from [src/userscript.txt](src/userscript.txt).
- Click the userscript title and open the script settings,  add "127.0.0.1" to "User domain whitelist" under "XHR Security" as below:
![add-127001-to-user-domain-whitelist](https://github.com/gongchandang49/brokecord-solver/assets/170948611/c91318d7-4b72-4049-8b60-2242101fbdb1)

- Save the settings, close the tab and open up a Discord login tab on incognito.
- Log in your token using Discord Token Login (or otherwise), and let the fun begin!
- **Any captchas that you encounter when performing actions on the page will automatically be solved by BrokeCord.** You can view solver logs in the browser console (F12) and requests in the Python server window that you opened in step 1.

## Tutorial video


## Still having trouble? Join our Support server!
https://t.me/+LgjJ6Ym0_JU3NmM8
