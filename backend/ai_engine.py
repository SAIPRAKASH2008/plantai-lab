"""
AI Engine Module
Simulated AI engine for plant tissue culture optimization.
Provides media formulation, growth stage analysis, anomaly detection,
and nutrient adjustment recommendations.
"""

import random
import time
import math
from datetime import datetime


class AIEngine:
    """Simulated AI engine for tissue culture optimization."""

    # Base media formulations (MS medium variants) in mg/L
    MEDIA_BASES = {
        'MS': {
            'NH4NO3': 1650, 'KNO3': 1900, 'CaCl2': 440,
            'MgSO4': 370, 'KH2PO4': 170, 'sucrose': 30000,
            'agar': 8000,
        },
        'Half-MS': {
            'NH4NO3': 825, 'KNO3': 950, 'CaCl2': 220,
            'MgSO4': 185, 'KH2PO4': 85, 'sucrose': 30000,
            'agar': 8000,
        },
        'B5': {
            'KNO3': 2500, 'CaCl2': 150, 'MgSO4': 250,
            'NaH2PO4': 150, 'sucrose': 20000, 'agar': 8000,
        },
    }

    # Growth regulator ranges (mg/L) by stage
    GROWTH_REGULATORS = {
        'callus_induction': {
            'auxin_2,4-D': (0.5, 3.0),
            'cytokinin_BAP': (0.1, 1.0),
            'gibberellin_GA3': (0, 0),
        },
        'shoot_multiplication': {
            'auxin_IAA': (0.1, 0.5),
            'cytokinin_BAP': (1.0, 5.0),
            'gibberellin_GA3': (0, 0.5),
        },
        'root_regeneration': {
            'auxin_IBA': (0.5, 2.0),
            'cytokinin_BAP': (0, 0),
            'gibberellin_GA3': (0, 0),
        },
        'hardening': {
            'auxin_IBA': (0, 0.1),
            'cytokinin_BAP': (0, 0),
            'gibberellin_GA3': (0, 0.1),
        },
    }

    SPECIES_PROFILES = {
        'Solanum tuberosum': {
            'name': 'Potato',
            'preferred_media': 'MS',
            'optimal_temp': 25,
            'photoperiod': 16,
            'auxin_sensitivity': 0.8,
            'cytokinin_sensitivity': 1.2,
        },
        'Musa acuminata': {
            'name': 'Banana',
            'preferred_media': 'MS',
            'optimal_temp': 27,
            'photoperiod': 16,
            'auxin_sensitivity': 1.0,
            'cytokinin_sensitivity': 1.5,
        },
        'Vanilla planifolia': {
            'name': 'Vanilla',
            'preferred_media': 'Half-MS',
            'optimal_temp': 26,
            'photoperiod': 12,
            'auxin_sensitivity': 0.6,
            'cytokinin_sensitivity': 0.9,
        },
        'Dendrobium nobile': {
            'name': 'Orchid',
            'preferred_media': 'Half-MS',
            'optimal_temp': 24,
            'photoperiod': 14,
            'auxin_sensitivity': 0.5,
            'cytokinin_sensitivity': 1.0,
        },
        'Stevia rebaudiana': {
            'name': 'Stevia',
            'preferred_media': 'MS',
            'optimal_temp': 25,
            'photoperiod': 16,
            'auxin_sensitivity': 0.7,
            'cytokinin_sensitivity': 1.1,
        },
        'Curcuma longa': {
            'name': 'Turmeric',
            'preferred_media': 'MS',
            'optimal_temp': 28,
            'photoperiod': 16,
            'auxin_sensitivity': 1.1,
            'cytokinin_sensitivity': 0.8,
        },
        'Zingiber officinale': {
            'name': 'Ginger',
            'preferred_media': 'MS',
            'optimal_temp': 28,
            'photoperiod': 14,
            'auxin_sensitivity': 1.0,
            'cytokinin_sensitivity': 0.9,
        },
        'Rosa damascena': {
            'name': 'Rose',
            'preferred_media': 'MS',
            'optimal_temp': 24,
            'photoperiod': 16,
            'auxin_sensitivity': 0.9,
            'cytokinin_sensitivity': 1.3,
        },
        'Bambusa vulgaris': {
            'name': 'Bamboo',
            'preferred_media': 'MS',
            'optimal_temp': 26,
            'photoperiod': 16,
            'auxin_sensitivity': 1.2,
            'cytokinin_sensitivity': 1.0,
        },
    }

    def __init__(self):
        self._recommendation_cache = {}
        self._dispensing_log = []

    def get_species_list(self):
        """Return list of supported species."""
        return [
            {'scientific_name': k, 'common_name': v['name']}
            for k, v in self.SPECIES_PROFILES.items()
        ]

    def optimize_media(self, species, stage, custom_params=None):
        """Generate AI-optimized media formulation for given species and stage."""
        profile = self.SPECIES_PROFILES.get(species)
        if not profile:
            profile = list(self.SPECIES_PROFILES.values())[0]

        base_media = self.MEDIA_BASES[profile['preferred_media']]
        stage_key = stage.lower().replace(' ', '_')
        regulators = self.GROWTH_REGULATORS.get(stage_key, self.GROWTH_REGULATORS['callus_induction'])

        # AI-optimized concentrations based on species sensitivity
        optimized_regulators = {}
        for reg_name, (low, high) in regulators.items():
            if 'auxin' in reg_name:
                sensitivity = profile['auxin_sensitivity']
            elif 'cytokinin' in reg_name:
                sensitivity = profile['cytokinin_sensitivity']
            else:
                sensitivity = 1.0

            optimal = round((low + high) / 2 * sensitivity + self._ai_adjustment(reg_name), 3)
            optimal = max(low, min(high, optimal))
            optimized_regulators[reg_name] = {
                'concentration': round(optimal, 2),
                'unit': 'mg/L',
                'range': [low, high],
            }

        confidence = round(random.uniform(88, 99), 1)

        return {
            'species': species,
            'common_name': profile['name'],
            'stage': stage,
            'base_medium': profile['preferred_media'],
            'base_components': base_media,
            'growth_regulators': optimized_regulators,
            'environmental': {
                'temperature': profile['optimal_temp'],
                'photoperiod': profile['photoperiod'],
                'light_intensity': 3000,
            },
            'ai_confidence': confidence,
            'optimization_notes': self._generate_notes(species, stage, confidence),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

    def _ai_adjustment(self, regulator_name):
        """Simulate AI fine-tuning adjustment."""
        return random.gauss(0, 0.1)

    def _generate_notes(self, species, stage, confidence):
        """Generate contextual AI notes."""
        notes = []
        profile = self.SPECIES_PROFILES.get(species, {})
        name = profile.get('name', species)

        if 'callus' in stage.lower():
            notes.append(f"Optimized 2,4-D concentration for {name} callus initiation based on 847 historical cultures.")
            notes.append("Recommend subculturing at 21-day intervals for maximum proliferation rate.")
        elif 'shoot' in stage.lower():
            notes.append(f"BAP concentration elevated for {name} — species shows strong cytokinin response.")
            notes.append("Monitor for hyperhydricity if shoot multiplication exceeds 8× per cycle.")
        elif 'root' in stage.lower():
            notes.append(f"IBA pulse treatment recommended for {name} root initiation.")
            notes.append("Half-strength MS salts will improve root quality and reduce callusing at base.")
        elif 'hardening' in stage.lower():
            notes.append(f"Gradual humidity reduction protocol recommended for {name} acclimatization.")
            notes.append("Transfer to hydroponic module at 70% relative humidity for optimal survival rate.")

        if confidence > 95:
            notes.append("⚡ High confidence — formulation matches top 5% of successful cultures in database.")
        else:
            notes.append("📊 Consider running a small pilot batch to validate before scale-up.")

        return notes

    def get_recommendations(self, sensor_data=None):
        """Generate AI recommendations based on current system state."""
        recommendations = []
        now = datetime.now()

        # General recommendations that cycle
        all_recs = [
            {
                'id': 'rec-001',
                'priority': 'high',
                'category': 'Media Optimization',
                'title': 'Adjust Cytokinin Ratio for Vessel V-003',
                'description': 'Growth rate in V-003 has plateaued. AI analysis suggests increasing BAP from 2.0 to 3.5 mg/L to stimulate lateral shoot formation.',
                'action': 'Update media formulation',
                'confidence': 94.2,
            },
            {
                'id': 'rec-002',
                'priority': 'critical',
                'category': 'Contamination Alert',
                'title': 'Possible Fungal Contamination in V-007',
                'description': 'Image analysis detected irregular growth pattern with 87% probability of fungal contamination. Immediate isolation recommended.',
                'action': 'Isolate and inspect',
                'confidence': 87.3,
            },
            {
                'id': 'rec-003',
                'priority': 'medium',
                'category': 'Environmental Control',
                'title': 'Temperature Optimization for Chamber 2',
                'description': 'Orchid cultures in Chamber 2 would benefit from a 1°C temperature reduction. Current 26°C exceeds optimal range for Dendrobium.',
                'action': 'Adjust thermostat',
                'confidence': 91.7,
            },
            {
                'id': 'rec-004',
                'priority': 'low',
                'category': 'Scheduling',
                'title': 'Subculture Window for V-001, V-005',
                'description': 'Potato cultures V-001 and V-005 are approaching optimal subculture timing (day 21). Schedule transfer within the next 48 hours.',
                'action': 'Schedule subculture',
                'confidence': 96.5,
            },
            {
                'id': 'rec-005',
                'priority': 'medium',
                'category': 'Hydroponics',
                'title': 'pH Drift Detected in Nutrient Reservoir',
                'description': 'pH trending above 6.5 over the last 4 hours. Auto-correction initiated but manual verification recommended.',
                'action': 'Verify pH probe',
                'confidence': 89.1,
            },
            {
                'id': 'rec-006',
                'priority': 'high',
                'category': 'Growth Analysis',
                'title': 'Root Initiation Detected in V-009',
                'description': 'AI image analysis confirms root primordia formation in Stevia cultures. Recommend transfer to rooting medium within 5 days.',
                'action': 'Prepare rooting medium',
                'confidence': 92.8,
            },
        ]

        # Return a rotating subset
        cycle = int(time.time() / 30) % len(all_recs)
        count = min(4, len(all_recs))
        indices = [(cycle + i) % len(all_recs) for i in range(count)]
        for idx in indices:
            rec = all_recs[idx].copy()
            rec['timestamp'] = now.strftime('%H:%M:%S')
            recommendations.append(rec)

        return sorted(recommendations, key=lambda r: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}.get(r['priority'], 4))

    def dispense_media(self, species, stage, volume_ml=500):
        """Simulate media dispensing operation."""
        formulation = self.optimize_media(species, stage)
        entry = {
            'id': f'DISP-{len(self._dispensing_log)+1:04d}',
            'species': species,
            'stage': stage,
            'volume_ml': volume_ml,
            'formulation': formulation,
            'status': 'completed',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'duration_seconds': random.randint(30, 120),
        }
        self._dispensing_log.append(entry)
        return entry

    def get_dispensing_log(self):
        """Return dispensing history."""
        return list(reversed(self._dispensing_log[-20:]))

    def get_anomaly_alerts(self):
        """Generate simulated anomaly detection alerts."""
        alerts = [
            {
                'id': 'alert-001',
                'severity': 'warning',
                'type': 'Environmental',
                'message': 'Humidity spike detected in Chamber 1 — exceeded 95% for 12 minutes',
                'vessel': 'Chamber 1',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'resolved': False,
            },
            {
                'id': 'alert-002',
                'severity': 'info',
                'type': 'Growth',
                'message': 'V-004 Banana culture showing accelerated shoot multiplication (3.2×/week)',
                'vessel': 'V-004',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'resolved': False,
            },
            {
                'id': 'alert-003',
                'severity': 'critical',
                'type': 'Contamination',
                'message': 'Bacterial contamination confirmed in V-011 — auto-quarantine activated',
                'vessel': 'V-011',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'resolved': False,
            },
        ]
        # Return a subset based on time
        cycle = int(time.time() / 60) % 3
        return alerts[:cycle+1]

    def get_protocols(self):
        """Return shared protocol library."""
        return [
            {
                'id': 'proto-001',
                'title': 'High-Efficiency Potato Micropropagation',
                'author': 'Dr. A. Sharma — ICAR Lab, Delhi',
                'species': 'Solanum tuberosum',
                'success_rate': 94.5,
                'description': 'Optimized MS + 3mg/L BAP protocol achieving 12× multiplication rate per 21-day cycle.',
                'shared_date': '2026-08-10',
                'downloads': 234,
                'rating': 4.8,
            },
            {
                'id': 'proto-002',
                'title': 'Orchid Meristem Culture Protocol',
                'author': 'Prof. K. Tanaka — Tokyo AgriTech',
                'species': 'Dendrobium nobile',
                'success_rate': 88.2,
                'description': 'Half-MS based protocol with activated charcoal for virus-free orchid propagation.',
                'shared_date': '2026-07-28',
                'downloads': 156,
                'rating': 4.6,
            },
            {
                'id': 'proto-003',
                'title': 'Banana Somatic Embryogenesis',
                'author': 'Dr. M. Okonkwo — IITA, Nigeria',
                'species': 'Musa acuminata',
                'success_rate': 82.7,
                'description': 'Scalable somatic embryogenesis protocol for commercial banana cultivar production.',
                'shared_date': '2026-08-05',
                'downloads': 189,
                'rating': 4.5,
            },
            {
                'id': 'proto-004',
                'title': 'Stevia Mass Propagation via Nodal Cuttings',
                'author': 'Dr. L. García — CIAT, Colombia',
                'species': 'Stevia rebaudiana',
                'success_rate': 91.3,
                'description': 'Rapid multiplication protocol using nodal segments with 8× multiplication per cycle.',
                'shared_date': '2026-08-15',
                'downloads': 98,
                'rating': 4.7,
            },
            {
                'id': 'proto-005',
                'title': 'Rose Shoot Tip Culture for Disease Elimination',
                'author': 'Dr. F. Müller — Wageningen University',
                'species': 'Rosa damascena',
                'success_rate': 86.9,
                'description': 'Thermotherapy + meristem tip culture for producing virus-free Rosa damascena planting material.',
                'shared_date': '2026-07-20',
                'downloads': 312,
                'rating': 4.9,
            },
        ]

    def get_connected_labs(self):
        """Return simulated connected lab data."""
        return [
            {'id': 'lab-001', 'name': 'ICAR Tissue Culture Lab', 'location': 'New Delhi, India', 'lat': 28.61, 'lng': 77.23, 'status': 'online', 'active_cultures': 45, 'researchers': 8},
            {'id': 'lab-002', 'name': 'Tokyo AgriTech Center', 'location': 'Tokyo, Japan', 'lat': 35.68, 'lng': 139.69, 'status': 'online', 'active_cultures': 32, 'researchers': 5},
            {'id': 'lab-003', 'name': 'IITA Biotech Lab', 'location': 'Ibadan, Nigeria', 'lat': 7.38, 'lng': 3.94, 'status': 'offline', 'active_cultures': 28, 'researchers': 6},
            {'id': 'lab-004', 'name': 'CIAT Plant Bio Lab', 'location': 'Cali, Colombia', 'lat': 3.45, 'lng': -76.53, 'status': 'online', 'active_cultures': 37, 'researchers': 7},
            {'id': 'lab-005', 'name': 'Wageningen Phytolab', 'location': 'Wageningen, Netherlands', 'lat': 51.97, 'lng': 5.67, 'status': 'online', 'active_cultures': 52, 'researchers': 10},
        ]


    def get_live_vision_data(self, vessel_id='V-001'):
        """Simulate real-time computer vision analysis feed for culture vessel."""
        random.seed(hash(vessel_id) + int(time.time() / 5))  # Smooth fluctuations every 5s

        shoot_count = random.randint(6, 18)
        root_length = round(random.uniform(12.0, 45.0), 1)
        leaf_area = round(random.uniform(120.0, 520.0), 1)
        ndvi = round(random.uniform(0.72, 0.94), 2)
        height_mm = round(random.uniform(25.0, 85.0), 1)

        # AI Object Detection Bounding Boxes
        boxes = [
            {'label': 'Shoot Primordia', 'confidence': 0.94, 'x': 32, 'y': 28, 'w': 24, 'h': 30, 'type': 'shoot'},
            {'label': 'Active Apical Meristem', 'confidence': 0.98, 'x': 54, 'y': 18, 'w': 20, 'h': 22, 'type': 'shoot'},
            {'label': 'Root Primordium', 'confidence': 0.91, 'x': 42, 'y': 68, 'w': 18, 'h': 26, 'type': 'root'},
            {'label': 'Healthy Leaf Tissue', 'confidence': 0.96, 'x': 20, 'y': 45, 'w': 35, 'h': 25, 'type': 'leaf'},
        ]

        if 'V-007' in vessel_id or 'V-011' in vessel_id:
            boxes.append({'label': 'Anomaly: Fungal Halo', 'confidence': 0.88, 'x': 68, 'y': 52, 'w': 22, 'h': 22, 'type': 'anomaly'})

        random.seed()  # reset seed

        return {
            'vessel_id': vessel_id,
            'fps': 30,
            'status': 'LIVE STREAM',
            'shoot_count': shoot_count,
            'root_length_mm': root_length,
            'leaf_area_mm2': leaf_area,
            'ndvi_index': ndvi,
            'height_mm': height_mm,
            'bounding_boxes': boxes,
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
        }


# Global AI engine instance
ai_engine = AIEngine()
