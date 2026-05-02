import psycopg2
from datetime import datetime

class DBManager:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="snake_db", 
                user="postgres", 
                password="1234", 
                host="localhost"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"DB Error: {e}")

    def get_player_id(self, username):
        self.cursor.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (username,))
        self.cursor.execute("SELECT id FROM players WHERE username = %s;", (username,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def save_game(self, player_id, score, level):
        self.cursor.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
            (player_id, score, level)
        )
        self.conn.commit()

    def get_leaderboard(self):
        self.cursor.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at 
            FROM game_sessions g JOIN players p ON g.player_id = p.id 
            ORDER BY g.score DESC LIMIT 10;
        """)
        return self.cursor.fetchall()

    def get_best_score(self, player_id):
        self.cursor.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s;", (player_id,))
        res = self.cursor.fetchone()[0]
        return res if res else 0