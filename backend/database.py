"""
Database Module for Plant Tissue Culture & Hydroponics System
SQLite persistence layer for vessels, dispensing history, sensor telemetry,
protocols, labs, and anomaly alerts.
"""

import sqlite3
import json
import os
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = os.path.join(os.path.dirname(__file__), 'plant_lab.db')


def get_db_connection():
    """Establish connection to SQLite database with Row factory."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed default data if empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Vessels Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vessels (
                id TEXT PRIMARY KEY,
                species TEXT NOT NULL,
                common_name TEXT,
                stage TEXT NOT NULL,
                stage_index INTEGER DEFAULT 0,
                progress REAL DEFAULT 0.0,
                growth_rate REAL DEFAULT 1.0,
                contamination_risk REAL DEFAULT 0.0,
                days_in_culture INTEGER DEFAULT 1,
                health_score REAL DEFAULT 95.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Dispensing Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dispensing_logs (
                id TEXT PRIMARY KEY,
                species TEXT NOT NULL,
                stage TEXT NOT NULL,
                volume_ml INTEGER NOT NULL,
                formulation_json TEXT NOT NULL,
                status TEXT DEFAULT 'completed',
                duration_seconds INTEGER DEFAULT 45,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 3. Sensor Telemetry Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,  -- 'tissue_culture' or 'hydroponics'
                parameter TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. Protocols Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protocols (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                species TEXT NOT NULL,
                success_rate REAL DEFAULT 85.0,
                description TEXT,
                downloads INTEGER DEFAULT 0,
                rating REAL DEFAULT 4.5,
                shared_date DATE DEFAULT CURRENT_DATE
            )
        ''')

        # 5. Connected Labs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connected_labs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                lat REAL,
                lng REAL,
                status TEXT DEFAULT 'online',
                active_cultures INTEGER DEFAULT 0,
                researchers INTEGER DEFAULT 0
            )
        ''')

        # 6. Alerts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                severity TEXT NOT NULL,  -- 'critical', 'warning', 'info'
                type TEXT NOT NULL,
                message TEXT NOT NULL,
                vessel_id TEXT,
                resolved INTEGER DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 7. Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'operator',
                face_signature TEXT,
                enrollment_status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

        # Run migrations to add enrollment_status if it doesn't exist
        try:
            cursor.execute('SELECT enrollment_status FROM users LIMIT 1')
        except sqlite3.OperationalError:
            cursor.execute('ALTER TABLE users ADD COLUMN enrollment_status TEXT NOT NULL DEFAULT \"pending\"')
            conn.commit()

    # Seed data if tables are empty
    _seed_initial_data()


def _seed_initial_data():
    """Seed sample data if empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?), (?, ?, ?, ?)
            ''', (
                'admin', generate_password_hash('plantai'), 'Administrator', 'admin',
                'operator', generate_password_hash('culture123'), 'Plant Operator', 'operator'
            ))

        # Seed Vessels
        cursor.execute('SELECT COUNT(*) FROM vessels')
        if cursor.fetchone()[0] == 0:
            sample_vessels = [
                ('V-001', 'Solanum tuberosum', 'Potato', 'Inoculation', 0, 15.5, 1.2, 1.2, 5, 96.4),
                ('V-002', 'Solanum tuberosum', 'Potato', 'Callus Induction', 1, 45.0, 1.8, 2.1, 14, 94.0),
                ('V-003', 'Musa acuminata', 'Banana', 'Shoot Multiplication', 2, 78.2, 2.5, 4.5, 22, 88.5),
                ('V-004', 'Musa acuminata', 'Banana', 'Shoot Multiplication', 2, 82.0, 3.1, 1.8, 25, 97.2),
                ('V-005', 'Vanilla planifolia', 'Vanilla', 'Callus Induction', 1, 35.0, 0.9, 3.2, 18, 91.0),
                ('V-006', 'Dendrobium nobile', 'Orchid', 'Root Regeneration', 3, 62.0, 1.4, 0.8, 30, 95.8),
                ('V-007', 'Dendrobium nobile', 'Orchid', 'Callus Induction', 1, 40.0, 1.1, 14.5, 12, 72.0),
                ('V-008', 'Stevia rebaudiana', 'Stevia', 'Hardening', 4, 91.5, 2.8, 0.5, 38, 98.1),
                ('V-009', 'Stevia rebaudiana', 'Stevia', 'Root Regeneration', 3, 55.0, 2.2, 1.0, 26, 93.4),
                ('V-010', 'Curcuma longa', 'Turmeric', 'Shoot Multiplication', 2, 70.0, 2.0, 2.8, 20, 89.6),
                ('V-011', 'Zingiber officinale', 'Ginger', 'Callus Induction', 1, 28.0, 0.8, 18.2, 9, 65.2),
                ('V-012', 'Rosa damascena', 'Rose', 'Inoculation', 0, 10.0, 1.5, 0.2, 3, 99.0),
            ]
            cursor.executemany('''
                INSERT INTO vessels (id, species, common_name, stage, stage_index, progress, growth_rate, contamination_risk, days_in_culture, health_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_vessels)

        # Seed Protocols
        cursor.execute('SELECT COUNT(*) FROM protocols')
        if cursor.fetchone()[0] == 0:
            sample_protocols = [
                ('proto-001', 'High-Efficiency Potato Micropropagation', 'Dr. A. Sharma — ICAR Lab', 'Solanum tuberosum', 94.5, 'Optimized MS + 3mg/L BAP protocol achieving 12× multiplication rate.', 234, 4.8, '2026-08-10'),
                ('proto-002', 'Orchid Meristem Culture Protocol', 'Prof. K. Tanaka — Tokyo AgriTech', 'Dendrobium nobile', 88.2, 'Half-MS based protocol with activated charcoal for virus-free propagation.', 156, 4.6, '2026-07-28'),
                ('proto-003', 'Banana Somatic Embryogenesis', 'Dr. M. Okonkwo — IITA', 'Musa acuminata', 82.7, 'Scalable somatic embryogenesis protocol for commercial banana cultivars.', 189, 4.5, '2026-08-05'),
                ('proto-004', 'Stevia Mass Propagation via Nodal Cuttings', 'Dr. L. García — CIAT', 'Stevia rebaudiana', 91.3, 'Rapid multiplication protocol using nodal segments with 8× multiplication.', 98, 4.7, '2026-08-15'),
                ('proto-005', 'Rose Shoot Tip Culture', 'Dr. F. Müller — Wageningen', 'Rosa damascena', 86.9, 'Thermotherapy + meristem tip culture for virus-free rose planting material.', 312, 4.9, '2026-07-20'),
            ]
            cursor.executemany('''
                INSERT INTO protocols (id, title, author, species, success_rate, description, downloads, rating, shared_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_protocols)

        # Seed Connected Labs
        cursor.execute('SELECT COUNT(*) FROM connected_labs')
        if cursor.fetchone()[0] == 0:
            sample_labs = [
                ('lab-001', 'ICAR Tissue Culture Lab', 'New Delhi, India', 28.61, 77.23, 'online', 45, 8),
                ('lab-002', 'Tokyo AgriTech Center', 'Tokyo, Japan', 35.68, 139.69, 'online', 32, 5),
                ('lab-003', 'IITA Biotech Lab', 'Ibadan, Nigeria', 7.38, 3.94, 'offline', 28, 6),
                ('lab-004', 'CIAT Plant Bio Lab', 'Cali, Colombia', 3.45, -76.53, 'online', 37, 7),
                ('lab-005', 'Wageningen Phytolab', 'Wageningen, Netherlands', 51.97, 5.67, 'online', 52, 10),
            ]
            cursor.executemany('''
                INSERT INTO connected_labs (id, name, location, lat, lng, status, active_cultures, researchers)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_labs)

        conn.commit()


