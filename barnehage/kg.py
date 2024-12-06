from flask import Flask, render_template, request, redirect, session, url_for
from kgmodel import Foresatt, Barn, Soknad, Barnehage
from kgcontroller import (form_to_object_soknad, insert_soknad, commit_all, select_alle_barnehager)
import pandas as pd

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'  # Nødvendig for session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barnehager')
def barnehager():
    information = select_alle_barnehager()
    return render_template('barnehager.html', data=information)

@app.route('/behandle', methods=['GET', 'POST'])
def behandle():
    if request.method == 'POST':
        sd = request.form
        print(sd)
        log = insert_soknad(form_to_object_soknad(sd))
        print(log)
        session['information'] = sd
        commit_all()  # Sørg for at vi skriver til Excel etter innsending av søknad
        return redirect(url_for('svar'))
    else:
        return render_template('soknad.html')

@app.route('/svar')
def svar():
    information = session['information']
    pri = information['liste_over_barnehager_prioritert_5']
    bh_liste = select_alle_barnehager()
    available_spots = []
    for el in pri.split(','):
        for bh_el in bh_liste:
            if bh_el.barnehage_id == int(el):
                if bh_el.barnehage_ledige_plasser > 0:
                    available_spots.append(bh_el)
    pri_rights = False
    return render_template('svar.html',
                           data=information,
                           available_spots=available_spots,
                           priority_rights=pri_rights)

@app.route('/commit')
def commit():
    # Etter commit_all(), last inn de nyeste dataene fra Excel
    global forelder, barnehage, barn, soknad
    forelder = pd.read_excel('kgdata.xlsx', sheet_name='foresatt')
    barnehage = pd.read_excel('kgdata.xlsx', sheet_name='barnehage')
    barn = pd.read_excel('kgdata.xlsx', sheet_name='barn')
    soknad = pd.read_excel('kgdata.xlsx', sheet_name='soknad')

    # Konverter DataFrames til dictionaries for visning i HTML
    data_forelder = forelder.to_dict(orient='records')
    data_barnehage = barnehage.to_dict(orient='records')
    data_barn = barn.to_dict(orient='records')
    data_soknad = soknad.to_dict(orient='records')

    return render_template('commit.html',
                           data_forelder=data_forelder,
                           data_barnehage=data_barnehage,
                           data_barn=data_barn,
                           data_soknad=data_soknad)
