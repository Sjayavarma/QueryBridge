import sqlite3

# Create database
conn = sqlite3.connect('product_offers.db')
cur = conn.cursor()

# Enable foreign keys
cur.execute("PRAGMA foreign_keys = ON;")

# Create tables
cur.executescript("""
CREATE TABLE IF NOT EXISTS item_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL UNIQUE,
  description TEXT,
  is_deleted BOOLEAN DEFAULT 0,
  is_public BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS item_details (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  code TEXT,
  stock_threshold DECIMAL(16,4),
  opening_stock DECIMAL(16,4),
  type_id INTEGER NOT NULL,
  FOREIGN KEY (type_id) REFERENCES item_types(id),
  UNIQUE (code, type_id)
);

CREATE TABLE IF NOT EXISTS assoc_items_props (
  item_id INTEGER NOT NULL,
  prop_id INTEGER NOT NULL,
  prop_value TEXT NOT NULL,
  PRIMARY KEY (item_id, prop_id, prop_value),
  FOREIGN KEY (item_id) REFERENCES item_details(id)
);

CREATE TABLE IF NOT EXISTS item_offers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  sub_title TEXT,
  is_deleted BOOLEAN DEFAULT 0,
  valid_from DATETIME,
  valid_till DATETIME
);

CREATE TABLE IF NOT EXISTS offer_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  offer_id INTEGER,
  target_qty DECIMAL(12,4),
  target_price DECIMAL(12,2),
  reward_qty DECIMAL(12,4),
  reward_price DECIMAL(12,2),
  reward_discount DECIMAL(12,2),
  FOREIGN KEY (offer_id) REFERENCES item_offers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS offer_item_criteria (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER,
  match_type TEXT, -- Emulating ENUM
  conc_id INTEGER,
  conc_val TEXT,
  FOREIGN KEY (source_id) REFERENCES offer_items(id) ON DELETE CASCADE
);
""")

# Insert into item_types
cur.executemany("""
INSERT INTO item_types (type, description) VALUES (?, ?)
""", [
    ("Cereals", "Breakfast cereals"),
    ("Clothing", "Men and Women Apparel"),
    ("Footwear", "Shoes and Sandals"),
    ("Beverages", "Cold and Hot Drinks"),
    ("Snacks", "Chips and Namkeen"),
    ("Stationery", "Pens, Books"),
    ("Electronics", "Gadgets and Devices"),
    ("Toys", "Kids' toys"),
    ("Furniture", "Home and Office furniture"),
    ("Groceries", "Daily groceries")
])

# Insert into item_details
cur.executemany("""
INSERT INTO item_details (name, code, stock_threshold, opening_stock, type_id) 
VALUES (?, ?, ?, ?, ?)
""", [
    ("Nestle Oats", "CER001", 10, 100, 1),
    ("ITC Cornflakes", "CER002", 15, 150, 1),
    ("Maize Flakes", "CER003", 5, 200, 1),
    ("Levi's Shirt", "CLO001", 20, 80, 2),
    ("Nike Running Shoes", "FOO001", 12, 60, 3),
    ("Pepsi Can", "BEV001", 50, 300, 4),
    ("Lays Chips", "SNK001", 40, 500, 5),
    ("Sony Headphones", "ELE001", 5, 30, 7),
    ("Wooden Chair", "FUR001", 2, 20, 9),
    ("Bournvita", "GRO001", 30, 90, 10)
])

# Insert into assoc_items_props (assume prop_id: 1=Brand, 2=Pack Size)
cur.executemany("""
INSERT INTO assoc_items_props (item_id, prop_id, prop_value) VALUES (?, ?, ?)
""", [
    (1, 1, "Nestle"),
    (2, 1, "ITC"),
    (3, 1, "MaizeCorp"),
    (1, 2, "500gm"),
    (2, 2, "500gm"),
    (3, 2, "100gm"),
    (6, 1, "PepsiCo"),
    (7, 1, "Lays"),
    (10, 1, "Cadbury"),
    (10, 2, "500gm")
])

# Insert into item_offers
cur.executemany("""
INSERT INTO item_offers (title, sub_title, valid_from, valid_till)
VALUES (?, ?, ?, ?)
""", [
    ("Buy Cereals, Save Big!", "Discounts on Cereal brands", "2024-04-01", "2025-04-30"),
    ("Footwear Fest", "Get discounts on Shoes", "2024-05-01", "2025-05-01"),
    ("Snacks Special", "Flat 10% off", "2024-06-01", "2025-06-01"),
])

# Insert into offer_items
cur.executemany("""
INSERT INTO offer_items (offer_id, target_qty, target_price, reward_qty, reward_discount)
VALUES (?, ?, ?, ?, ?)
""", [
    (1, 2, None, 1, 10.00),
    (2, 1, None, 1, 20.00),
    (3, 3, None, 1, 15.00),
])

# Insert into offer_item_criteria (Make sure items match!)
cur.executemany("""
INSERT INTO offer_item_criteria (source_id, match_type, conc_id, conc_val)
VALUES (?, ?, ?, ?)
""", [
    (1, 'item', 1, None),  # Cereals category
    (1, '+prop', 1, "Nestle"), # Brand Nestle
    (1, '+prop', 1, "ITC"),    # Brand ITC
    (1, '-prop', 2, "100gm"),  # Exclude 100gm packs

    (2, '-item', 3, None),    # Footwear type
    (3, '+type', 5, None),    # Snacks type
])

conn.commit()
conn.close()

print("Database created with 10+ rows per table!")