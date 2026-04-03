import csv
from datetime import datetime

class ConversationHistory:
    def __init__(self):
        self.history = []

    def add(self, user, agent):
        self.history.append({"user": user, "agent": agent, "timestamp": datetime.now().isoformat()})

    def save(self, path):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "user", "agent"])
            writer.writeheader()
            writer.writerows(self.history)

    def load(self, path):
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            self.history = list(reader)

    def __str__(self):
        return "\n".join(f"[{h['timestamp']}] User: {h['user']}\nAgent: {h['agent']}" for h in self.history)

def export_device_readings_to_csv(readings, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "device", "value"])
        for r in readings:
            writer.writerow([r["timestamp"], r["device"], r["value"]])
