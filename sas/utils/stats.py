import matplotlib.pyplot as plt
import io
from database.db import Database

db = Database()

def generate_stats_graph():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT region, COUNT(*) FROM accounts GROUP BY region")
        data = cursor.fetchall()
        regions = [row[0] for row in data]
        counts = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.bar(regions, counts)
    plt.title("Accounts by Region")
    plt.xlabel("Region")
    plt.ylabel("Number of Accounts")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf