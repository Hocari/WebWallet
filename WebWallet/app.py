from flask import Flask, request, render_template, redirect, session
import sqlite3
import hashlib
from words import words
import uuid

conn = sqlite3.connect("wallet.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, address TEXT)")

#conn = sqlite3.connect('/Users/briac/Documents/GitHub/Hocari-Network/blockchain.db')
#c = conn.cursor()

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    seed = request.form['seed']
    addr = generate_wallet_address(seed)
    shortaddr = addr[0:2] + ".." + addr[-4:]


    
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()
    
    c.execute("SELECT username FROM users WHERE address=?", (addr,))
    result = c.fetchone()

    
    if result:
        username = result[0]
        session['seed'] = seed
        return render_template('landing.html', address=addr, short_address=shortaddr, username=username)
    else:
        return 'Invalid Login'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        seed_phrase = request.form.get('seed_phrase')
        address = generate_wallet_address(seed_phrase)
        return render_template('signin.html', address=address)
    return render_template('signin.html')


@app.route("/create_wallet", methods=["GET", "POST"])
def create_wallet():
    if request.method == "POST":
        username = request.form.get('username')
        username = str("@" + str(username))

        # Connect to the database
        conn = sqlite3.connect("wallet.db")
        c = conn.cursor()

        # Check if the username already exists in the database
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result:
            conn.close()
            return "This username already exists, please choose another one."

        # Create a new account and store the information in the database
        seed_phrase, address = create_account()
        print(address.split())

        c.execute("INSERT INTO users (username, address) VALUES (?, ?)", (username, seed_phrase))
        conn.commit()
        conn.close()

        return render_template("create_wallet.html", seed_phrase=seed_phrase, wallet_address=address, username=username)

    return render_template("create_wallet.html")




import random



def generate_seed_phrase():
    seed = ' '.join(random.choices(words, k=8))
    print(seed)
    return seed

def generate_wallet_address(seed_phrase):
    # You can use a hash function (such as sha256) to generate a unique identifier from the seed phrase
    import hashlib
    hash = hashlib.sha256(seed_phrase.encode())
    address = 'Hx' + hash.hexdigest()[:40]
    return address

def create_account():
    seed_phrase = generate_seed_phrase()
    address = generate_wallet_address(seed_phrase)
    print(address)
    return address, seed_phrase
    





if __name__ == "__main__":
    app.run(debug=True)
