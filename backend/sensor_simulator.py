"""
Sensor Simulator Module
Generates realistic simulated sensor data for the plant tissue culture
and hydroponics monitoring system.
"""

import random
import math
import time
from datetime import datetime, timedelta


class SensorSimulator:
    """Generates realistic sensor readings with natural fluctuations."""

    def __init__(self):
        self._start_time = time.time()
        self._history = {
            'temperature': [],
            'humidity': [],
            'light_intensity': [],
            'co2': [],
            'ph': [],
            'ec': [],
            'dissolved_oxygen': [],
        }
        self._max_history = 50

    def _wave(self, base, amplitude, period_seconds=3600):
        """Generate a sinusoidal fluctuation around a base value."""
        elapsed = time.time() - self._start_time
        return base + amplitude * math.sin(2 * math.pi * elapsed / period_seconds)

    def _noise(self, scale=1.0):
        """Add Gaussian noise."""
        return random.gauss(0, scale)

    def get_tissue_culture_sensors(self):
        """Return sensor readings for tissue culture chambers."""
        temp = round(self._wave(25.0, 1.5, 7200) + self._noise(0.3), 1)
        humidity = round(self._wave(85.0, 5.0, 5400) + self._noise(1.0), 1)
        humidity = max(60, min(100, humidity))
        light = round(self._wave(3000, 500, 43200) + self._noise(50), 0)
        light = max(0, light)
        co2 = round(self._wave(400, 50, 3600) + self._noise(10), 0)
        co2 = max(200, co2)

        data = {
            'temperature': {'value': temp, 'unit': '°C', 'min': 20, 'max': 30, 'optimal': [24, 26]},
            'humidity': {'value': humidity, 'unit': '%', 'min': 60, 'max': 100, 'optimal': [80, 90]},
            'light_intensity': {'value': light, 'unit': 'lux', 'min': 0, 'max': 5000, 'optimal': [2500, 3500]},
            'co2_level': {'value': co2, 'unit': 'ppm', 'min': 200, 'max': 600, 'optimal': [350, 450]},
            'timestamp': datetime.now().strftime('%H:%M:%S'),
        }
        return data

    def get_hydroponic_sensors(self):
        """Return sensor readings for the hydroponic module."""
        ph = round(self._wave(5.8, 0.4, 4800) + self._noise(0.05), 2)
        ph = max(4.0, min(8.0, ph))
        ec = round(self._wave(1.8, 0.3, 6000) + self._noise(0.05), 2)
        ec = max(0.5, min(3.5, ec))
        do = round(self._wave(7.0, 1.0, 3600) + self._noise(0.2), 1)
        do = max(4.0, min(10.0, do))
        water_temp = round(self._wave(22.0, 1.0, 7200) + self._noise(0.2), 1)
        flow_rate = round(self._wave(2.5, 0.5, 1800) + self._noise(0.1), 2)
        flow_rate = max(0.5, flow_rate)

        return {
            'ph': {'value': ph, 'unit': '', 'min': 4.0, 'max': 8.0, 'optimal': [5.5, 6.5]},
            'ec': {'value': ec, 'unit': 'mS/cm', 'min': 0.5, 'max': 3.5, 'optimal': [1.5, 2.5]},
            'dissolved_oxygen': {'value': do, 'unit': 'mg/L', 'min': 4.0, 'max': 10.0, 'optimal': [6.0, 8.0]},
            'water_temperature': {'value': water_temp, 'unit': '°C', 'min': 18, 'max': 28, 'optimal': [20, 24]},
            'flow_rate': {'value': flow_rate, 'unit': 'L/min', 'min': 0.5, 'max': 5.0, 'optimal': [2.0, 3.0]},
            'timestamp': datetime.now().strftime('%H:%M:%S'),
        }

    def get_growth_data(self):
        """Return simulated growth monitoring data for culture vessels."""
        stages = ['Inoculation', 'Callus Induction', 'Shoot Multiplication', 'Root Regeneration', 'Hardening']
        vessels = []
        random.seed(42)  # consistent vessel data within a session
        for i in range(12):
            stage_idx = (i + int(time.time() / 86400)) % len(stages)
            progress = round(((time.time() % 86400) / 86400) * 100 + random.uniform(-10, 10), 1)
            progress = max(5, min(98, progress))
            contamination_risk = round(random.uniform(0, 15) + self._noise(2), 1)
            contamination_risk = max(0, min(100, contamination_risk))
            growth_rate = round(random.uniform(0.5, 3.0) + self._noise(0.2), 2)
            growth_rate = max(0.1, growth_rate)

            vessels.append({
                'id': f'V-{i+1:03d}',
                'species': random.choice([
                    'Solanum tuberosum', 'Musa acuminata', 'Vanilla planifolia',
                    'Dendrobium nobile', 'Stevia rebaudiana', 'Curcuma longa',
                    'Zingiber officinale', 'Rosa damascena', 'Bambusa vulgaris',
                ]),
                'stage': stages[stage_idx],
                'stage_index': stage_idx,
                'progress': progress,
                'growth_rate': growth_rate,
                'contamination_risk': contamination_risk,
                'days_in_culture': random.randint(3, 45),
                'health_score': round(random.uniform(70, 99), 1),
            })
        random.seed()  # reset seed
        return vessels

    def get_trend_data(self, param='temperature', points=24):
        """Return historical trend data for charts."""
        now = datetime.now()
        data = []
        for i in range(points):
            t = now - timedelta(hours=points - i)
            elapsed_sim = (points - i) * 150  # simulate elapsed seconds
            if param == 'temperature':
                val = round(25.0 + 1.5 * math.sin(2 * math.pi * elapsed_sim / 7200) + random.gauss(0, 0.3), 1)
            elif param == 'humidity':
                val = round(85.0 + 5.0 * math.sin(2 * math.pi * elapsed_sim / 5400) + random.gauss(0, 1.0), 1)
            elif param == 'ph':
                val = round(5.8 + 0.4 * math.sin(2 * math.pi * elapsed_sim / 4800) + random.gauss(0, 0.05), 2)
            elif param == 'ec':
                val = round(1.8 + 0.3 * math.sin(2 * math.pi * elapsed_sim / 6000) + random.gauss(0, 0.05), 2)
            elif param == 'growth_rate':
                val = round(1.5 + 0.5 * math.sin(2 * math.pi * elapsed_sim / 10000) + random.gauss(0, 0.1), 2)
            else:
                val = round(random.uniform(0, 100), 1)
            data.append({
                'time': t.strftime('%H:%M'),
                'value': val,
            })
        return data


# Global simulator instance
simulator = SensorSimulator()
