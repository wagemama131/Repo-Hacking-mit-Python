from sqlalchemy.exc import SQLAlchemyError

from pinboard import app,db, SIMPLE_CAPTCHA
from flask import render_template, request, redirect, url_for, jsonify
from sqlalchemy import text
from datetime import datetime
import bcrypt, re, os, string

#password_salt = bcrypt.gensalt()
mapper = {"true": 1, "false": 0}
password_flag = Flag{Rekursive_Flag_Gefunden}

def filter_special_chars(s:str, special_chars: str) -> bool:
    for char in s:
        if char in special_chars:
            return True
    return False


@app.route('/')
def homepage():

    user = request.cookies.get('userID')
    cleaned_seller_name = ''

    if user:
        user_query = "Select seller_name from User where user_ID = :user;"
        ##print(user_query)
        result = db.session.execute(text(user_query), {'user': user})
        seller_name = result.fetchone()
        ##print(seller_name)

        if seller_name is None:   # Falsche UserIDs herauswerfen
            response = redirect('/')
            response.set_cookie('userID', '', expires=0)
            return response

        cleaned_seller_name = ''.join(re.sub(r"[\'\(\)\,]", "", str(x)) for x in seller_name) # angepasst für Union
        ##print(cleaned_seller_name)

    # Eigene Artikel aus Datenbank holen
    articles = []
    try:
        article_query = "Select article_ID, image_url, title, price from Artikel where user_ID = :user;"
        #print(article_query)
        result2 = db.session.execute(text(article_query), {'user': user})
        articles = result2.fetchall()
        #print(articles)
    except SQLAlchemyError as e:
        print(e)


    return render_template("homepage.html", userID=cleaned_seller_name, articles=articles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    ##print(request.form)
    if request.method == 'POST':

        # Details aus Form ziehen
        email = request.form.get('email').strip()
        seller_name = request.form.get('seller_name').strip()
        password = request.form.get('password').strip()
        password2 = request.form.get('confirm_password').strip()
        #print(email, seller_name, password, password2)

        #Details prüfen
        if len(email) < 3:
            return redirect('/register?error=Problem mit der Email!')

        if password != password2 or len(password) < 1:
            return redirect('/register?error=Problem mit den Passwörtern!')

        if len(seller_name) < 1 or len(seller_name) > 32 or filter_special_chars(seller_name, "!@#$%^&*()_+-=[]{}|;:'\",.<>?/\\`~"):
            return redirect('/register?error=Problem mit dem Nutzernamen!')

        email_query = "SELECT * FROM User WHERE email = :email"     # Ist Email schon registriert
        if db.session.execute(text(email_query),{'email': email}).fetchone() is not None:
            return redirect('/register?error=Email ist schon vorhanden!')

        #hashed_password = bcrypt.hashpw(b'password', password_salt)
        #hashed_password_string = hashed_password.decode('utf-8')
        registry_query = "Insert into User(user_ID, seller_name, email, password) VALUES (UUID(),:seller_name,:email,:password);" #{hashed_password_string}');"
        db.session.execute(text(registry_query), {'seller_name': seller_name, 'email': email, 'password': password})
        db.session.commit()

        return redirect("/login")
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        #Captcha checken
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if not SIMPLE_CAPTCHA.verify(c_text, c_hash):
            new_captcha_dict = SIMPLE_CAPTCHA.create()
            return_statement = '<script>alert("Captcha ist falsch");</script>'
            return render_template("login.html", captcha=new_captcha_dict, return_statement=return_statement)

        # Elemente verifizieren
        if len(email) < 3 or len(password) < 1:
            new_captcha_dict = SIMPLE_CAPTCHA.create()
            return render_template("login.html", captcha=new_captcha_dict)

        email_query = "SELECT user_ID FROM User WHERE email = :email and password = :password;"
        ##print(email_query)
        result = db.session.execute(text(email_query), {'email': email, 'password': password})
        user = result.fetchone()
        if not user:
            new_captcha_dict = SIMPLE_CAPTCHA.create()
            return render_template("login.html", captcha=new_captcha_dict)

        response = redirect('/')
        response.set_cookie('userID', user[0])
        return response

    new_captcha_dict = SIMPLE_CAPTCHA.create()
    return render_template("login.html", captcha=new_captcha_dict)

@app.route('/pinboard')
def pinboard():
    user = request.cookies.get('userID')
    mapping = {0: 'Nein', 1: 'Ja'}

    if user:
        user_query = "Select seller_name from User where user_ID = :user;"
        result = db.session.execute(text(user_query), {'user': user})
        seller_name = result.fetchone()
        #print(seller_name)

        if seller_name is None or len(seller_name) == 0:   # Falsche UserIDs herauswerfen
            response = redirect('/pinboard')
            response.set_cookie('userID', '', expires=0)
            return response

    articles = []
    article_query = "Select * From Artikel Inner Join User On Artikel.user_ID = User.user_ID ORDER BY RAND();"
    result = db.session.execute(text(article_query))
    articles = result.fetchall()
    #print(articles)
    return render_template("pinboard.html", userID=user, articles=articles, mapping=mapping)

@app.route('/logout')
def logout():
    response = redirect("/")
    response.set_cookie('userID', '', expires=0)
    return response

@app.route('/article/<article_id>', methods=['DELETE'])
def delete_article(article_id):

    user = request.cookies.get('userID')

    article_query = "DELETE FROM Artikel WHERE article_ID = :article_id and user_ID = :user;"
    result = db.session.execute(text(article_query), {'article_id': article_id, 'user': user})
    db.session.commit()

    if result.rowcount == 0:
        return jsonify({"message": "Datenbankfehler"}), 500

    return jsonify({"message": "OK"}), 200

@app.route('/add/article', methods=['POST'])
def add_article():

    ##print("IM in")
    user = request.cookies.get('userID')
    form = request.form
    image = request.files.get("image")
    image_url = ''

    title = form.get("title")
    price = float(form.get("price"))
    state = form.get("condition")
    location = form.get("location").strip()
    postalcode = form.get("postalcode").strip()
    phone_number = form.get("phone_number")
    description = form.get("description").strip()
    negotiable = form.get("negotiable")

    ##print("Im here")

    if image:
        filename = f"{user}_{image.filename}"
        save_path = f"{app.root_path}\\static\\uploads\\{filename}"
        ##print(save_path)
        image.save(save_path)
        image_url = f"../static/uploads/{filename}"
        ##print(image_url)

    # Überprüfungen
    if len(title) < 1:
        return jsonify({"message": "Titelfehler"}), 500

    if float(price) < 0:
        return jsonify({"message": "Preisfehler"}), 500

    if filter_special_chars(location, "!@#$%^&*()_+-=[]{}|;:'\",.<>?/\\`~0123456789") or len(location) < 1:
        return jsonify({"message": "Titelfehler"}), 500

    if len(postalcode) < 5 or filter_special_chars(postalcode, ("!@#$%^&*()_+-=[]{}|;:'\",.<>?/\\`~"+string.ascii_letters)):
        return jsonify({"message": "Postleitzahlfehler"}), 500

    if len(phone_number) < 4 or filter_special_chars(phone_number, ("!@#$%^&*()_+-=[]{}|;:'\",.<>?/\\`~"+string.ascii_letters)):
        return jsonify({"message": "Telefonfehler"}), 500

    if len(description) < 1:
        return jsonify({"message": "Beschreibungsfehler"}), 500

    # Datenbank befüllen
    add_query = "Insert into Artikel(user_ID, title, price, state, location, postalcode, description,negotiable, image_url, phone_number) values (:user, :title,:price,:state,:location,:postalcode,:description,:negotiable,:image_url,:phone_number);"

    db.session.execute(text(add_query), {'user': user, 'title': title, 'price': price, 'state': state, 'location': location, 'postalcode': postalcode, 'description': description, 'negotiable': mapper[negotiable], 'image_url': image_url, 'phone_number': phone_number})
    db.session.commit()

    user_query = "Select email From User where user_ID = :user;"
    result = db.session.execute(text(user_query), {'user': user})
    user_details = result.fetchone()


    return jsonify({
        "title": title,
        "price": price,
        "negotiable": negotiable,
        "condition": state,
        "location": location,
        "postalcode": postalcode,
        "description": description,
        "phone_number": phone_number,
        "email": user_details[0],
        "image_url": image_url,
        "created_at": "Gerade eben"
    })