# ─── CRUD Functions ──────────────────────────────────────────────

def get_all_vessels():
    """Retrieve all culture vessels."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vessels ORDER BY id')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_vessel(vessel_data):
    """Add a new culture vessel."""
    v_id = vessel_data.get('id') or f"V-{(len(get_all_vessels()) + 1):03d}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vessels (id, species, common_name, stage, stage_index, progress, growth_rate, contamination_risk, days_in_culture, health_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            v_id,
            vessel_data.get('species', 'Unknown'),
            vessel_data.get('common_name', 'Plant'),
            vessel_data.get('stage', 'Inoculation'),
            vessel_data.get('stage_index', 0),
            vessel_data.get('progress', 0.0),
            vessel_data.get('growth_rate', 1.0),
            vessel_data.get('contamination_risk', 0.0),
            vessel_data.get('days_in_culture', 1),
            vessel_data.get('health_score', 95.0)
        ))
        conn.commit()
    return v_id


def update_vessel(vessel_id, update_fields):
    """Update fields of an existing vessel."""
    set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values())
    values.append(vessel_id)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE vessels SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
        conn.commit()
    return True


def delete_vessel(vessel_id):
    """Delete a culture vessel."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vessels WHERE id = ?", (vessel_id,))
        conn.commit()
    return True


