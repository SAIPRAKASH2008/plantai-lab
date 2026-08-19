"""
AI-Based Accelerated Plant Tissue Culture and Hydroponics System
Flask Web Application Backend
Integrated with SQLite Persistence Layer
"""

from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from sensor_simulator import simulator
from ai_engine import ai_engine
import database as db
from face_auth import compute_face_signature, verify_face_match, serialize_face_signature, deserialize_face_signature

import os
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')
)
app.secret_key = 'plantai-lab-secret-key-change-me'


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        user = db.get_user_by_username(session.get('username', ''))
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required.'}), 403
        return view_func(*args, **kwargs)
    return wrapped_view


def enrollment_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        user = db.get_user_by_username(session.get('username', ''))
        if user and user.get('enrollment_status') == 'enrolled':
            return redirect(url_for('dashboard'))
        return view_func(*args, **kwargs)
    return wrapped_view


@app.before_request
def require_authentication():
    allowed_routes = {'login', 'logout', 'register', 'static', 'api_register'}
    if request.endpoint in allowed_routes:
        return None
    if request.path.startswith('/api/'):
        if request.endpoint in {'api_facial_login', 'api_enroll_face'}:
            return None
        return None
    if session.get('locked'):
        if request.endpoint not in {'lock_screen', 'logout'}:
            return redirect(url_for('lock_screen'))
    if not session.get('logged_in'):
        return redirect(url_for('login'))


# ─── Authentication Routes ────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Display login page and authenticate users."""
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if db.authenticate_user(username, password):
            session['logged_in'] = True
            session['username'] = username.lower()
            return redirect(url_for('dashboard'))

        error = 'Invalid username or password.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """End the current user session."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User self-registration page with role selection."""
    error = None
    admin_code_required = True

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', 'operator').strip()
        admin_code = request.form.get('admin_code', '').strip()

        if not username or not password or not full_name:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif role not in ['admin', 'operator']:
            error = 'Invalid role selected.'
        elif role == 'admin' and admin_code != 'PLANTAI2026':
            error = 'Invalid admin invitation code.'
        else:
            user = db.create_user(username, password, full_name, role)
            if user:
                session['logged_in'] = True
                session['username'] = username.lower()
                return redirect(url_for('enroll_face'))
            else:
                error = 'Username already exists.'

    return render_template('register.html', error=error, admin_code_required=admin_code_required)


@app.route('/enroll', methods=['GET', 'POST'])
@login_required
def enroll_face():
    """Face enrollment for biometric verification."""
    username = session.get('username', '')
    user = db.get_user_by_username(username)

    if not user:
        return redirect(url_for('logout'))

    if user.get('enrollment_status') == 'enrolled':
        return redirect(url_for('dashboard'))

    return render_template('enroll_face.html', username=user.get('full_name'))


