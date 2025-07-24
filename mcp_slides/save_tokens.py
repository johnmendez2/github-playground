# save_tokens.py

import csv
import sqlite3
from datetime import datetime
import os
import psycopg2
import mysql.connector

def save_to_csv(service, client_id, client_secret, access_token, refresh_token, scopes):
    filename = "tokens.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "service", "client_id", "client_secret", "access_token", "refresh_token", "scopes"])
        writer.writerow([
            datetime.now().isoformat(),
            service,
            client_id,
            client_secret,
            access_token,
            refresh_token,
            ",".join(scopes)
        ])

def save_to_sqlite(service, client_id, client_secret, access_token, refresh_token, scopes):
    conn = sqlite3.connect("oauth_tokens.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            service TEXT,
            client_id TEXT,
            client_secret TEXT,
            access_token TEXT,
            refresh_token TEXT,
            scopes TEXT
        )
    """)

    cur.execute("""
        INSERT INTO tokens (timestamp, service, client_id, client_secret, access_token, refresh_token, scopes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        service,
        client_id,
        client_secret,
        access_token,
        refresh_token,
        ",".join(scopes)
    ))

    conn.commit()
    conn.close()

def save_to_postgres(service, client_id, client_secret, access_token, refresh_token, scopes):
    conn = psycopg2.connect(
        host="localhost",
        database="your_db",
        user="your_user",
        password="your_password"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id SERIAL PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            client_id TEXT,
            client_secret TEXT,
            access_token TEXT,
            refresh_token TEXT,
            scopes TEXT
        )
    """)

    cur.execute("""
        INSERT INTO tokens (timestamp, service, client_id, client_secret, access_token, refresh_token, scopes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.now().isoformat(),
        service,
        client_id,
        client_secret,
        access_token,
        refresh_token,
        ",".join(scopes)
    ))

    conn.commit()
    conn.close()

def save_to_mysql(service, client_id, client_secret, access_token, refresh_token, scopes):
    conn = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="your_db"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            client_id TEXT,
            client_secret TEXT,
            access_token TEXT,
            refresh_token TEXT,
            scopes TEXT
        )
    """)

    cur.execute("""
        INSERT INTO tokens (timestamp, service, client_id, client_secret, access_token, refresh_token, scopes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.now().isoformat(),
        service,
        client_id,
        client_secret,
        access_token,
        refresh_token,
        ",".join(scopes)
    ))

    conn.commit()
    conn.close()