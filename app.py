from flask import Flask, render_template, request, redirect, url_for, make_response
import base64

app = Flask(__name__)

USER_CREDENTIALS = {'user': 'password', 'admin': 'admin_password'}

def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def decode_base64(encoded_text):
    return base64.b64decode(encoded_text).decode()

# Dictionary to store comments for each user
user_comments = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        encoded_username = encode_base64(username)
        response = make_response(redirect(url_for('user_page')))
        response.set_cookie('username', encoded_username)
        return response
    else:
        return 'Invalid credentials'

@app.route('/user', methods=['GET', 'POST'])
def user_page():
    encoded_username = request.cookies.get('username')
    username = decode_base64(encoded_username) if encoded_username else None

    if username:
        if request.method == 'POST':
            # Process the comment data
            comment = request.form.get('comment', '')
            
            # Store the comment in the dictionary
            if username in user_comments:
                user_comments[username].append(comment)
            else:
                user_comments[username] = [comment]

        # Render the user page with all comments for the user
        return render_template('user_page.html', username=username, comments=user_comments.get(username, []))
    else:
        return 'Access denied. Please log in.'

@app.route('/admin')
def admin_page():
    encoded_username = request.cookies.get('username')
    username = decode_base64(encoded_username) if encoded_username else None

    if username == 'admin':
        return 'Welcome, admin! Here is the flag: DJSISACA{S3ss10n_H1j@cked!}'
    else:
        return 'Access denied. You are not the admin.'

if __name__ == '__main__':
    app.run(debug=True)