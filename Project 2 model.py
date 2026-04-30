import json
from pathlib import Path

PRIMARY_OPTIONS = [
    "beach",
    "nature_hiking",
    "city_culture",
    "food_nightlife",
    "ski_snow",
    "relaxing",
    "romantic",
]


class VacationModel:
    def __init__(self, data_file):
        self.data_file = Path(data_file)
        self.data = self.load_database()

    def load_database(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_options(self):
        seasons = ["spring", "summer", "fall", "winter"]
        secondary_activities = set()
        for spot in self.data:
            for tag in spot.get("secondary_tags", []):
                if tag:
                    secondary_activities.add(tag)
        return {
            "seasons": seasons,
            "primary_activities": PRIMARY_OPTIONS,
            "secondary_activities": sorted(secondary_activities),
        }

    def find_best_match(self, season, primary_value, secondary_values, wants_us, target_temp):
        candidates = []
        for spot in self.data:
            if spot.get("primary_activity") != primary_value:
                continue
            if bool(spot.get("is_us")) != wants_us:
                continue

            season_temp = spot.get("temps_f", {}).get(season)
            if season_temp is None:
                continue

            temp_diff = abs(season_temp - target_temp)
            if temp_diff > 10:
                continue

            secondary_matches = len(set(secondary_values) & set(spot.get("secondary_tags", [])))
            score = secondary_matches * 20 - temp_diff

            candidates.append({
                "spot": spot,
                "score": score,
                "temp_diff": temp_diff,
                "secondary_matches": secondary_matches,
                "matched_temp": season_temp,
            })

        if not candidates:
            return None

        candidates.sort(
            key=lambda x: (-x["secondary_matches"], x["temp_diff"], -x["score"], x["spot"]["name"])
        )
        return candidates[0]
