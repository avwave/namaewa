- Make sure you have virtualenv installed. (i.e. "sudo pip install virtualenv")
- Activate your virtualenv by running "source venv/bin/activate"
- Install requirements by running "pip install -r requirements.txt"

# To run the script standalone
- Run 'python NameExtract.py <email@thebestveb.com>'

# To run the server
- Make sure you enter your SECRET_KEY in server.py (line 17).
  - If you're unsure how to generate your SECRET_KEY, then start the Python shell.
    - import os
    - os.urandom(24)
    - '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    - Just take that result and copy/paste it into SECRET_KEY and you’re done.

- Now run the server like 'python server.py'
