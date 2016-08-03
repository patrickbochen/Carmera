#Local webapp to expedite hand labeling images for training

#imports for flask to run
from flask import Flask
from flask import render_template
from flask import flash, redirect
from flask import request, session, g, url_for, abort, jsonify

import os
import sqlite3
import time
import numpy as np

#imports for wtforms
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from json import JSONEncoder
import random

from carmera import Carmera
cm          = Carmera(api_key="69d2724e760ab8756c4054a9b54d4b44ef6bc4fc")
cm.url_base = "http://192.168.60.2" # Note how this IP is Euclids Vagrant files private IP
im          = cm.Image()



#Class for a form for labeling - not important at all
class LabelForm(Form):
    safe = BooleanField('safe', default=False)
    residential = BooleanField('residential', default=False)
    outside_venue = BooleanField('outside_venue', default=False)
    tourist = BooleanField('tourist', default=False)
    old = BooleanField('old', default=False)
    modern = BooleanField('modern', default=False)
    poor = BooleanField('poor', default=False)
    rich = BooleanField('rich', default=False)
    construction = BooleanField('construction', default=False)

# create our little application :)                                                               
app = Flask(__name__)
app.config.from_object('config')

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'hotnot.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('HOTNOT_SETTINGS', silent=True)

#global variable that determines the unique ids in the database
unique_ids = np.loadtxt("unique_ids.txt", dtype = bytes, delimiter='\n').astype(str)
unique_holder = 0

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print ('Initialized the database.')

#Helper method with database queries
def query(sql, params=None):
    db  = get_db()
    res = None
    if params is None:
        cur = db.execute(sql)
    else:
        cur = db.execute(sql % params)
    db.commit()
    if "SELECT " in sql.upper():
        res = cur.fetchall()
    #db.close()
    if res is not None:
        return res

#Determine next image to be chosen for labeling
def nextImage():
    #Randomly choose an image_id from a file of examined images
    # rndm_select = random.randint(0,200)
    # fp = open("crowdAIExp.txt",'r')
    # for i, line in enumerate(fp):
    #     if (i == rndm_select) :
    #     ## Download image by id and save to disk
    #         line = line.replace("\n", "")
    #         rndm_image_id = line
    # fp.close()

    #Complete random images
    rndm_image_id = random.randint(1, 300000)
    #rndm_image_id = 22519

    # Get image by ID
    try:
        res = im.get_by_id(rndm_image_id)
        ## Do stuff with response
        data = res.json()
        return data

    except Exception as e:
        print(e.code)  ## HTTP status code
        print(e.error) ## JSON error message

#Home page shows entries
@app.route('/')
def home():
    sql = "SELECT * FROM entries"
    entries = query(sql)
    return render_template('show_entries.html', entries=entries)

#Writes database into training and testing files
@app.route('/tofile')
def save_file():
    train_file_name = 'train_2.txt'
    test_file_name = 'test_2.txt'

    #Won't overwrite training files (in case of accident page switch)
    if os.path.isfile(train_file_name):
        status = "Training files already exists!"
    else:
        sql = "SELECT * FROM entries"
        entries = query(sql)
        oTrain_file = open(train_file_name, 'w+')
        oTest_file = open(test_file_name, 'w+')
        test_data = 0
        #This changes depending on the labels you trained on
        #This order needs to be preserved in label_names.txt file
        label_ids = ['Safe', 'Green', 'Family Friendly', 'Beautiful', 'Desolate', 'Vibrant']

        #Changes label to numeric value and writes to file
        for row in entries:
            new_label_id = None
            for i in range(6):
                if row[2] == label_ids[i]:
                    new_label_id = i
                    i = 6

            if new_label_id == None:
                continue
            else:
                test_data += 1
                #need to add the path to the file name depending on environment
                #Writes every 10th datapoint into the testing file
                if test_data % 10 == 0:
                    oTest_file.write('%r.jpg %r\n' % (row[1], new_label_id))
                else:
                    oTrain_file.write('%r.jpg %r\n' % (row[1], new_label_id))

        oTrain_file.close()
        oTest_file.close()
        status = "Training files successfully created"
    return render_template('trainfile.html', status = status)

