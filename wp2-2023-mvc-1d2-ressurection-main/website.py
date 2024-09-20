from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import sqlite3
import os
from functools import wraps
from lib.testgpt.testgpt import TestGPT
from dotenv import load_dotenv
import csv
from io import StringIO

load_dotenv()



app = Flask(__name__)
app.secret_key = '32kje32nekjwndiqiuwqnidhnweiqdniu'
conn = sqlite3.connect('databases/testgpt.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS notities (
        notitie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT NOT NULL,
        datum DATETIME CURRENT_TIMESTAMP,
        inhoud TEXT NOT NULL,
        bron TEXT NOT NULL,
        categorie TEXT NOT NULL,
        bronnaam TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY(teacher_id) REFERENCES teachers (teacher_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS vragen (
        vragen_id INTEGER PRIMARY KEY,
        notitie_id INTEGER NOT NULL,
        vraag_type TEXT NOT NULL,
        vraag_inhoud TEXT NOT NULL,
        datum DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(notitie_id) REFERENCES notities(notitie_id)
    )
''')

conn.commit()
conn.close()

@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        wachtwoord = request.form['teacher_password']
        conn = sqlite3.connect('databases/testgpt.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE username = ? AND teacher_password = ?", (email, wachtwoord))
        user = cursor.fetchone()
        conn.close()
        if user:
            display_name = user[1]
            session['display_name'] = display_name
            session['teacher_id'] = user[0]
            session['is_admin'] = user[5]
            return redirect(url_for('notities'))
        else:
            return "Login Failed"
    return render_template('Homepage.html')

@app.route('/logout')
def logout():
    session.pop('display_name', None)
    return redirect(url_for('login'))

@app.route('/home')
def homepage():
    return render_template('Homepage.html')
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or session['is_admin'] == 0:
            flash("Je bent geen admin")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin_pagina')
@admin_required
def admin_pagina():
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    conn.close()

    return render_template('admin_pagina.html', teachers=teachers)

@app.route('/delete_teacher/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
    conn.commit()
    conn.close()
    flash('Teacher deleted successfully.')
    return redirect(url_for('admin_pagina'))


@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        is_admin = 1 if request.form.get('is_admin') else 0

        conn = sqlite3.connect('databases/testgpt.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO teachers (display_name, username, teacher_password, is_admin) VALUES (?, ?, ?, ?)',
                       (name, email, password, is_admin))
        conn.commit()
        conn.close()

        flash('Teacher added successfully.')
        return redirect(url_for('admin_pagina'))


@app.route('/notities')
def notities():
    if 'teacher_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    if session.get('is_admin') == 1:
        cursor.execute('SELECT * FROM notities')
    else:
        teacher_id = session['teacher_id']
        cursor.execute('SELECT * FROM notities WHERE teacher_id = ?', (teacher_id,))
    notities = cursor.fetchall()
    conn.close()
    return render_template('Notities.html', notities=notities)


@app.route('/notitie_toevoegen', methods=['POST'])
def notitie_toevoegen():
    if request.method == 'POST':
        if 'teacher_id' not in session:
            return redirect(url_for('login'))
        teacher_id = session['teacher_id']
        titel = request.form['titel']
        datum = request.form['datum']
        inhoud = request.form['inhoud']
        bron = request.form['bron']
        categorie = request.form.getlist('categorie')
        categorie_string = ', '.join(categorie)
        bronnaam = request.form['bronnaam']
        with sqlite3.connect('databases/testgpt.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notities (titel, datum, inhoud, bron, categorie, bronnaam, teacher_id) VALUES (?, ?, ?, ?, ?, ?, ?)', (titel, datum, inhoud, bron, categorie_string, bronnaam, teacher_id))
            conn.commit()
    return redirect(url_for('notitie_weergeven'))

@app.route('/notitie_verwijderen/<int:notitie_id>', methods=['POST'])
def notitie_verwijderen(notitie_id):
    if 'teacher_id' not in session:
        return redirect(url_for('login'))
    teacher_id = session['teacher_id']
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notities WHERE notitie_id = ? AND teacher_id = ?', (notitie_id, teacher_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('notitie_weergeven'))

@app.route('/notitie_weergeven', methods=['get'])
def notitie_weergeven():
    if 'teacher_id' not in session:
        return redirect(url_for('login'))
    teacher_id = session['teacher_id']
    pagina = request.args.get('pagina', 1, type=int)
    sorteer = request.args.get('sorteer', default='')
    zoekterm = request.args.get('zoekterm', '')
    categorie = request.args.get('categorie', '')
    per_pagina = 20
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    order_by_datum = "ORDER BY datum DESC"  # Standaard sortering
    if sorteer == 'nieuw_naar_oud':
        order_by_datum = 'ORDER BY datum DESC'
    elif sorteer == 'oud_naar_nieuw':
        order_by_datum = 'ORDER BY datum ASC'

    zoek_query = 'WHERE teacher_id = ? AND (titel LIKE ? OR inhoud LIKE ?)'
    zoek_params = (teacher_id, '%' + zoekterm + '%', '%' + zoekterm + '%')
    if categorie:
        zoek_query += ' AND categorie = ?'
        zoek_params += (categorie,)

    cursor.execute(f'SELECT COUNT(*) FROM notities {zoek_query}', zoek_params)
    totaal_items = cursor.fetchone()[0]
    totaal_pagina = (totaal_items + per_pagina - 1) // per_pagina

    query = f'SELECT * FROM notities {zoek_query} {order_by_datum} LIMIT ? OFFSET ?'
    cursor.execute(query, zoek_params + (per_pagina, (pagina - 1) * per_pagina))
    notities = cursor.fetchall()
    notitie_vragen = {}
    for notitie in notities:
        notitie_id = notitie[0]
        notitie_vragen[notitie_id] = haal_vragen_op(notitie_id)
    conn.close()

    return render_template('notities_weergeven.html', notities=notities, pagina=pagina, totaal_pagina=totaal_pagina, notitie_vragen=notitie_vragen)

@app.route('/notitie_bijwerken/<int:notitie_id>', methods=['GET', 'POST'])
def notitie_bijwerken(notitie_id):
    teacher_id = session['teacher_id']
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    bericht = None

    if request.method == 'POST':
        if 'teacher_id' not in session:
            return redirect(url_for('login'))
        titel = request.form['titel']
        datum = request.form['datum']
        inhoud = request.form['inhoud']
        bron = request.form['bron']
        categorie = request.form.getlist('categorie')
        categorie_string = ', '.join(categorie)
        bronnaam = request.form['bronnaam']
        cursor.execute('UPDATE notities SET titel = ?, datum = ?, inhoud = ?, bron = ?, categorie = ?, bronnaam = ? WHERE notitie_id = ?', (titel, datum, inhoud, bron, categorie_string, bronnaam, notitie_id))
        conn.commit()
        bericht = "Notitie is bijgewerkt."

    cursor.execute('SELECT * FROM notities WHERE notitie_id = ? AND teacher_id = ?', (notitie_id, teacher_id,))
    notitie_tuple = cursor.fetchone()

    if notitie_tuple:
        columns = [column[0] for column in cursor.description]
        notitie = dict(zip(columns, notitie_tuple))
    else:
        notitie = None

    conn.close()
    return render_template('notitie_bijwerken.html', notitie=notitie, bericht=bericht)


@app.route('/genereer_vragen', methods=['POST'])
def genereer_vragen():
    notitie_id = request.form.get('notitie_id')
    vraag_type = request.form.get('vraag_type')
    notitie_inhoud = haal_notitie_op(notitie_id)
    api_key = os.getenv('test_gpt')
    test_gpt = TestGPT(api_key)

    try:
        if vraag_type == 'open':
            open_vragen = test_gpt.generate_open_question(notitie_inhoud)
            if not isinstance(open_vragen, list):
                open_vragen = open_vragen.split('\n')
                for vraag in open_vragen:
                    sla_vraag_op(notitie_id, 'open', vraag)
            return render_template('genereer_vragen.html', open_vragen=open_vragen, vragen_meerkeuze=[])

        elif vraag_type == 'meerkeuze':
            vragen_meerkeuze = test_gpt.generate_multiple_choice_question(notitie_inhoud)
            if not isinstance(vragen_meerkeuze, list):
                vragen_meerkeuze = vragen_meerkeuze.split('\n')
                for vraag in vragen_meerkeuze:
                    sla_vraag_op(notitie_id, 'meerkeuze', vraag)
            return render_template('genereer_vragen.html', open_vragen=[], vragen_meerkeuze=vragen_meerkeuze)

        else:
            flash("Selecteer een type vraag.", "foutmelding")
            return redirect(url_for('notitie_weergeven'))

    except Exception as e:
        flash(str(e), "foutmelding")
        return redirect(url_for('notitie_weergeven'))

def haal_notitie_op(notitie_id):
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute('SELECT inhoud FROM notities WHERE notitie_id = ?', (notitie_id,))
    notitie = cursor.fetchone()
    conn.close()

    if notitie:
        return notitie[0]
    else:
        print("Geen notitie gevonden met ID:", notitie_id)
        return None

def sla_vraag_op(notitie_id, vraag_type, vraag_inhoud):
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vragen (notitie_id, vraag_type, vraag_inhoud) VALUES (?, ?, ?)', (notitie_id, vraag_type, vraag_inhoud))
    conn.commit()
    conn.close()

def haal_vragen_op(notitie_id):
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute('SELECT vraag_inhoud FROM vragen WHERE notitie_id = ?', (notitie_id,))
    vragen = cursor.fetchall()
    return [vraag[0] for vraag in vragen]

@app.route('/vragen_verwijderen/<int:notitie_id>', methods=['POST'])
def vragen_verwijderen(notitie_id):
    if 'teacher_id' not in session:
        return redirect(url_for('login'))
    teacher_id = session['teacher_id']
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vragen WHERE notitie_id = ?', (notitie_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('notitie_weergeven'))

@app.route('/export_vragen_csv/<int:notitie_id>')
def export_vragen_csv(notitie_id):
    conn = sqlite3.connect('databases/testgpt.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        notities.notitie_id, 
        notities.titel, 
        notities.datum AS notitie_datum, 
        notities.inhoud, 
        notities.bron, 
        notities.categorie, 
        notities.bronnaam, 
        vragen.vragen_id, 
        vragen.vraag_type, 
        vragen.vraag_inhoud, 
        vragen.datum AS vraag_datum 
    FROM 
        notities 
    JOIN 
        vragen ON notities.notitie_id = vragen.notitie_id
    WHERE
        notities.notitie_id = ?
""", (notitie_id,))
    resultaten = cursor.fetchall()
    conn.close()

    rijen = [["Notitie ID, Titel, Datum, Inhoud, Bron, Categorie, Bronnaam, Vraag ID, Vraag Type, Vraag Inhoud, Datum"]]
    rijen.extend(resultaten)

    def generate_csv(rijen):
        data = StringIO()
        writer = csv.writer(data)
        for rij in rijen:
            writer.writerow(rij)
            data.seek(0)
            yield data.read()
            data.seek(0)
            data.truncate(0)

    return Response(
        generate_csv(rijen),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=vragen_en_antwoorden.csv"}
    )

if __name__=='__main__':
    app.run(debug=True)