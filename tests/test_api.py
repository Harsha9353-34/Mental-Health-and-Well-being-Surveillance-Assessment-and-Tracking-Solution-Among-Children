"""
MindBridge — Backend Test Suite.
Tests API endpoints, ML risk classification, NLP sentiment scoring,
SQLAlchemy database persistence, and distress alert logic.
"""

import os
import sys
import unittest
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from backend.main import app
from backend.database import Base, engine, SessionLocal
from backend.models import CheckIn


class MindBridgeBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    def setUp(self):
        # Clean test table between tests
        db = SessionLocal()
        db.query(CheckIn).delete()
        db.commit()
        db.close()

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model_loaded"])

    def test_submit_checkin_low_risk(self):
        payload = {
            "mood_score": 5,
            "mood_label": "😌 Calm",
            "sleep_hours": 9.0,
            "screen_time": 1.5,
            "physical_play": 2.0,
            "school_stress": 1,
            "journal_text": "I had a wonderful day playing with my friends at school!",
        }
        response = self.client.post("/api/checkin", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check ML prediction
        self.assertEqual(data["risk_tier"], 0)
        self.assertIn("Low Risk", data["risk_label"])
        self.assertGreater(data["confidence"], 0.5)

        # Check NLP sentiment
        self.assertGreater(data["sentiment"]["compound"], 0.2)
        self.assertEqual(data["sentiment"]["tone_tag"], "Positive")

        # Check DB record
        self.assertEqual(data["checkin"]["mood_score"], 5)
        self.assertEqual(data["checkin"]["sleep_hours"], 9.0)

    def test_submit_checkin_elevated_risk(self):
        payload = {
            "mood_score": 1,
            "mood_label": "😤 Frustrated",
            "sleep_hours": 4.0,
            "screen_time": 7.0,
            "physical_play": 0.0,
            "school_stress": 5,
            "journal_text": "I am feeling terribly hopeless and exhausted with all the exams.",
        }
        response = self.client.post("/api/checkin", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["risk_tier"], 2)
        self.assertIn("Elevated", data["risk_label"])
        self.assertLess(data["sentiment"]["compound"], -0.2)
        self.assertEqual(data["sentiment"]["tone_tag"], "Negative")

    def test_demo_seeding_and_dashboard_metrics(self):
        # Seed balanced scenario
        seed_resp = self.client.post("/api/seed-demo", json={"scenario": "balanced", "days": 14})
        self.assertEqual(seed_resp.status_code, 200)
        self.assertEqual(seed_resp.json()["seeded_count"], 14)

        # Check dashboard metrics
        dash_resp = self.client.get("/api/dashboard")
        self.assertEqual(dash_resp.status_code, 200)
        dash_data = dash_resp.json()
        self.assertEqual(dash_data["total_checkins"], 14)
        self.assertGreater(dash_data["avg_mood"], 3.0)
        self.assertFalse(dash_data["distress_alert"])

    def test_distress_alert_trigger(self):
        # Seed distress scenario where last 3 check-ins are elevated (Tier 2)
        seed_resp = self.client.post("/api/seed-demo", json={"scenario": "distress", "days": 14})
        self.assertEqual(seed_resp.status_code, 200)

        dash_resp = self.client.get("/api/dashboard")
        self.assertEqual(dash_resp.status_code, 200)
        dash_data = dash_resp.json()
        self.assertTrue(dash_data["distress_alert"])
        self.assertGreaterEqual(dash_data["consecutive_elevated"], 3)

    def test_diagnostics_endpoint(self):
        resp = self.client.get("/api/diagnostics")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("RandomForestClassifier", data["model_name"])
        self.assertGreaterEqual(data["cv_mean_accuracy"], 0.75)
        self.assertEqual(data["elevated_recall"], 1.0)
        self.assertIn("sleep_hours", data["feature_importances"])

    def test_sentiment_sandbox(self):
        resp = self.client.post("/api/sentiment/sandbox", json={"text": "I feel joyful, proud, and super excited!"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["tone_tag"], "Positive")
        self.assertGreater(data["compound"], 0.5)

    def test_crisis_resources(self):
        resp = self.client.get("/api/crisis-resources")
        self.assertEqual(resp.status_code, 200)
        resources = resp.json()
        self.assertGreaterEqual(len(resources), 3)
        names = [r["name"] for r in resources]
        self.assertTrue(any("Childline" in n for n in names))
        self.assertTrue(any("Tele-MANAS" in n for n in names))


if __name__ == "__main__":
    unittest.main()
