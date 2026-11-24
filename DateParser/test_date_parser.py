
import unittest
from datetime import date
from date_parser import DateParser


class TestDateParser(unittest.TestCase):
    def setUp(self):
        self.parser = DateParser(today=date(2026, 11, 2))

    # Different date orders
    def test_month_day_year(self):
        self.assertEqual(self.parser.parse("10/27/2028"), date(2028, 10, 27))

    def test_day_month_year(self):
        self.assertEqual(self.parser.parse("27/10/2028"), date(2028, 10, 27))

    def test_year_month_day(self):
        self.assertEqual(self.parser.parse("2028/10/27"), date(2028, 10, 27))

    def test_year_day_month(self):
        self.assertEqual(self.parser.parse("2028/27/10"), date(2028, 10, 27))

    # Missing date components
    def test_missing_year(self):
        self.assertEqual(self.parser.parse("10/27"), date(2026, 10, 27))

    def test_missing_day(self):
        self.assertEqual(self.parser.parse("2028/10"), date(2028, 10, 2))
        self.assertEqual(self.parser.parse("10/2028"), date(2028, 10, 2))

    # Ambiguous dates
    def test_ambiguous_dates(self):
        self.assertEqual(self.parser.parse("05/06"), date(2026, 5, 6))
        self.assertEqual(self.parser.parse("11/12"), date(2026, 11, 12))
        self.assertEqual(self.parser.parse("24/12"), date(2026, 12, 24))

    # Two-digit years
    def test_two_digit_years(self):
        self.assertEqual(self.parser.parse("5/6/26"), date(2026, 5, 6))
        self.assertEqual(self.parser.parse("24/12/26"), date(2026, 12, 24))
        self.assertEqual(self.parser.parse("11/23/75"), date(1975, 11, 23))

    def test_two_digit_year_boundaries(self):
        self.assertEqual(self.parser.parse("1/1/00"), date(2000, 1, 1))
        self.assertEqual(self.parser.parse("1/1/49"), date(2049, 1, 1))
        self.assertEqual(self.parser.parse("1/1/50"), date(1950, 1, 1))
        self.assertEqual(self.parser.parse("1/1/99"), date(1999, 1, 1))

    def test_two_part_month_year(self):
        self.assertEqual(self.parser.parse("10/49"), date(2049, 10, 2))
        self.assertEqual(self.parser.parse("10/75"), date(1975, 10, 2))

    # One-digit month and day
    def test_one_digit_month_and_day(self):
        self.assertEqual(self.parser.parse("1/5/26"), date(2026, 1, 5))
        self.assertEqual(self.parser.parse("2026/1/5"), date(2026, 1, 5))

    # Different separators and spaces
    def test_separators(self):
        self.assertEqual(self.parser.parse("10-27-2028"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("10.27.2028"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("10\\27\\2028"), date(2028, 10, 27))

    def test_spaces(self):
        self.assertEqual(self.parser.parse(" 10/27/2028 "), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("10 / 27 / 2028"), date(2028, 10, 27))

    # Leap years and invalid calendar dates
    def test_leap_year(self):
        self.assertEqual(self.parser.parse("02/29/2024"), date(2024, 2, 29))

    def test_invalid_dates(self):
        with self.assertRaises(ValueError):
            self.parser.parse("02/30/2028")
        with self.assertRaises(ValueError):
            self.parser.parse("02/29/2026")
        with self.assertRaises(ValueError):
            self.parser.parse("13/14/2028")
        with self.assertRaises(ValueError):
            self.parser.parse("00/00/2028")

    # Invalid text and unsupported formats
    def test_invalid_text(self):
        with self.assertRaises(ValueError):
            self.parser.parse("hello")
        with self.assertRaises(ValueError):
            self.parser.parse("today")
        with self.assertRaises(ValueError):
            self.parser.parse("")
        with self.assertRaises(ValueError):
            self.parser.parse("10/hello")

    def test_invalid_formats(self):
        with self.assertRaises(ValueError):
            self.parser.parse("27")
        with self.assertRaises(ValueError):
            self.parser.parse("2028")
        with self.assertRaises(ValueError):
            self.parser.parse("10/2028/27")
        with self.assertRaises(ValueError):
            self.parser.parse("10/27/2028/99")

    def test_no_day_year(self):
        with self.assertRaises(ValueError):
            self.parser.parse("2028/27")
        with self.assertRaises(ValueError):
            self.parser.parse("27/2028")

    # Weekday conversions
    def test_get_weekday(self):
        self.assertEqual(self.parser.get_weekday("10/27/2026"), "Tuesday")
        self.assertEqual(self.parser.get_weekday("02/29/2024"), "Thursday")

    def test_get_date(self):
        self.assertEqual(self.parser.get_date("Tuesday"), date(2026, 11, 3))
        self.assertEqual(self.parser.parse("Friday"), date(2026, 11, 6))

    def test_get_date_backward(self):
        parser = DateParser(today=date(2026, 11, 5))
        self.assertEqual(parser.get_date("Monday"), date(2026, 11, 2))

    def test_invalid_weekdays(self):
        with self.assertRaises(ValueError):
            self.parser.get_date("hello")
        with self.assertRaises(ValueError):
            self.parser.get_date("tues")

    # Finding dates inside longer text
    def test_find_single_date(self):
        self.assertEqual(
            self.parser.find_dates("Exam on 10/27"),
            [date(2026, 10, 27)]
        )

    def test_find_multiple_dates(self):
        self.assertEqual(
            self.parser.find_dates("Exam 10/27 and quiz 11/05"),
            [date(2026, 10, 27), date(2026, 11, 5)]
        )

    def test_find_weekday(self):
        self.assertEqual(
            self.parser.find_dates("Meeting on Tuesday"),
            [date(2026, 11, 3)]
        )

    def test_find_two_digit_year(self):
        self.assertEqual(
            self.parser.find_dates("Exam 11/23/26 and quiz 12/25/75."),
            [date(2026, 11, 23), date(1975, 12, 25)]
        )

    def test_find_punctuation(self):
        self.assertEqual(
            self.parser.find_dates("Exam 10/27."),
            [date(2026, 10, 27)]
        )
        self.assertEqual(
            self.parser.find_dates("Exam 10/27!"),
            [date(2026, 10, 27)]
        )
        self.assertEqual(
            self.parser.find_dates("Exam 10/27, meeting Tuesday."),
            [date(2026, 10, 27), date(2026, 11, 3)]
        )

    def test_find_invalid_or_no_dates(self):
        self.assertEqual(self.parser.find_dates("Deadline 02/30/2026"), [])
        self.assertEqual(self.parser.find_dates("Hello, I have 25 assignments"), [])

    # Missing day can be invalid in certain months
    def test_missing_day_invalid_for_month(self):
        parser = DateParser(today=date(2026, 1, 31))

        with self.assertRaises(ValueError):
            parser.parse("02/49")

        with self.assertRaises(ValueError):
            parser.parse("2028/02")


if __name__ == "__main__":
    unittest.main()
