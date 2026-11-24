
import unittest
from datetime import date
from date_parser import DateParser


class TestDateParser(unittest.TestCase):
    def setUp(self):
        self.parser = DateParser(today=date(2026, 11, 2))

    def test_month_day_year(self):
        self.assertEqual(self.parser.parse("10/27/2028"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("12/25/2026"), date(2026, 12, 25))

    def test_day_month_year(self):
        self.assertEqual(self.parser.parse("27/10/2028"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("25/12/2026"), date(2026, 12, 25))

    def test_year_month_day(self):
        self.assertEqual(self.parser.parse("2028/10/27"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("2026/12/25"), date(2026, 12, 25))

    def test_year_day_month(self):
        self.assertEqual(self.parser.parse("2028/27/10"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("2026/25/12"), date(2026, 12, 25))

    def test_missing_year(self):
        self.assertEqual(self.parser.parse("10/27"), date(2026, 10, 27))
        self.assertEqual(self.parser.parse("27/10"), date(2026, 10, 27))

    def test_missing_month_or_day(self):
        self.assertEqual(self.parser.parse("2028/10"), date(2028, 10, 2))
        self.assertEqual(self.parser.parse("2028/27"), date(2028, 11, 27))
        self.assertEqual(self.parser.parse("10/2028"), date(2028, 10, 2))

    def test_ambiguous_dates(self):
        self.assertEqual(self.parser.parse("05/06"), date(2026, 5, 6))
        self.assertEqual(self.parser.parse("11/12"), date(2026, 11, 12))
        self.assertEqual(self.parser.parse("06/05/2028"), date(2028, 6, 5))

    def test_different_separators(self):
        self.assertEqual(self.parser.parse("10-27-2028"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("10.27.2028"), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("10\\27\\2028"), date(2028, 10, 27))

    def test_spaces(self):
        self.assertEqual(self.parser.parse(" 10/27/2028 "), date(2028, 10, 27))
        self.assertEqual(self.parser.parse("10 / 27 / 2028"), date(2028, 10, 27))

    def test_leap_year(self):
        self.assertEqual(self.parser.parse("02/29/2024"), date(2024, 2, 29))
        self.assertEqual(self.parser.parse("29/02/2024"), date(2024, 2, 29))

    def test_invalid_dates(self):
        with self.assertRaises(ValueError):
            self.parser.parse("02/30/2028")
        with self.assertRaises(ValueError):
            self.parser.parse("02/29/2026")
        with self.assertRaises(ValueError):
            self.parser.parse("13/14/2028")
        with self.assertRaises(ValueError):
            self.parser.parse("00/00/2028")

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
            self.parser.parse("10/27/28")
        with self.assertRaises(ValueError):
            self.parser.parse("10/2028/27")
        with self.assertRaises(ValueError):
            self.parser.parse("10/27/2028/99")

    def test_get_weekday(self):
        self.assertEqual(self.parser.get_weekday("10/27/2026"), "Tuesday")
        self.assertEqual(self.parser.get_weekday("11/02/2026"), "Monday")
        self.assertEqual(self.parser.get_weekday("12/25/2026"), "Friday")

    def test_get_date(self):
        self.assertEqual(self.parser.get_date("Monday"), date(2026, 11, 2))
        self.assertEqual(self.parser.get_date("Tuesday"), date(2026, 11, 3))
        self.assertEqual(self.parser.get_date("Sunday"), date(2026, 11, 8))

    def test_weekday_in_parse(self):
        self.assertEqual(self.parser.parse("Tuesday"), date(2026, 11, 3))
        self.assertEqual(self.parser.parse("Friday"), date(2026, 11, 6))
        self.assertEqual(self.parser.parse("  MONDAY "), date(2026, 11, 2))

    def test_get_date_backward(self):
        parser = DateParser(today=date(2026, 11, 5))
        self.assertEqual(parser.get_date("Monday"), date(2026, 11, 2))
        self.assertEqual(parser.get_date("Tuesday"), date(2026, 11, 3))

    def test_invalid_weekdays(self):
        with self.assertRaises(ValueError):
            self.parser.get_date("hello")
        with self.assertRaises(ValueError):
            self.parser.get_date("Funday")
        with self.assertRaises(ValueError):
            self.parser.get_date("tues")

    # Tests for find_dates method
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

    def test_find_invalid_date(self):
        self.assertEqual(
            self.parser.find_dates("Deadline 02/30/2026"),
            []
        )

    def test_find_no_dates(self):
        self.assertEqual(
            self.parser.find_dates("Hello, I have 25 assignments"),
            []
        )

    def test_date_followed_by_period(self):
        self.assertEqual(
            self.parser.find_dates("Exam 10/27."),
            [date(2026, 10, 27)]
        )

    def test_date_followed_by_comma(self):
        self.assertEqual(
            self.parser.find_dates("Exam 10/27, meeting Tuesday."),
            [date(2026, 10, 27), date(2026, 11, 3)]
        )

    def test_date_at_end_of_sentence(self):
        self.assertEqual(
            self.parser.find_dates("My exam is on 10/27!"),
            [date(2026, 10, 27)]
        )



if __name__ == "__main__":
    unittest.main()
