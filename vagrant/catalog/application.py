from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc, update
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# Pulls all categories and latest items from DB and display using index.html
@app.route('/')
@app.route('/catalog')
def showCatalogs():
    categories = session.query(Category).all()
    latestItems = session.query(Item).order_by(Item.date_added.desc()).limit(6).all()
    itemsL = []
    categoryList = []

    for c in categories:
        categoryList.append(c.name)

    for i in latestItems:
        itemsL.append(i.name)

    return render_template('index.html', categories=categoryList, items=itemsL)


# Pulls all items in a specific category and display them using categories.html
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    categories = session.query(Category).all()
    categoryList = []
    for c in categories:
        categoryList.append(c.name)

    catId = session.query(Category).filter_by(name=category_name).one()
    print catId.id
    catItems = session.query(Item).filter_by(cat_id=catId.id).all()
    itemsL = []
    count = 0

    for i in catItems:
        itemsL.append(i.name)
        count += 1

    header = category_name+' Items '+'( '+str(count)+' items)'
    return render_template('categories.html', categories=categoryList, items=itemsL, header=header)


# Pulls item information and alows you to edit using edit_Item.html
@app.route('/catalog/<string:category_name>/<string:item_name>')
def itemInformation(category_name, item_name):

    catId = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(cat_id=catId.id, name=item_name).one()
    description = 'Description: ' + item.description
    return render_template('item_information.html', item=item.name, description=description, category=catId.name)


# Pulls item information and alows you to edit using edit_Item.html
@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if username not in login_session:
        flash("You need to login")
        return render_template('login.html')
    else:
        catId = session.query(Category).filter_by(name=category_name).one()
        editItem = session.query(Item).filter_by(cat_id=catId.id, name=item_name).one()
        if request.method == 'POST':
            print "zzzzzzzzzzzzzzzz"
            if request.form['edit'] == "submit":
                print editItem.description
                updateItem = session.query(Item).filter_by(cat_id=catId.id, name=item_name).one()
                print "asdawer"
                updateItem.name = request.form['title']
                updateItem.description = request.form['description']
                session.commit()
                print updateItem.description
                print "asdaweruuuuuu"
                flash("Item change was made")
                return render_template('item_information.html', category_name=category_name, item_name=item_name, description=editItem.description)
        else:
            print "notpe"
            return render_template('edit_Item.html', category_name=category_name, item_name=item_name, item=editItem)


@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
    if username not in login_session:
        flash("You need to login")
        return render_template('login.html')
    else:
        categories = session.query(Category).all()
        categoryList = []
        for c in categories:
            categoryList.append(c.name)

        if request.method == 'POST':
            print "zzzzzzzzzzzzzzzz"
            if request.form['edit'] == "submit":
                print request.form['category']
                catId = session.query(Category).filter_by(name=request.form['category']).one()
                print "2"
                item = Item(name=request.form['name'], description=request.form['description'], cat_id=catId.id)
                print "zcc"
                session.add(item)
                session.commit()
                flash("Item change was added")
                return redirect('/catalog')
        else:
            print "notpe"
            return render_template('addItem.html', categories=categoryList)


# Delete an item using delete_item.html
@app.route('/catalog/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    catId = session.query(Category).filter_by(name=category_name).one()
    itemDelete = session.query(Item).filter_by(cat_id=catId.id, name=item_name).one()
    if request.method == 'POST':
        if request.form['delete'] == "delete":
            session.delete(itemDelete)
            session.commit()
            flash("Item deleted")
            return redirect(url_for('showItems', category_name=category_name))
        if request.form['cancel'] == "cancel":

            redirect('/catalog')
    else:
        return render_template('delete_Item.html', item=itemDelete)


# creating JSON endpoints
@app.route('/catalog/JSON')
def showCatalogJSON():
    category = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in category])


@app.route('/catalog/<int:category_id>/items/JSON')
def showItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(cat_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# Create anti-forgery state token
@app.route('/login', methods=['GET', 'POST'])
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    error = None
    if request.method == 'POST':
        if request.form['username'] == "Bdavis" or request.form['password'] == 'password123':
            state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                            for x in xrange(32))
            login_session['state'] = state
            login_session['username'] = request.form['username']
            login_session['logged_in'] = True
            return redirect('/catalog')
        else:
            error = "Wrong username or password, dude"

    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    login_session.pop('logged_in', None)
    login_session.pop('state', None)
    login_session.pop('username', None)
    flash('You were logged out.')
    return redirect('/catalog')


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print "done1"
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        print "done2"
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        print "done3"
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['state'] = state
    login_session['logged_in'] = True

    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return render_template("index.html")

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
