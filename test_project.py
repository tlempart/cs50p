import unittest
from project import convert_to_float, Subject, School, get_subject_order, get_sorted_school_rows

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

    def test_has_results_no_results(self):
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

    def test_floats_with_comma(self):
        self.assertEqual(convert_to_float("1,0"), 1.0)
        self.assertEqual(convert_to_float("0,57"), 0.57)
        self.assertEqual(convert_to_float("123,123"), 123.123)

    def test_empty(self):
        self.assertEqual(convert_to_float(""), 0)

    def test_non_number(self):
        with self.assertRaises(ValueError):
            convert_to_float("A")

class TestGetSubjectOrder(unittest.TestCase):

    def test_valid_subject_and_order(self):
        self.assertEqual(get_subject_order("P", "A"), "polish_average")
        self.assertEqual(get_subject_order("E", "T"), "english_trend")
        self.assertEqual(get_subject_order("M", "A"), "math_average")
        self.assertEqual(get_subject_order("A", "T"), "all_trend")

    def test_invalid_subject_code(self):
        with self.assertRaises(KeyError):
            get_subject_order("G", "A")  # G is not defined
        with self.assertRaises(KeyError):
            get_subject_order("Z", "T")
        with self.assertRaises(KeyError):
            get_subject_order("", "A")

    def test_invalid_order_code(self):
        with self.assertRaises(KeyError):
            get_subject_order("P", "X")
        with self.assertRaises(KeyError):
            get_subject_order("M", "")
        with self.assertRaises(KeyError):
            get_subject_order("A", "1")

    def test_case_sensitivity(self):
        with self.assertRaises(KeyError):
            get_subject_order("p", "a")  # Lowercase unsupported

class MockSchool:
    """Mock version of the School class for testing."""
    def __init__(self, name, result_data):
        self.name = name
        self.result_data = result_data

    def convert_to_dict(self, trend_year: int) -> dict[str, float]:
        return {"school": self.name, **self.result_data}

class TestGetSortedSchoolRows(unittest.TestCase):

    def setUp(self):
        self.schools = [
            MockSchool("Alpha", {"math_average": 65.0, "math_trend": 84.0}),
            MockSchool("Beta",  {"math_average": 82.0, "math_trend": 67.5}),
            MockSchool("Gamma", {"math_average": 75.0, "math_trend": 70.0}),
        ]

    def test_sort_by_math_average(self):
        sorted_rows = get_sorted_school_rows(self.schools, "math_average", 2025)
        names = [row["school"] for row in sorted_rows]
        self.assertEqual(names, ["Beta", "Gamma", "Alpha"])

    def test_sort_by_math_trend(self):
        sorted_rows = get_sorted_school_rows(self.schools, "math_trend", 2025)
        names = [row["school"] for row in sorted_rows]
        self.assertEqual(names, ["Alpha", "Gamma", "Beta"])

    def test_empty_input(self):
        sorted_rows = get_sorted_school_rows([], "math_average", 2025)
        self.assertEqual(sorted_rows, [])

    def test_missing_sort_key(self):
        # One school lacks the sort key
        self.schools.append(MockSchool("Delta", {"english_average": 60.0}))
        with self.assertRaises(KeyError):
            get_sorted_school_rows(self.schools, "math_average", 2025)