def add_dispensing_log(log_data):
    """Record a new dispensing operation."""
    log_id = log_data.get('id') or f"DISP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    formulation_json = json.dumps(log_data.get('formulation', {}))
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dispensing_logs (id, species, stage, volume_ml, formulation_json, status, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_id,
            log_data.get('species'),
            log_data.get('stage'),
            log_data.get('volume_ml', 500),
            formulation_json,
            log_data.get('status', 'completed'),
            log_data.get('duration_seconds', 45)
        ))
        conn.commit()
    return log_id


def get_dispensing_logs(limit=20):
    """Fetch dispensing history."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dispensing_logs ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d['formulation'] = json.loads(d['formulation_json']) if d['formulation_json'] else {}
            result.append(d)
        return result


def add_protocol(protocol_data):
    """Add a new protocol to the shared library."""
    proto_id = protocol_data.get('id') or f"proto-{(len(get_protocols()) + 1):03d}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO protocols (id, title, author, species, success_rate, description, downloads, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            proto_id,
            protocol_data.get('title'),
            protocol_data.get('author'),
            protocol_data.get('species'),
            protocol_data.get('success_rate', 85.0),
            protocol_data.get('description', ''),
            protocol_data.get('downloads', 0),
            protocol_data.get('rating', 5.0)
        ))
        conn.commit()
    return proto_id


def get_protocols():
    """Fetch all shared protocols."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM protocols ORDER BY shared_date DESC')
        return [dict(r) for r in cursor.fetchall()]


def get_connected_labs():
    """Fetch connected lab network data."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM connected_labs')
        return [dict(r) for r in cursor.fetchall()]


def create_user(username, password, full_name='User', role='operator', face_signature=None):
    """Create a user record with a hashed password."""
    username_clean = (username or '').strip()
    if not username_clean:
        return None

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, full_name, role, face_signature)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                username_clean.lower(),
                generate_password_hash(password),
                full_name or 'User',
                role or 'operator',
                face_signature,
            ))
            conn.commit()
            return get_user_by_username(username_clean)
        except sqlite3.IntegrityError:
            return None


def get_user_by_username(username):
    """Fetch a user record by username."""
    key = (username or '').strip().lower()
    if not key:
        return None
    with get_db_connection() as conn:
        row = conn.execute('SELECT * FROM users WHERE username = ?', (key,)).fetchone()
        return dict(row) if row is not None else None


def authenticate_user(username, password):
    """Check username and password against the database."""
    user = get_user_by_username(username)
    if not user:
        return False
    return check_password_hash(user['password_hash'], password)


def update_user_face_signature(username, face_signature):
    """Persist a user face signature for biometric verification."""
    user = get_user_by_username(username)
    if not user:
        return False
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET face_signature = ?, enrollment_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE username = ?
        ''', (face_signature, 'enrolled', user['username']))
        conn.commit()
    return True


def get_all_users():
    """Retrieve all user accounts."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, full_name, role, enrollment_status, created_at FROM users ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]


def update_user_role(username, new_role):
    """Change a user role (admin/operator)."""
    user = get_user_by_username(username)
    if not user:
        return False
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET role = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?', (new_role, user['username']))
        conn.commit()
    return True


def delete_user(username):
    """Remove a user account."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
    return True


def log_telemetry(module, parameter, value, unit=''):
    """Record a sensor telemetry reading."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_telemetry (module, parameter, value, unit)
            VALUES (?, ?, ?, ?)
        ''', (module, parameter, value, unit))
        conn.commit()


# Initialize database on module load
init_db()
