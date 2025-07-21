import unittest
from project import convert_to_float, Subject
from project import School

class TestSchool(unittest.TestCase):

    def test_has_results_two_results(self):
        school = School("A")
        school.add_result(Subject.MATH, 2021, 32.0)
        school.add_result(Subject.MATH,2022, 64.0)
        self.assertTrue(school.has_results(Subject.MATH))

    def test_has_results_single_result(self):
        school = School("A")
        school.add_result(Subject.MATH,2021, 32.0)
        self.assertTrue(school.has_results(Subject.MATH))

    def test_calculate_average_no_results(self):
        school = School("A")
        self.assertFalse(school.has_results(Subject.MATH))


    def test_calculate_average_two_results(self):
        school = School("A")
        school.add_result(Subject.MATH, 2021, 32.0)
        school.add_result(Subject.MATH,2022, 64.0)
        self.assertEqual(school.calculate_average(Subject.MATH), 48)

    def test_calculate_average_single_result(self):
        school = School("A")
        school.add_result(Subject.MATH,2021, 32.0)
        self.assertEqual(school.calculate_average(Subject.MATH), 32)

    def test_calculate_average_no_results(self):
        school = School("A")
        self.assertEqual(school.calculate_average(Subject.MATH), 0)

    def test_calculate_trend_two_results(self):
        school = School("A")
        school.add_result(Subject.MATH,2021, 32.0)
        school.add_result(Subject.MATH,2022, 64.0)
        self.assertEqual(school.calculate_trend(Subject.MATH,2023), 96.0)

    def test_calculate_trend_single_result(self):
        school = School("A")
        school.add_result(Subject.MATH,2021, 32.0)
        self.assertEqual(school.calculate_trend(Subject.MATH,2022), 32.0)

    def test_calculate_trend_no_results(self):
        school = School("A")
        self.assertEqual(school.calculate_trend(Subject.MATH,2022), 0.0)

    def test_calculate_trend_greater_than_100(self):
        school = School("A")
        school.add_result(Subject.MATH,2021, 80.0)
        school.add_result(Subject.MATH,2022, 99.0)
        self.assertEqual(school.calculate_trend(Subject.MATH,2023), 100.0)

    def test_calculate_trend_less_than_0(self):
        school = School("A")
        school.add_result(Subject.MATH,2021, 20.0)
        school.add_result(Subject.MATH,2022, 1.0)
        self.assertEqual(school.calculate_trend(Subject.MATH,2023), 0.0)

class TestConvertToFlat(unittest.TestCase):

    def test_integers(self):
        self.assertEqual(convert_to_float("1"), 1.0)
        self.assertEqual(convert_to_float("0"), 0.0)
        self.assertEqual(convert_to_float("123"), 123.0)

    def test_floats(self):
        self.assertEqual(convert_to_float("1.0"), 1.0)
        self.assertEqual(convert_to_float("0.57"), 0.57)
        self.assertEqual(convert_to_float("123.123"), 123.123)

    def test_empty_and_none(self):
        self.assertEqual(convert_to_float(""), 0)
        self.assertEqual(convert_to_float(None), 0)

    def test_non_number(self):
        with self.assertRaises(ValueError):
            convert_to_float("A")

