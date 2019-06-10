from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysql_html import pymysql
import xlrd

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='crud',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.secret_key = "flash message"


@app.route('/')
def index():
    cur = connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        emp = request.form['Id']
        name = request.form['Name']
        email = request.form['Email']
        mobile = request.form['Mobile']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employees(Id, Name, Email, Mobile) VALUES (%s, %s, %s, %s)", (emp, name, email, mobile))
        connection.commit()
        return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        file = request.form['File']
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_name("Sheet1")
        for r in range(1, sheet.nrows):
            emp = sheet.cell(r, 0).value
            name = sheet.cell(r, 1).value
            email = sheet.cell(r, 2).value
            mobile = sheet.cell(r, 3).value
            cursor = connection.cursor()
            cursor.execute("INSERT INTO employees(Id, Name, Email, Mobile) VALUES (%s, %s, %s, %s)",
                           (emp, name, email, mobile))
            connection.commit()
            return redirect(url_for('index'))


@app.route('/update', methods={'POST', 'GET'})
def update():
    if request.method == 'POST':
        id_data = request.form['Id']
        name = request.form['Name']
        email = request.form['Email']
        mobile = request.form['Mobile']

        cur = connection.cursor()
        sqlcmd = "UPDATE employees SET Name='"+name+"', Email='"+email+"', Mobile='"+mobile+"' WHERE Id="+str(id_data)
        cur.execute(sqlcmd)
        flash("Data Updated Successfully")
        connection.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods={'POST', 'GET'})
def delete(id_data):
    flash("Data Deleted Successfully")
    cur = connection.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s",(id_data))
    connection.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
