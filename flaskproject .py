from flask import Flask,request,render_template
import sqlite3 as sql
app=Flask(__name__)
connection_object= sql.connect('COVID.db')
cursor_object=connection_object.cursor()
# cursor_object.execute('DROP TABLE IF EXISTS COVID')
table = ''' CREATE TABLE IF NOT EXISTS COVID(
       ADARNUMBER VARCHAR(25) PRIMARY KEY NOT NULL,
       NAME VARCHAR(25) NOT NULL,
       AGE INT,
       DOSES INT
     );'''
cursor_object.execute(table)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def covid_details():
   return render_template('covid.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try: 
         adarnumber = request.form['adarnumber']
         name = request.form['name']
         age = request.form['age']
         doses=request.form['doses']
         
         with sql.connect("COVID.db") as con:
            cur=con.cursor()
            cur.execute("INSERT INTO COVID (ADARNUMBER,NAME,AGE,DOSES) VALUES (?,?,?,?)",(adarnumber,name,age,doses))
            
            con.commit()
            msg ="Record successfully added"
      except:
          con.rollback()
          msg = "error in insert operation"
      
      finally:
          con.close()
          return render_template("result.html",msg = msg)
         
@app.route('/list')
def list():
   connection_object = sql.connect("covid.db")
   connection_object.row_factory = sql.Row
   
   cursor_object = connection_object.cursor()
   cursor_object.execute("select * from covid")
   
   rows = cursor_object.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
