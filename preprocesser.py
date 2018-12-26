# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 17:08:55 2018

@author: tt
"""

import glob
import re
import sqlite3
import csv


def parser(Pfizer):
    # Open a TXT file. Store all articles in a list. Each article is an item
    # of the list. Split articles based on the location of such string as
    # 'Document PRN0000020080617e46h00461'

    articles = []
    with open('Pfizer1.txt', 'r') as infile:
        data = infile.read()
    start = re.search(r'\n HD\n', data).start()
    for m in re.finditer(r'Document [a-zA-Z0-9]{25}\n', data):
        end = m.end()
        a = data[start:end].strip()
        a = '\n   ' + a
        articles.append(a)
        start = end

    # In each article, find all used Intelligence Indexing field codes. Extract
    # content of each used field code, and write to a CSV file.

    # All field codes (order matters)
    fields = ['HD', 'CR', 'WC', 'PD', 'ET', 'SN', 'SC', 'ED', 'PG', 'LA', 'CY', 'LP',
              'TD', 'CT', 'RF', 'CO', 'IN', 'NS', 'RE', 'IPC', 'IPD', 'PUB', 'AN']

    for a in articles:
        used = [f for f in fields if re.search(r'\n   ' + f + r'\n', a)]
        unused = [[i, f] for i, f in enumerate(fields) if not re.search(r'\n   ' + f + r'\n', a)]
        fields_pos = []
        for f in used:
            f_m = re.search(r'\n   ' + f + r'\n', a)
            f_pos = [f, f_m.start(), f_m.end()]
            fields_pos.append(f_pos)
        obs = []
        n = len(used)
        for i in range(0, n):
            used_f = fields_pos[i][0]
            start = fields_pos[i][2]
            if i < n - 1:
                end = fields_pos[i + 1][1]
            else:
                end = len(a)
            content = a[start:end].strip()
            obs.append(content)
        for f in unused:
            obs.insert(f[0], '')
        obs.insert(0, Pfizer.split('/')[-1].split('.')[0])  # insert Company ID, e.g., GVKEY
        print("*****************************************************")
        print(obs)
        print("*****************************************************")
        cur.execute('''INSERT INTO articles
                       (id, hd, cr, wc, pd, et, sn, sc, ed, pg, la, cy, lp, td, ct, rf,
                       co, ina, ns, re, ipc, ipd, pub, an)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?)''', obs)


# Write to SQLITE
conn = sqlite3.connect('factiva.db')
with conn:
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS articles')
    # Mirror all field codes except changing 'IN' to 'INC' because it is an invalid name
    cur.execute('''CREATE TABLE articles
                   (nid integer primary key, id text, hd text, cr text, wc text, pd text,
                   et text, sn text, sc text, ed text, pg text, la text, cy text, lp text,
                   td text, ct text, rf text, co text, ina text, ns text, re text, ipc text,
                   ipd text, pub text, an text)''')
    for f in glob.glob('*.txt'):
        print(f)
        parser(f)

# Write to CSV to feed Stata
with open('factiva1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE CT like ?", ["%Pfizer%"])
        colname = [desc[0] for desc in cur.description]
        writer.writerow(colname)
        for obs in cur.fetchall():
            writer.writerow(obs)