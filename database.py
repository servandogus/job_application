#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import main as efc
import pandas as pd

# création db et une table
db_connexion = sqlite3.connect('database.sqlite')

# pas besoin de créer la base, la méthode to_sql s'en charge. 
#cursor = db_connexion.cursor()
#cursor.execute('create table if not exists python(id integer primary key, JobTitle text, Link text, Salary text, Location text, PositionType text, Company text, Date text, Summary text, Description text)')

# creation de donnée en dataframe
d = efc.get_EFC_results('python')

# sauvegarde dans la base
d.to_sql('python', con = db_connexion, if_exists = 'append')

# commit
db_connexion.commit

# close
#cursor.close()
