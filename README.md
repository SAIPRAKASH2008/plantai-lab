# PlantAI Lab - Project Structure

## Directories

- **backend/** — Python Flask application, AI engine, database, sensors, face auth
- **frontend/** — Placeholder (templates & static assets not present in source attachments)
- **readme/** — Documentation and implementation guides

## Backend files
- app.py              — Flask web application
- ai_engine.py        — AI media optimization & recommendations
- database.py         — SQLite persistence layer
- face_auth.py        — Biometric face recognition
- sensor_simulator.py — Simulated sensor data
- plant_lab.db        — SQLite database
- requirements.txt    — Python dependencies
- .gitignore
- pyvenv.cfg

## Running
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Server starts at http://localhost:5000

Demo credentials:
- admin / plantai
- operator / culture123