#Creates a file containing the unique_ids in the database
@app.route('/list_unique_ids')
def list_unique_ids():
    file_name = 'unique_ids.txt'

    if os.path.isfile(file_name):
        status = "Training files already exists!"
    else:
        sql = "SELECT * FROM entries"
        entries = query(sql)
        unique_file = open(file_name, 'w+')

        prev = 'None'

        for row in entries:
            #i need to add the path to the file name as well when i finally work in ubuntu
            if prev == row[1]:
                continue
            else:
                unique_file.write('%r\n' % (row[1]))
            prev = row[1]
        unique_file.close()
        status = "Training files successfully created"
    return render_template('trainfile.html', status = status)

#Shows the entires in the database
@app.route('/entries')
def show_entries():
    entries = query('select image_id, tag from entries order by id desc')
    print (entries)
    return render_template('show_entries.html', entries=entries)

#Random playing around with FLASK
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           #title='Test',
                           user=user)

#Adds image and labels into database using request.json
#Returns the response.json
@app.route('/add', methods=['POST'])
def add_entry():
    for tag in request.json['tags']:
        sql = "INSERT INTO entries (image_id, tag) VALUES (%i, \"%s\")"
        query(sql, (int(request.json['image_id']), tag))

    image_data = nextImage()
    #print (image_data)
    new_id = image_data['properties']['id']
    new_url = image_data['properties']['url']

    ## add some logic for choosing next image
    return jsonify({"success":True, "code": 201, "image_id" : new_id, "src": new_url}), 201


#Skips image during labeling (if poor quality, repeated, etc)
@app.route('/skip', methods=['POST'])
def skip_entry():
    image_data = nextImage()
    #print (image_data)
    new_id = image_data['properties']['id']
    new_url = image_data['properties']['url']

    ## add some logic for choosing next image
    return jsonify({"success":True, "code": 201, "image_id" : new_id, "src": new_url}), 201


#Labels images
@app.route('/label', methods=['GET', 'POST'])
def label():
    #Finds an image
    image_data = None
    while image_data == None:
        image_data = nextImage()
        time.sleep(1)

    new_id = image_data['properties']['id']
    new_url = image_data['properties']['url']

    #POSTs the image_id and image_src to the template for the ADD function
    form = LabelForm()
    return render_template('label.html', 
                           title='Create set',
                           form=form,
                           image_id=new_id,
                           image_src=new_url)

#Runs through old images in case you want to add a label
#Alternative for choosing images
def cycleOldImages():
    try:
        global unique_holder
        global unique_ids
        image_id = unique_ids[unique_holder]

        print (image_id)
        res = im.get_by_id(image_id)
        unique_holder+=1
        ## Do stuff with response
        data = res.json()
        return data

    except Exception as e:
        print(e.code)  ## HTTP status code
        print(e.error) ## JSON error message


#Relabeling old images - Can improve this sections modularity, thrown together
@app.route('/relabel', methods=['GET', 'POST'])
def relabel():
    #image_data = None
    #while image_data == None:
    image_data = cycleOldImages()
    time.sleep(1)

    new_id = image_data['properties']['id']
    new_url = image_data['properties']['url']

    return render_template('relabel.html', 
                            title='Add labels',
                            image_id=new_id,
                            image_src=new_url)

@app.route('/relabel_add', methods=['POST'])
def relabel_add():
    for tag in request.json['tags']:
        sql = "INSERT INTO entries (image_id, tag) VALUES (%i, \"%s\")"
        query(sql, (int(request.json['image_id']), tag))

    image_data = cycleOldImages()
    #print (image_data)
    new_id = image_data['properties']['id']
    new_url = image_data['properties']['url']

    ## add some logic for choosing next image
    return jsonify({"success":True, "code": 201, "image_id" : new_id, "src": new_url}), 201

@app.route('/relabel_skip', methods=['POST'])
def relabel_skip():
    image_data = cycleOldImages()
    #print (image_data)
    new_id = image_data['properties']['id']
    new_url = image_data['properties']['url']

    ## add some logic for choosing next image
    return jsonify({"success":True, "code": 201, "image_id" : new_id, "src": new_url}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0")
#addtag -id,tag - database connection, insert                                                    
#1 model - 1 id, tag (string)                                                                    
#increment id, image_id, tag, time -created_at
#use javascript response save to endpoint to save data
