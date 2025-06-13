import yfinance as yf
import mysql.connector

# Step 1: DB Connection
db = mysql.connector.connect(
    host="localhost",      # update if different
    user="root",   # update
    password="",  # update
    database="myalgo_db"   # update
)
cursor = db.cursor()

# Step 2: Fetch tradingsymbols without yfinsymbol
cursor.execute("SELECT id, tradingsymbol FROM nse_data WHERE (yfinsymbol IS NULL OR yfinsymbol = '') and instrument_type = 'EQUITY' and exchange = 'NSE_EQ' and last_price > 50")
rows = cursor.fetchall()

def to_yfinance_symbol(nse_symbol):
    if not nse_symbol:
        return None
    nse_symbol = nse_symbol.strip().upper()
    return f"{nse_symbol}.NS"

def is_valid_yfinance_symbol(symbol):
    try:
        info = yf.Ticker(symbol).info
        return info.get("regularMarketPrice") is not None
    except Exception:
        return False

# Step 3: Check and update
for row in rows:
    row_id, tradingsymbol = row
    yfin_symbol = to_yfinance_symbol(tradingsymbol)
    if is_valid_yfinance_symbol(yfin_symbol):
        print(f"✅ {tradingsymbol} → {yfin_symbol}")
        cursor.execute("UPDATE nse_data SET yfinsymbol = %s WHERE id = %s", (yfin_symbol, row_id))
        db.commit()
    else:
        print(f"❌ {tradingsymbol} → {yfin_symbol} (Invalid)")

# Cleanup
cursor.close()
db.close()
