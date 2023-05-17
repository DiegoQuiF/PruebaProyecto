from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

def connection():
    s = 'LAPTOP-3H729AV9\SQLEXPRESS'    #Nombre del servidor
    d = 'CarSales'  #DataBase, va igual
    u = ''      #usuario de la BD
    p = ''      #contraseña de la BD
    #línea de conexión con autentificación de windows
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+s+';DATABASE='+d+';Trusted_Connection=yes;'
    #línea de conexión con usuario de sql server
    #cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

@app.route("/")
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [dbo].[TblCars]")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name":row[1], "year":row[2], "price":row[3]})
    conn.close()
    return render_template("carslist.html", cars = cars)


@app.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html")
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.TblCars (id, name, year, price) VALUES (?, ?, ?, ?)", id, name, year, price)
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM dbo.TblCars WHERE id = ?", id)
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        cursor.execute("UPDATE dbo.TblCars SET name = ?, year = ?, price = ? WHERE id = ?", name, year, price, id)
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/deletecar/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.TblCars WHERE id = ?", id)
    conn.commit()
    conn.close()
    return redirect('/')


if(__name__ == "__main__"):
    app.run(debug=True, port=5000)