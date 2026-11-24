import re
from datetime import date, timedelta


class DateParser:
    WEEKDAYS = (
        "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday"
    )

    def __init__(self, today=None):
        self.today = today if today is not None else date.today()

    # Assume all years must be 4 chars
    # Feed the 4 digit year first, then the other two numbers
    # Assume month entered first, then day, but if that fails, try day then month
    def _make_date(self, year, first, second):
        try:
            return date(year, first, second)
        except ValueError:
            pass

        return date(year, second, first)

    def _fill_missing(self, year, month):
        return date(year, month, self.today.day)

    def _convert_year(self, year):
        if year < 50:
            return 2000 + year
        else:
            return 1900 + year

    def parse(self, text):
        text = text.strip().lower()

        if text in self.WEEKDAYS:
            return self.get_date(text)

        # Atleast 2 numbers with 1 seperator required to be a valid date
        pattern = r"\d{1,4}(?:\s*[-/.\\]\s*\d{1,4}){1,2}"

        if not re.fullmatch(pattern, text):
            raise ValueError(f"Unrecognized date: {text!r}")

        parts = re.split(r"\s*[-/.\\]\s*", text)

        if len(parts) == 2:
            a, b = parts

            if len(a) == 4:
                return self._fill_missing(int(a), int(b))

            if len(b) == 4:
                return self._fill_missing(int(b), int(a))

            try:
                return self._make_date(
                    self.today.year, int(a), int(b)
                )
            except ValueError:
                pass

            if 1 <= int(a) <= 12 and len(b) == 2:
                year = self._convert_year(int(b))
                return self._fill_missing(year, int(a))

            raise ValueError(f"Invalid date: {text!r}")

        if len(parts) == 3:
            a, b, c = parts

            # Year is not likely to be the middle number 
            # We only check if first or last number is 4 digits
            if len(a) == 4 and len(b) <= 2 and len(c) <= 2:
                return self._make_date(
                    int(a), int(b), int(c)
                )

            if len(c) == 4 and len(a) <= 2 and len(b) <= 2:
                return self._make_date(
                    int(c), int(a), int(b)
                )

            if len(a) <= 2 and len(b) <= 2 and len(c) <= 2:
                year = self._convert_year(int(c))

                return self._make_date(
                    year, int(a), int(b)
                )

            raise ValueError(
                "Year must have four digits and be first or last"
            )

    def get_weekday(self, text):
        return self.parse(text).strftime("%A")

    # Returns weekday date for the current week    
    def get_date(self, weekday):
        weekday = weekday.strip().lower()

        if weekday not in self.WEEKDAYS:
            raise ValueError(f"Invalid weekday: {weekday}")

        target = self.WEEKDAYS.index(weekday)
        current = self.today.weekday()

        days_difference = target - current

        return self.today + timedelta(days=days_difference)

    # Returns a list of dates found in the text
    def find_dates(self, text):
        pattern = (
            r"(?<![\w/\\-])"
            r"\d{1,4}(?:\s*[-/.\\]\s*\d{1,4}){1,2}"
            r"(?![\w/\\-]|\.\d)"
            r"|\b(?:monday|tuesday|wednesday|thursday|"
            r"friday|saturday|sunday)\b"
        )

        results = []

        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                parsed_date = self.parse(match.group())
                results.append(parsed_date)
            except ValueError:
                pass

        return results
