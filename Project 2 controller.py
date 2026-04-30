from PyQt6.QtWidgets import QMessageBox


class AppController:
    def __init__(self, model, window):
        self.model = model
        self.window = window
        self.input_page = window.input_page
        self.result_page = window.result_page

        self.input_page.continue_button.clicked.connect(self.handle_find_location)
        self.result_page.back_button.clicked.connect(self.window.show_input_page)
        self.input_page.secondary_combo_1.currentIndexChanged.connect(self.ensure_unique_secondaries)
        self.input_page.secondary_combo_2.currentIndexChanged.connect(self.ensure_unique_secondaries)

    def normalize_label(self, text: str) -> str:
        return text.lower().replace(" ", "_").replace(".", "")

    def ensure_unique_secondaries(self):
        one = self.input_page.secondary_combo_1.currentText()
        two = self.input_page.secondary_combo_2.currentText()
        if one != "No preference" and one == two:
            sender = self.window.sender()
            other_name = "Secondary Activity #2" if sender == self.input_page.secondary_combo_2 else "Secondary Activity #1"
            QMessageBox.warning(
                self.window,
                "Duplicate secondary activity",
                f"Please choose a different value for {other_name}."
            )
            sender.blockSignals(True)
            sender.setCurrentIndex(0)
            sender.blockSignals(False)

    def handle_find_location(self):
        if self.input_page.primary_combo.currentIndex() == 0:
            QMessageBox.warning(self.window, "Missing primary activity", "Please select a primary activity before continuing.")
            return

        if self.input_page.region_group.checkedButton() is None:
            QMessageBox.warning(self.window, "Missing trip region", "Please choose either U.S. or International before continuing.")
            return

        season = self.input_page.season_combo.currentText().lower()
        primary_display = self.input_page.primary_combo.currentText()
        primary_value = self.normalize_label(primary_display)
        secondary_values = self.get_secondary_values()
        wants_us = self.input_page.us_radio.isChecked()
        target_temp = self.input_page.slider_temp()

        best = self.model.find_best_match(season, primary_value, secondary_values, wants_us, target_temp)

        review_text = self.build_review_text(season, primary_display, target_temp)
        location_text, description_text = self.build_result_text(best, secondary_values)

        self.result_page.show_result(review_text, location_text, description_text)
        self.window.show_result_page()

    def get_secondary_values(self):
        secondary_values = []
        for combo in (self.input_page.secondary_combo_1, self.input_page.secondary_combo_2):
            value = combo.currentText()
            if value != "No preference":
                secondary_values.append(self.normalize_label(value))
        return secondary_values

    def build_review_text(self, season, primary_display, target_temp):
        region = self.input_page.selected_region()
        sec1 = self.input_page.secondary_combo_1.currentText()
        sec2 = self.input_page.secondary_combo_2.currentText()
        return (
            f"Trip season: {season.title()}\n"
            f"Primary activity: {primary_display}\n"
            f"Secondary Activity #1: {sec1}\n"
            f"Secondary Activity #2: {sec2}\n"
            f"Trip region: {region}\n"
            f"Preferred average temperature: {target_temp:.1f}°F"
        )

    def build_result_text(self, best, secondary_values):
        if best is None:
            return (
                "Sorry, but we could not find a matching location from the database.",
                "Try adjusting your season, temperature, or secondary activity choices and search again."
            )

        location = best["spot"]
        secondary_line = "No secondary matches affected this result."
        if secondary_values:
            secondary_line = (
                f"Matched {best['secondary_matches']} of {len(secondary_values)} "
                f"selected secondary activities."
            )

        location_text = f"{location['name']}, {location['country']}"
        description_text = (location.get("description", "No description available.")
                + f"\n\nResult details: {secondary_line} "
                  f"Temperature difference: {best['temp_diff']:.1f}°F. "
                  f"Matched seasonal temperature: {best['matched_temp']:.1f}°F."
        )
        return location_text, description_text

    def build_result_text(self, best, secondary_values):
        if best is None:
            return (
                "Sorry, but we could not find a matching location from the database.",
                "Try adjusting your season, temperature, or secondary activity choices and search again."
            )

        location = best["spot"]
        secondary_line = "No secondary matches affected this result."
        if secondary_values:
            secondary_line = f"Matched {best['secondary_matches']} of {len(secondary_values)} selected secondary activities."

        location_text = f"{location['name']}, {location['country']}"
        description_text = (
            location.get("description", "No description available.")
            + f"Result details: {secondary_line} "
              f"Temperature difference: {best['temp_diff']:.1f}°F. "
              f"Matched seasonal temperature: {best['matched_temp']:.1f}°F."
        )
        return location_text, description_text
