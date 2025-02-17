# streamlit_app.py
import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file="database.db"):
        self.db_path = Path(__file__).parent / db_file
        self.connection = None

    def connect(self):
        """Kapcsolódás az adatbázishoz"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            return self.connection
        except sqlite3.Error as e:
            st.error(f"Hiba történt a kapcsolódás során: {e}")
            return None

    def init_db(self):
        """Adatbázis inicializálása"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                st.success("Adatbázis sikeresen inicializálva")
        except sqlite3.Error as e:
            st.error(f"Hiba az adatbázis inicializálása során: {e}")

    def add_user(self, username, email):
        """Felhasználó hozzáadása"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email) VALUES (?, ?)",
                    (username, email)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            st.error(f"Hiba a felhasználó hozzáadása során: {e}")
            return None

    def get_all_users(self):
        """Összes felhasználó lekérése"""
        try:
            with self.connect() as conn:
                return pd.read_sql_query("SELECT * FROM users", conn)
        except sqlite3.Error as e:
            st.error(f"Hiba a felhasználók lekérése során: {e}")
            return pd.DataFrame()

    def delete_user(self, user_id):
        """Felhasználó törlése"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            st.error(f"Hiba a felhasználó törlése során: {e}")
            return False

# Streamlit alkalmazás
def main():
    st.title("SQLite3 Felhasználókezelő Alkalmazás")
    
    # Adatbáziskezelő inicializálása
    db = DatabaseManager()
    db.init_db()
    
    # Oldalsáv - Új felhasználó hozzáadása
    st.sidebar.header("Új felhasználó hozzáadása")
    with st.sidebar.form("new_user_form"):
        username = st.text_input("Felhasználónév")
        email = st.text_input("Email cím")
        submit_button = st.form_submit_button("Felhasználó hozzáadása")
        
        if submit_button:
            if username and email:
                if db.add_user(username, email):
                    st.success(f"Felhasználó sikeresen hozzáadva: {username}")
            else:
                st.warning("Kérlek töltsd ki mindkét mezőt!")

    # Főoldal - Felhasználók listázása
    st.header("Felhasználók listája")
    users_df = db.get_all_users()
    
    if not users_df.empty:
        # DataFrame megjelenítése
        st.dataframe(users_df)
        
        # Felhasználó törlése
        st.header("Felhasználó törlése")
        user_to_delete = st.selectbox(
            "Válaszd ki a törölni kívánt felhasználót",
            users_df['id'].tolist(),
            format_func=lambda x: f"{x} - {users_df[users_df['id'] == x]['username'].iloc[0]}"
        )
        
        if st.button("Törlés"):
            if db.delete_user(user_to_delete):
                st.success("Felhasználó sikeresen törölve!")
                st.experimental_rerun()
    else:
        st.info("Még nincsenek felhasználók az adatbázisban.")

    # Statisztikák megjelenítése
    if not users_df.empty:
        st.header("Statisztikák")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Összes felhasználó", len(users_df))
        
        with col2:
            latest_user = users_df.iloc[-1]
            st.metric("Legutóbbi regisztráció", latest_user['username'])

if __name__ == "__main__":
    main()
