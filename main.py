from flask import Flask, request, render_template ,redirect, url_for
import sqlite3

app = Flask(__name__)

def addData(data):
    conn = sqlite3.connect('data.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS DATA (VALUE TEXT NOT NULL);''')
    sql = ''' INSERT INTO DATA(VALUE) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql,(data,))
    conn.commit()
    return cur.lastrowid

def display():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    sql = ('''SELECT * FROM DATA;''')
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    data = []
    for i in rows:
        data.append(list(i)[0])
    return data

def deleteData(data):
    conn = sqlite3.connect('data.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS DATA (VALUE TEXT NOT NULL);''')
    sql = '''DELETE FROM DATA WHERE VALUE=(?);'''
    cur = conn.cursor()
    cur.execute(sql,(str(data),))
    conn.commit()
    conn.close()
    return cur.lastrowid

def updateData(data,updatedText):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    values =(updatedText,data,)
    sql = '''UPDATE DATA SET VALUE = ? WHERE VALUE = ? '''
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return cur.lastrowid

def checkData(value):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS DATA (VALUE TEXT NOT NULL);''')
    sql = ('''SELECT * FROM DATA;''')
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    data = []
    for i in rows:
        data.append(list(i)[0])
    if value in data:
        return True
    else:
        return False

def checkEmpty():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS DATA (VALUE TEXT NOT NULL);''')
    sql = ('''SELECT * FROM DATA;''')
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    data = []
    for i in rows:
        data.append(list(i)[0])
    if (len(data) == 0):
        return True
    else:
        return False


@app.route('/', methods =["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/add', methods =["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form["text"]
        if checkData(data):
            return render_template('add.html',command = "Same word already present in directory",color="Red")
        elif " " in data:
            return render_template('add.html',command = "Please enter one word at a time",color="Red")
        else:
            addData(data)
            return render_template('add.html',command = "Data added successfully",color="Green")
    return render_template('add.html',command = "")

@app.route('/delete', methods =["GET", "POST"])
def delete():
    data = display()
    if request.method == "POST":
        value = request.form["value"]
        deleteData(value)
        data = display()
        return render_template('success.html',header="Delete a record from the database",comment="File Deleted successfull")
    if(checkEmpty()):
        return render_template('empty.html',header="Delete a record from the database",comment="Database empty : Please insert data first.")
    else:
        return render_template('delete.html',data = data,command ="")

@app.route('/update', methods =["GET", "POST"])
def update():
    data = display()

    if request.method == "POST":
        value = request.form["value"]
        update = request.form["updatedText"]
        if " " in update:
            data = display()
            return render_template('update.html',data = data,command = "Please enter one word at a time")
        elif checkData(update):
            data = display()
            return render_template('update.html',data = data,command = "Same word already present in database")
        else:
            updateData(value,update)
            return render_template('success.html',header="Update a record from the database",comment="File updated successfull")
    if(checkEmpty()):
        return render_template('empty.html',header="Update a record from the database",comment="Database empty : Please insert data first.")
    else:
        return render_template('update.html',data = data,command = "")

@app.route('/view', methods =["GET", "POST"])
def view():
    data = display()
    if(checkEmpty()):
        return render_template('empty.html',header="Displaying all the record from the database",comment="Database empty : Please insert data first.")
    else:
        return render_template('view.html',data = data)

if __name__=='__main__':
    app.run(debug = True)
