-- schema.sql
-- Adatbázis séma létrehozása

-- Meglévő táblák törlése (ha léteznek)
DROP TABLE IF EXISTS users;

-- Felhasználók tábla
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexek létrehozása a gyakran keresett mezőkre
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);

-- Alap jogok beállítása (opcionális)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON users TO 'app_user';

-- Kezdeti teszt adatok (development környezethez)
INSERT INTO users (username, email) VALUES 
    ('test_user1', 'test1@example.com'),
    ('test_user2', 'test2@example.com');

-- Megjegyzések:
-- 1. A TIMESTAMP típus SQLite-ban TEXT-ként tárolódik
-- 2. Az AUTOINCREMENT biztosítja az egyedi ID-ket
-- 3. A NOT NULL és UNIQUE megszorítások segítenek az adatintegritás megőrzésében
