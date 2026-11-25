"""SQLite 持久化：保存检查记录，供历史查询。"""

import os
import sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE, "instance")
DB_PATH = os.path.join(DB_DIR, "checks.db")


def _conn():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                org_name TEXT,
                org_code TEXT,
                scene TEXT,
                result TEXT,
                photo_count INTEGER,
                detail TEXT,
                created_at TEXT
            )
            """
        )


def save_check(*, check_type, org_name, org_code, scene, result, photo_count, detail):
    with _conn() as conn:
        cur = conn.execute(
            """INSERT INTO checks
               (type, org_name, org_code, scene, result, photo_count, detail, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                check_type,
                org_name,
                org_code,
                scene,
                result,
                photo_count,
                detail,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        return cur.lastrowid


def list_checks(limit=20):
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM checks ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def stats():
    with _conn() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM checks").fetchone()["c"]
        passed = conn.execute(
            "SELECT COUNT(*) AS c FROM checks WHERE result='pass'"
        ).fetchone()["c"]
        anomaly = conn.execute(
            "SELECT COUNT(*) AS c FROM checks WHERE result='anomaly'"
        ).fetchone()["c"]
        return {"total": total, "pass": passed, "anomaly": anomaly}
