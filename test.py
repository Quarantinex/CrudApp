import pandas as pd
import xlrd
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysql_html import pymysql


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='upload',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


data = pd.read_excel('crud_data.xlsx')

book = xlrd.open_workbook("crud_data.xlsx")
sheet = book.sheet_by_name("Sheet1")
for r in range(1, sheet.nrows):
    emp = sheet.cell(r, 0).value
    name = sheet.cell(r, 1).value
    email = sheet.cell(r, 2).value
    mobile = sheet.cell(r, 3).value
    print(emp, name, email, mobile)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO employees(Id, Name, Email, Mobile) VALUES (%s, %s, %s, %s)", (emp, name, email, mobile))
    cursor.close()
    connection.commit()
    connection.close()
