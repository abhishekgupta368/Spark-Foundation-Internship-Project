from flask import Flask,render_template,request, url_for, jsonify
import sqlite3 as sql
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    conn = sql.connect('school.db')
    c = conn.cursor()
    c.execute('CREATE TABLE  IF NOT EXISTS student (name text, country text, city text, email text, address text, school text)')
    c.execute('CREATE TABLE  IF NOT EXISTS course (course_name text, course_code text, faculty text, book text, department text)')
    c.execute('CREATE TABLE  IF NOT EXISTS teacher (faculty_name text, course_name text, faculty_id text, email text, department text)')
    c.execute('CREATE TABLE  IF NOT EXISTS item (item_name text, code text, cost text, color text, supplier text)')
    conn.commit()
    conn.close()
    return render_template('index.html')

@app.route('/home')
def home():
    conn = sql.connect('school.db')
    c = conn.cursor()
    c.execute('CREATE TABLE  IF NOT EXISTS student (name text, country text, city text, email text, address text, school text)')
    c.execute('CREATE TABLE  IF NOT EXISTS course (course_name text, course_code text, faculty text, book text, department text)')
    c.execute('CREATE TABLE  IF NOT EXISTS teacher (faculty_name text, course_name text, faculty_id text, email text, department text)')
    c.execute('CREATE TABLE  IF NOT EXISTS item (item_name text, code text, cost text, color text, supplier text)')
    conn.commit()
    conn.close()
    return render_template('index.html') 
@app.route('/item_insert',methods=['GET', 'POST'])
def item_insert():
    return render_template('Items_insert.html')

@app.route('/item_update',methods=['GET', 'POST'])
def item_update():
    name = []
    conn = sql.connect('school.db')
    c = conn.cursor()
    for a in c.execute('SELECT * FROM item'):
        name.append(a[0])
    conn.commit()
    conn.close()
    return render_template('Items_update.html',name=name)

@app.route('/item_retrive',methods=['GET', 'POST'])
def item_retrive():
    res=[]
    conn = sql.connect('school.db')
    c = conn.cursor()
    for a in c.execute('SELECT * FROM item'):
        res.append(a)
    conn.commit()
    conn.close()
    return render_template('Items_retrive.html',res=res)

@app.route('/item_delete',methods=['GET', 'POST'])
def item_delete():
    name = []
    conn = sql.connect('school.db')
    c = conn.cursor()
    for a in c.execute('SELECT * FROM item'):
        name.append(a[0])
    conn.commit()
    conn.close()
    print(name)
    return render_template('Items_delete.html',name=name)

@app.route('/handle_insert_item',methods=['GET', 'POST'])
def handle_insert_item():
    conn = sql.connect('school.db')
    c = conn.cursor()
    if request.method=='POST':
        name = str(request.form["name"])
        code = str(request.form["code"])
        cost = str(request.form["cost"])
        color = str(request.form["color"])
        supplier = str(request.form["supplier"])
        c.execute('INSERT INTO item VALUES(?,?,?,?,?)', (name,code,cost,color,supplier,))
        conn.commit()
        conn.close()
        flag="value inserted in api"
        return render_template('Items_insert.html',flag=flag)
    else:
        return "Something goes Worang!!!!!"
    
@app.route('/handle_delete_item',methods=['GET', 'POST'])
def handle_delete_item():
    conn = sql.connect('school.db')
    c = conn.cursor()
    if request.method == "POST":
        username = str(request.form['name'])
        c.execute('DELETE FROM item WHERE item_name=(?)',(username,))
        name = []
        for a in c.execute('SELECT * FROM item'):
            name.append(a[0])
        conn.commit()
        conn.close()
        flag="Course Removed"
        return render_template('Items_delete.html',flag=flag,name=name)
    else:
        return "Something goes Worang"

@app.route('/handle_update_item',methods=['GET', 'POST'])
def handle_update_item():
    conn = sql.connect('school.db')
    c = conn.cursor()
    if request.method=='POST':
        name = str(request.form["name"])
        code = str(request.form["code"])
        cost = str(request.form["cost"])
        color = str(request.form["color"])
        supplier = str(request.form["supplier"])
        #(item_name text, code text, cost text, color text, supplier text)
        c.execute('UPDATE item SET code=(?),cost=(?),color=(?),supplier=(?) WHERE item_name=(?)',(code,cost,cost,color,supplier,))
        name = []
        for a in c.execute('SELECT * FROM course'):
            name.append(a[0])
        conn.commit()
        conn.close()
        flag="Student Information updated"
        return render_template('Items_update.html',flag=flag,name=name)
    else:
        return "Something goes Worang"

@app.route('/item_check_api',methods=['GET', 'POST'])
def item_check_api():
    data=[]
    conn = sql.connect('school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM item')
    row = c.fetchall()
    i=1
    for a in row:
        data.append({'Item '+str(i):{'Item Name':a[0],'Code':a[1],'Cost':a[2],'Color':a[3],'Supplier':a[4]}})
        i+=1
    res = jsonify(data)
    conn.commit()
    conn.close()
    return res

if __name__ == '__main__':
    app.run(debug=True)