@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin panel for user management."""
    users = db.get_all_users()
    current_user = db.get_user_by_username(session.get('username', ''))
    return render_template('admin_users.html', users=users, current_user=current_user)


@app.route('/lock')
@login_required
def lock_screen():
    """Show the locked system screen requiring facial verification."""
    session['locked'] = True
    return render_template('lock.html')


@app.route('/api/lock-system', methods=['POST'])
@login_required
def api_lock_system():
    """Lock the system from the dashboard until face verification passes."""
    session['locked'] = True
    return jsonify({'status': 'locked'})


@app.route('/api/face-verify', methods=['POST'])
@login_required
def api_face_verify():
    """Mark the current user as successfully face-verified and unlock the system."""
    session['locked'] = False
    session['face_verified'] = True
    return jsonify({'status': 'verified', 'user': session.get('username', 'admin')})


@app.route('/api/facial-login', methods=['POST'])
def api_facial_login():
    """Allow camera-based login using the standard username/password credentials."""
    username = request.form.get('username', '').strip() or 'admin'
    password = request.form.get('password', '')
    face_image = request.form.get('face_image')

    if not db.authenticate_user(username, password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    user = db.get_user_by_username(username)
    if face_image:
        try:
            signature = compute_face_signature(face_image)
            stored_signature = deserialize_face_signature(user.get('face_signature')) if user and user.get('face_signature') else None
            if stored_signature and verify_face_match(face_image, stored_signature):
                session['logged_in'] = True
                session['username'] = username.lower()
                session['locked'] = False
                session['face_verified'] = True
                return jsonify({'status': 'ok', 'redirect': url_for('dashboard')})
            if not stored_signature:
                db.update_user_face_signature(username, serialize_face_signature(signature))
                session['logged_in'] = True
                session['username'] = username.lower()
                session['locked'] = False
                session['face_verified'] = True
                return jsonify({'status': 'ok', 'redirect': url_for('dashboard')})
            return jsonify({'error': 'Face verification failed.'}), 401
        except Exception:
            return jsonify({'error': 'Face verification failed.'}), 401

    session['logged_in'] = True
    session['username'] = username.lower()
    session['locked'] = False
    session['face_verified'] = True
    return jsonify({'status': 'ok', 'redirect': url_for('dashboard')})


@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for user registration with role selection."""
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password', '')
    full_name = (data.get('full_name') or '').strip()
    role = (data.get('role') or 'operator').strip()
    admin_code = (data.get('admin_code') or '').strip()

    if not username or not password or not full_name:
        return jsonify({'error': 'Missing required fields'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if role not in ['admin', 'operator']:
        return jsonify({'error': 'Invalid role'}), 400

    if role == 'admin' and admin_code != 'PLANTAI2026':
        return jsonify({'error': 'Invalid admin invitation code'}), 403

    user = db.create_user(username, password, full_name, role)
    if user:
        return jsonify({'status': 'ok', 'user_id': user.get('id'), 'role': role}), 201
    return jsonify({'error': 'Username already exists'}), 409


@app.route('/api/enroll-face', methods=['POST'])
@login_required
def api_enroll_face():
    """API endpoint to capture and store face signature during enrollment."""
    username = session.get('username')
    face_image = request.form.get('face_image')

    if not face_image:
        return jsonify({'error': 'No face image provided'}), 400

    try:
        signature = compute_face_signature(face_image)
        db.update_user_face_signature(username, serialize_face_signature(signature))
        return jsonify({'status': 'enrolled', 'message': 'Face signature captured successfully'})
    except Exception as e:
        return jsonify({'error': f'Face enrollment failed: {str(e)}'}), 400


@app.route('/api/admin/users/<username>/role', methods=['PUT'])
@admin_required
def api_update_user_role(username):
    """API endpoint to update user role."""
    if session.get('username') == username:
        return jsonify({'error': 'Cannot modify own role'}), 400

    data = request.get_json() or {}
    new_role = data.get('role', '').strip()

    if new_role not in ['admin', 'operator']:
        return jsonify({'error': 'Invalid role'}), 400

    if db.update_user_role(username, new_role):
        return jsonify({'status': 'ok', 'message': f'User {username} role updated to {new_role}'})
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/admin/users/<username>', methods=['DELETE'])
@admin_required
def api_delete_user(username):
    """API endpoint to delete a user."""
    if session.get('username') == username:
        return jsonify({'error': 'Cannot delete own account'}), 400

    if db.delete_user(username):
        return jsonify({'status': 'ok', 'message': f'User {username} deleted'})
    return jsonify({'error': 'User not found'}), 404


# ─── Page Routes ────────────────────────────────────────────────

@app.route('/')
@login_required
def dashboard():
    """Main dashboard overview."""
    return render_template('dashboard.html', active_page='dashboard')


@app.route('/media-dispensing')
@login_required
def media_dispensing():
    """AI media dispensing control panel."""
    species_list = ai_engine.get_species_list()
    return render_template('media_dispensing.html', active_page='media', species_list=species_list)


@app.route('/growth-monitor')
@login_required
def growth_monitor():
    """Growth monitoring and analytics."""
    return render_template('growth_monitor.html', active_page='growth')


@app.route('/hydroponics')
@login_required
def hydroponics():
    """Hydroponic acclimatization module."""
    return render_template('hydroponics.html', active_page='hydroponics')


@app.route('/collaboration')
@login_required
def collaboration():
    """Networking and collaboration hub."""
    return render_template('collaboration.html', active_page='collaboration')


# ─── Sensor & Growth Data Endpoints ────────────────────────────

@app.route('/api/sensor-data/tissue-culture')
def api_tc_sensors():
    """Return tissue culture sensor readings and record to DB."""
    data = simulator.get_tissue_culture_sensors()
    # Log telemetry
    db.log_telemetry('tissue_culture', 'temperature', data['temperature']['value'], '°C')
    db.log_telemetry('tissue_culture', 'humidity', data['humidity']['value'], '%')
    return jsonify(data)


@app.route('/api/sensor-data/hydroponics')
def api_hydro_sensors():
    """Return hydroponic sensor readings and record to DB."""
    data = simulator.get_hydroponic_sensors()
    db.log_telemetry('hydroponics', 'ph', data['ph']['value'], 'pH')
    db.log_telemetry('hydroponics', 'ec', data['ec']['value'], 'mS/cm')
    return jsonify(data)


@app.route('/api/growth-data')
def api_growth_data():
    """Return growth monitoring data for vessels (from DB)."""
    vessels = db.get_all_vessels()
    if not vessels:
        vessels = simulator.get_growth_data()
    return jsonify(vessels)


@app.route('/api/trend-data/<param>')
def api_trend_data(param):
    """Return historical trend data for a parameter."""
    points = request.args.get('points', 24, type=int)
    return jsonify(simulator.get_trend_data(param, points))


# ─── Vessel Management CRUD ─────────────────────────────────────

@app.route('/api/vessels', methods=['GET', 'POST'])
def api_vessels():
    """List all vessels or create a new culture vessel."""
    if request.method == 'POST':
        vessel_data = request.get_json()
        if not vessel_data or not vessel_data.get('species'):
            return jsonify({'error': 'Missing required species'}), 400
        v_id = db.add_vessel(vessel_data)
        return jsonify({'message': 'Vessel created successfully', 'id': v_id}), 201
    return jsonify(db.get_all_vessels())


@app.route('/api/vessels/<vessel_id>', methods=['GET', 'PUT', 'DELETE'])
def api_vessel_detail(vessel_id):
    """Get, update, or delete a specific vessel."""
    if request.method == 'PUT':
        update_data = request.get_json()
        db.update_vessel(vessel_id, update_data)
        return jsonify({'message': f'Vessel {vessel_id} updated successfully'})
    elif request.method == 'DELETE':
        db.delete_vessel(vessel_id)
        return jsonify({'message': f'Vessel {vessel_id} deleted successfully'})
    else:
        vessels = [v for v in db.get_all_vessels() if v['id'] == vessel_id]
        if not vessels:
            return jsonify({'error': 'Vessel not found'}), 404
        return jsonify(vessels[0])


# ─── AI & Media Dispensing Endpoints ───────────────────────────

@app.route('/api/ai-recommendations')
def api_recommendations():
    """Return current AI recommendations."""
    return jsonify(ai_engine.get_recommendations())


@app.route('/api/live-plant-vision/<vessel_id>')
def api_live_plant_vision(vessel_id):
    """Return real-time AI computer vision analysis payload for culture vessel."""
    return jsonify(ai_engine.get_live_vision_data(vessel_id))


@app.route('/api/anomaly-alerts')
def api_anomaly_alerts():
    """Return anomaly detection alerts."""
    return jsonify(ai_engine.get_anomaly_alerts())


@app.route('/api/optimize-media', methods=['POST'])
def api_optimize_media():
    """Get AI-optimized media formulation."""
    data = request.get_json() or {}
    species = data.get('species', 'Solanum tuberosum')
    stage = data.get('stage', 'callus_induction')
    result = ai_engine.optimize_media(species, stage)
    return jsonify(result)


@app.route('/api/dispense', methods=['POST'])
def api_dispense():
    """Trigger media dispensing and persist in DB log."""
    data = request.get_json() or {}
    species = data.get('species', 'Solanum tuberosum')
    stage = data.get('stage', 'callus_induction')
    volume = data.get('volume', 500)
    result = ai_engine.dispense_media(species, stage, volume)
    # Store in database
    db.add_dispensing_log(result)
    return jsonify(result)


@app.route('/api/dispensing-log')
def api_dispensing_log():
    """Return dispensing history from DB."""
    db_logs = db.get_dispensing_logs()
    if not db_logs:
        db_logs = ai_engine.get_dispensing_log()
    return jsonify(db_logs)


# ─── Protocols & Labs Endpoints ───────────────────────────────

@app.route('/api/protocols', methods=['GET', 'POST'])
def api_protocols():
    """Fetch shared protocols or add a new protocol."""
    if request.method == 'POST':
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': 'Title required'}), 400
        p_id = db.add_protocol(data)
        return jsonify({'message': 'Protocol shared successfully', 'id': p_id}), 201
    return jsonify(db.get_protocols())


@app.route('/api/connected-labs')
def api_connected_labs():
    """Return connected lab network data."""
    labs = db.get_connected_labs()
    if not labs:
        labs = ai_engine.get_connected_labs()
    return jsonify(labs)


# ─── Hardware IoT Ingestion API ──────────────────────────────

@app.route('/api/telemetry', methods=['POST'])
def api_telemetry_ingest():
    """IoT Endpoint: Allows physical sensors/microcontrollers (ESP32, Raspberry Pi, Arduino) to post sensor readings."""
    data = request.get_json() or {}
    module = data.get('module', 'tissue_culture')
    parameter = data.get('parameter')
    value = data.get('value')
    unit = data.get('unit', '')

    if not parameter or value is None:
        return jsonify({'error': 'parameter and value are required'}), 400

    db.log_telemetry(module, parameter, float(value), unit)
    return jsonify({'status': 'recorded', 'timestamp': data.get('timestamp')}), 201


@app.route('/api/export-data')
def api_export_data():
    """Export system state, vessels, dispensing logs, and protocols as JSON."""
    return jsonify({
        'vessels': db.get_all_vessels(),
        'dispensing_logs': db.get_dispensing_logs(limit=100),
        'protocols': db.get_protocols(),
        'connected_labs': db.get_connected_labs(),
        'system_status': 'operational',
    })


@app.route('/api/system-status')
def api_system_status():
    """Return overall system status."""
    tc = simulator.get_tissue_culture_sensors()
    hydro = simulator.get_hydroponic_sensors()
    vessels = db.get_all_vessels()
    alerts = ai_engine.get_anomaly_alerts()

    active_vessels = len([v for v in vessels if v['progress'] > 10])
    avg_health = round(sum(v['health_score'] for v in vessels) / len(vessels), 1) if vessels else 0
    critical_alerts = len([a for a in alerts if a['severity'] == 'critical'])

    return jsonify({
        'tissue_culture': {
            'status': 'critical' if critical_alerts > 0 else 'operational',
            'active_vessels': active_vessels,
            'total_vessels': len(vessels),
            'avg_health_score': avg_health,
        },
        'hydroponics': {
            'status': 'operational',
            'ph': hydro['ph']['value'],
            'ec': hydro['ec']['value'],
        },
        'ai_engine': {
            'status': 'active',
            'model_version': '2.4.1',
            'last_analysis': tc['timestamp'],
            'recommendations_pending': len(ai_engine.get_recommendations()),
        },
        'alerts': {
            'total': len(alerts),
            'critical': critical_alerts,
        },
        'environment': {
            'temperature': tc['temperature']['value'],
            'humidity': tc['humidity']['value'],
        },
    })


if __name__ == '__main__':
    print("\n[+] AI Plant Tissue Culture & Hydroponics Backend Server")
    print("    Database: SQLite (plant_lab.db)")
    print("    Starting server at http://localhost:5000\n")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
