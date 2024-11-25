import sqlite3
from typing import Tuple, Optional

class Database:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS Event (
                    EventID INTEGER PRIMARY KEY,
                    EventName TEXT NOT NULL
                );
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS Objects (
                    ObjectID INTEGER PRIMARY KEY,
                    EventID INTEGER,
                    ObjectName TEXT NOT NULL,
                    FOREIGN KEY (EventID) REFERENCES Event(EventID)
                );
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS Purchases (
                    PurchaseID INTEGER PRIMARY KEY,
                    PurchaseName TEXT NOT NULL,
                    PaymentID INTEGER,
                    ObjectID INTEGER,
                    Quantity INTEGER NOT NULL,
                    FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID),
                    FOREIGN KEY (ObjectID) REFERENCES Objects(ObjectID)
                );
            ''')

    def create_event(self, event_name: str) -> int:
        with self.connection:
            cursor = self.connection.execute('INSERT INTO Event (EventName) VALUES (?)', (event_name,))
            return cursor.lastrowid

    def read_event(self, event_id: int) -> Optional[Tuple[int, str]]:
        cursor = self.connection.execute('SELECT * FROM Event WHERE EventID = ?', (event_id,))
        return cursor.fetchone()

    def update_event(self, event_id: int, event_name: str) -> None:
        with self.connection:
            self.connection.execute('UPDATE Event SET EventName = ? WHERE EventID = ?', (event_name, event_id))

    def delete_event(self, event_id: int) -> None:
        with self.connection:
            self.connection.execute('DELETE FROM Event WHERE EventID = ?', (event_id,))

    def create_object(self, event_id: int, object_name: str) -> int:
        with self.connection:
            cursor = self.connection.execute('INSERT INTO Objects (EventID, ObjectName) VALUES (?, ?)', (event_id, object_name))
            return cursor.lastrowid

    def read_object(self, object_id: int) -> Optional[Tuple[int, int, str]]:
        cursor = self.connection.execute('SELECT * FROM Objects WHERE ObjectID = ?', (object_id,))
        return cursor.fetchone()

    def update_object(self, object_id: int, event_id: int, object_name: str) -> None:
        with self.connection:
            self.connection.execute('UPDATE Objects SET EventID = ?, ObjectName = ? WHERE ObjectID = ?', (event_id, object_name, object_id))

    def delete_object(self, object_id: int) -> None:
        with self.connection:
            self.connection.execute('DELETE FROM Objects WHERE ObjectID = ?', (object_id,))

    def create_purchase(self, purchase_name: str, payment_id: int, object_id: int, quantity: int) -> int:
        with self.connection:
            cursor = self.connection.execute('INSERT INTO Purchases (PurchaseName, PaymentID, ObjectID, Quantity) VALUES (?, ?, ?, ?)', (purchase_name, payment_id, object_id, quantity))
            return cursor.lastrowid

    def read_purchase(self, purchase_id: int) -> Optional[Tuple[int, str, int, int, int]]:
        cursor = self.connection.execute('SELECT * FROM Purchases WHERE PurchaseID = ?', (purchase_id,))
        return cursor.fetchone()

    def update_purchase(self, purchase_id: int, purchase_name: str, payment_id: int, object_id: int, quantity: int) -> None:
        with self.connection:
            self.connection.execute('UPDATE Purchases SET PurchaseName = ?, PaymentID = ?, ObjectID = ?, Quantity = ? WHERE PurchaseID = ?', (purchase_name, payment_id, object_id, quantity, purchase_id))

    def delete_purchase(self, purchase_id: int) -> None:
        with self.connection:
            self.connection.execute('DELETE FROM Purchases WHERE PurchaseID = ?', (purchase_id,))

    def close(self):
        self.connection.close()