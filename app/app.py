from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_mysqldb import MySQL

from config import config  # Fichero config

app = Flask(__name__)
db = MySQL(app)
# Datos que utiliza el servidor (se usa para módulo → flash)
app.secret_key = 'mysecretkey'


# PAGE INDEX
@app.route('/')
def index():
    # return 'Run Server'
    return render_template('index.html')


# PAGE FORM NEW DATA
@app.route('/new')
def new_contact():
    return render_template('/new.html')


# PAGE TABLE LIST DATA
@app.route('/list')
def list_contact():
    cur = db.connection.cursor()
    query = """SELECT * FROM contacts"""
    cur.execute(query)
    result = cur.fetchall()
    # print(result)
    cur.close()
    return render_template('/list.html', data=result)


# ADD NEW DATA
@ app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        cur = db.connection.cursor()
        query = """INSERT INTO contacts (firstname, lastname, email, phone, message)
                    VALUES(%s, %s, %s, %s, %s)"""
        params = (firstname, lastname, email, phone, message)
        cur.execute(query, params)
        db.connection.commit()
        cur.close()
        # The session is unavailable because no secret key was set.
        flash('Contacto registrado con exito!')
        return redirect(url_for('list_contact'))
    else:
        return 'Select Correct Method Http'


# FORM SHOW EDIT DATA
@ app.route('/edit_contact/<id_contact>')
def get_contact(id_contact):
    cur = db.connection.cursor()
    query = "SELECT * FROM contacts WHERE id = {0}".format(id_contact)
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    return render_template('/edit.html', data=result)


# UPDATE DATA
@app.route('/update_contact/<id_contact>', methods=['POST'])
def update_contact(id_contact):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        cur = db.connection.cursor()
        query = """UPDATE contacts SET 
                        firstname = %s, 
                        lastname = %s, 
                        email = %s, 
                        phone = %s, 
                        message = %s
                    WHERE id = %s
                    """
        params = (firstname, lastname, email, phone, message, id_contact)
        cur.execute(query, params)
        db.connection.commit()
        cur.close()
        flash('Contacto actualilzado con exito!')
        return redirect(url_for('list_contact'))
    else:
        return 'Select Correct Method Http'


# DELETE DATA
@ app.route('/delete_contact/<id_contact>')
def delete_contact(id_contact):
    cur = db.connection.cursor()
    query = "DELETE FROM contacts WHERE id = {0}".format(id_contact)
    cur.execute(query)
    db.connection.commit()
    cur.close()
    flash('Contacto eliminado con exito!')
    return redirect(url_for('list_contact'))


#####################################################################
# OTHER ROUTES
#####################################################################

# ERROR 404


def page_not_found(error):
    # return render_template('404.html'), 404 # Mostrar una plantilla
    return redirect(url_for('index'))  # Redireccionar a otra url


#####################################################################
# RUN SERVER
#####################################################################

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()
