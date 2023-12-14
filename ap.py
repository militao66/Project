from flask import Flask, render_template, url_for, flash, request, current_app, redirect
from flaskext.mysql import MySQL
import pymysql
import os

app = Flask(__name__)

app.secret_key = 'secret'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'students'
app.config['MYSQL_DATABASE_USER'] = 'root'

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student/<id>')
def students_details(id):
    word_id=id
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from data where id=%s', (word_id))
    rv = cur.fetchall()
    students_details=rv
    cur.close()
    return render_template('student_details.html', words=students_details)

@app.route('/student/<id>/update', methods = ['GET, POST'])
def students_details_update(id):
    word_id=id
    if request.method == 'GET':
        print('This is get method')
        return render_template('student_details.html')
    else:
        status = request.form('status')
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('update word set status=%s where id=%s', (status, word_id))
        conn.commit()
        cur.close()

@app.route('/students', methods = ['GET', 'POST'])
def students_index():
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from data')
    rv = cur.fetchall()
    return render_template('students_index.html', words=rv)


# route handler for image
@app.route('/portal', methods=['GET', 'POST'])
def portal_form():
    if request.method == 'GET' :
        return render_template('portal_form.html')
    else:
        image = request.files['image']
        if image :
            filepath = os.path.join(current_app.root_path, 'static/images/profile_pic.PNG')
            image.save(filepath)
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']
        gender = request.form['gndr']
        address = request.form['address']
        state = request.form['state']
        score = int(request.form['score'])
        if score > '200':
            status = 'undecided'
        local = request.form['lg']
        kin = request.form['kin']
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('insert into data(fname, mname , lname , email , dob , phone, gender, address , state , score , status , local , kin ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (fname, mname , lname , email , dob , phone, gender, address , state , score , status , local, kin ))
        conn.commit()
        cur.close()
        return redirect(url_for('students_index'))



if __name__ == "__main__":
    app.run(debug=True)