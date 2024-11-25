CREATE TABLE Event (
    EventID INTEGER PRIMARY KEY,
    EventName TEXT NOT NULL
);

CREATE TABLE Objects (
    ObjectID INTEGER PRIMARY KEY,
    EventID INTEGER,
    ObjectName TEXT NOT NULL,
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
);

CREATE TABLE Purchases (
    PurchaseID INTEGER PRIMARY KEY,
    PurchaseName TEXT NOT NULL,
    PaymentID INTEGER,
    ObjectID INTEGER,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID),
    FOREIGN KEY (ObjectID) REFERENCES Objects(ObjectID)
);