This is QR scanner of XXX event, which is a traditional festival in Lam Son High School, Vietnam.
To use, ensure that you already installed packages required in requirements.txt.

# Setting up
1, Have python installed from https://python.org and added to path.
2, Download ngrok at https://ngrok.com/download and sign up a new account. Then, add ngrok to path (If you do not know how to add ngrok to path, it is in the end of this document). Open ngrok and type "ngrok config add-authtoken <token>" 
3, Open the folder where this project is located. Open a terminal (cmd/ Windows PS) and type "pip install -r requirements.txt", after installation finished, close the terminal.

# From this step, no need to repeat the above steps 
4, Open a terminal (same folder as the project) and type "ngrok http 5500"
5, Open another terminal, type "py app.py"
6, In your device, open the link provided by ngrok and free to use the scanner !!!


# Notion: Add ngrok (as well as every other application to path)
1, Copy the absolute path to the folder where you install ngrok (other apps) just by clicking on the address bar.
2, In windows seach bar (Windows + S), search and click on "Edit the system environment variables"
3, Find and click on "Environment variables"
4, In "System variables", double click on "Path", choose "New" and paste and copied path.
5, Click "OK", "OK" and "OK"
