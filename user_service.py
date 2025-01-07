import json
import os

FILE = "./user_list.json"


def load_data():
    """Lädt die Benutzer-Daten aus der JSON-Datei."""
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as file:
        return json.load(file)


def save_data(data):
    """Speichert die Benutzer-Daten in die JSON-Datei."""
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)


def create(obj):
    """Fügt einen neuen Benutzer hinzu."""
    data = load_data()
    data.append(obj)
    save_data(data)


def read_cr(cr_id):
    """Liest einen Benutzer basierend auf der Clash Royale-ID."""
    return next((user for user in load_data() if user["cr_id"] == cr_id), None)


def read_dc(dc_id):
    """Liest einen Benutzer basierend auf der Discord-ID."""
    return next((user for user in load_data() if user["dc_id"] == dc_id), None)


def delete(dc_id):
    """Löscht einen Benutzer basierend auf der Discord-ID."""
    data = load_data()
    updated_data = [user for user in data if user["dc_id"] != dc_id]
    save_data(updated_data)
