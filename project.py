from enum import Enum
import csv
import numpy as np
import pyinputplus as pyip
from sklearn.linear_model import LinearRegression
from tabulate import tabulate

class Subject(Enum):
    """
    Enumeration of school subjects.

    Attributes:
        POLISH (int): The Polish language subject.
        ENGLISH (int): The English language subject.
        MATH (int): The Math subject.
    """
    POLISH = 1
    ENGLISH = 2
    MATH = 3

class School:
    """
    Represents a school with exam results for Polish, English, and Math subjects.

    Each subject result is stored as a dictionary mapping the year to the average score.
    Provides methods to add results, calculate averages, estimate performance trends,
    and convert school data into a dictionary format for further use (e.g., reporting or serialization).
    """

    def __init__(self, name) -> None:
        """
        Initializes a School instance with an empty result structure for each subject.

        :param name: The name of the school.
        :type name: str
        """
        self.name = name
        self.results: dict[Subject, dict[int, float]] = {
            Subject.POLISH: {},
            Subject.ENGLISH: {},
            Subject.MATH: {}
        }

    def has_results(self, subject: Subject) -> bool:
        """
        Checks if the school has any results recorded for the given subject.

        :param subject: The subject to check for results.
        :type subject: Subject
        :return: True if results are present, False otherwise.
        :rtype: bool
        """
        return len(self.results[subject].values()) > 0

    def add_result(self, subject: Subject, year: int, result: float) -> None:
        """
        Adds an exam result for a specific subject and year.

        :param subject: The subject for which to add the result.
        :type subject: Subject
        :param year: The year of the exam.
        :type year: int
        :param result: The average score for the exam.
        :type result: float
        """
        self.results[subject][year] = result

    def calculate_average(self, subject: Subject) -> float:
        """
        Calculates the average result for a specific subject.

        :param subject: The subject to calculate the average for.
        :type subject: Subject
        :return: The average score, or 0.0 if no results are available.
        :rtype: float
        """
        return sum(self.results[subject].values()) / len(self.results[subject]) if self.has_results(subject) else 0.0

    def calculate_trend(self, subject: Subject, year: int) -> float:
        """
        Predicts the expected result for a given year using linear regression based on past results.

        :param subject: The subject to calculate the trend for.
        :type subject: Subject
        :param year: The year for which to predict the result.
        :type year: int
        :return: The predicted score, clipped to the range 0.0–100.0. Returns 0.0 if no data is available.
        :rtype: float

        :requires: `numpy` and `sklearn.linear_model.LinearRegression`
        """
        if not self.has_results(subject):
            return 0.0

        x = np.array(list(self.results[subject].keys())).reshape(-1, 1)
        y = np.array(list(self.results[subject].values()))

        model = LinearRegression()
        model.fit(x, y)

        y_pred = model.predict(np.array([[year]]))

        return np.clip(y_pred[0], 0.0, 100.0)

    def convert_to_dict(self, trend_year: int) -> dict[str, float]:
        """
        Converts the school data into a dictionary that includes average exam results and
        predicted trends for Polish, English, and Math, as well as combined metrics.

        This method is typically used for reporting, exporting, or feeding structured
        school performance data into downstream systems like analytics dashboards.

        :param trend_year: The year for which to predict exam trends using linear regression.
        :type trend_year: int
        :return: A dictionary containing exam averages and trend predictions.
        :rtype: dict[str, float or str]

        Returns:
            The returned dictionary contains the following keys:

            - ``school`` (str): Name of the school.
            - ``polish_average`` (float): Average Polish exam score.
            - ``polish_trend`` (float): Predicted Polish score for the trend year.
            - ``english_average`` (float): Average English exam score.
            - ``english_trend`` (float): Predicted English score for the trend year.
            - ``math_average`` (float): Average Math exam score.
            - ``math_trend`` (float): Predicted Math score for the trend year.
            - ``all_average`` (float): Overall average score (mean of all three subjects).
            - ``all_trend`` (float): Overall predicted score for the trend year.



        Example:

        >>> school = School("Publiczna SP nr 1 im. Jana Pawła II")
        >>> # ... suppose results have been added here ...
        >>> school.convert_to_dict(2025)
        {
            "school": "Publiczna SP nr 1 im. Jana Pawła II",
            "polish_average": 63.4,
            "polish_trend": 65.2,
            "english_average": 76.1,
            "english_trend": 77.9,
            "math_average": 58.7,
            "math_trend": 61.3,
            "all_average": 66.07,
            "all_trend": 68.13
        }
        """
        polish_average = self.calculate_average(Subject.POLISH)
        polish_trend = self.calculate_trend(Subject.POLISH, trend_year)
        english_average = self.calculate_average(Subject.ENGLISH)
        english_trend = self.calculate_trend(Subject.ENGLISH, trend_year)
        math_average = self.calculate_average(Subject.MATH)
        math_trend = self.calculate_trend(Subject.MATH, trend_year)
        return {
            "school": self.name,
            "polish_average": polish_average,
            "polish_trend": polish_trend,
            "english_average": english_average,
            "english_trend": english_trend,
            "math_average": math_average,
            "math_trend": math_trend,
            "all_average": (polish_average + english_average + math_average) / 3,
            "all_trend": (polish_trend + english_trend + math_trend) / 3
        }

def read_schools(years: list[str], city: str) -> list[School]:
    """
    Reads school performance data from CSV files for a given list of years and filters it by city.

    This function processes CSV files named `resources/e8-schools-<year>.csv`, where `<year>` is each
    entry from the `years` list. It reads rows that match the specified city and builds a list of
    `School` objects, each enriched with average exam results for Polish, English, and Math
    (if available). Each school is uniquely identified by its name.

    :param years: A list of school report years (e.g., ['2021', '2022']).
    :type years: list[str]
    :param city: The name of the city to filter schools by.
    :type city: str
    :return: A list of `School` objects with aggregated results by subject and year.
    :rtype: list[School]

    :raises FileNotFoundError: If any of the CSV files for the given years are missing.
    :raises KeyError: If expected CSV columns are missing (e.g., 'school', 'city', 'polish_average', etc.).
    :raises ValueError: If any non-numeric average values cannot be converted to float.

    :example:

    >>> schools = read_schools(['2021', '2022'], 'Warsaw')
    >>> len(schools)
    15
    >>> schools[0].name
    'Publiczna SP nr 1 im. Jana Pawła II'
    >>> schools[0].results[Subject.POLISH][2021]
    64.3
    """
    schools_by_name = {}
    for year in years:
        with open(f"resources/e8-schools-{year}.csv") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if row["city"] == city:
                    if not row["school"] in schools_by_name:
                        schools_by_name[row["school"]] = School(row["school"])

                    school = schools_by_name[row["school"]]
                    if row["polish_average"]:
                        school.add_result(Subject.POLISH, int(year), convert_to_float(row["polish_average"]))
                    if row["english_average"]:
                        school.add_result(Subject.ENGLISH, int(year), convert_to_float(row["english_average"]))
                    if row["math_average"]:
                        school.add_result(Subject.MATH, int(year), convert_to_float(row["math_average"]))

    return list(schools_by_name.values())

def convert_to_float(number_as_string: str) -> float:
    """
    Converts a string representation of a number to a float.

    This function handles strings where the decimal separator may be a comma
    (',') instead of a period ('.'), which is common in many European locales.
    If the input string is empty, it returns 0.0.

    :param number_as_string: The string representation of the number.
    :type number_as_string: str
    :return: The numeric value represented by the string.
    :rtype: float
    :raises ValueError: If the string cannot be converted to a float.

    :example:

    >>> convert_to_float("123.45")
    123.45
    >>> convert_to_float("123,45")
    123.45
    >>> convert_to_float("")
    0.0
    >>> convert_to_float("abc")
    Traceback (most recent call last):
        ...
    ValueError: could not convert string to float: 'abc'
    """
    return 0 if not number_as_string else float(number_as_string.replace(",", "."))

def main():
    """
    Main entry point of the program.

    Prompts the user to input a city name, choose a subject, and choose whether to sort by average or trend.
    Then loads school data for the given city across multiple years, computes averages and trends,
    sorts the schools based on the user's selection, and prints the results in a table.

    The subject options are:
        - 'P' for Polish
        - 'E' for English
        - 'M' for Math
        - 'A' for All subjects combined

    The order options are:
        - 'A' to sort by average score
        - 'T' to sort by trend prediction

    The program reads school data from CSV files for the years 2021 to 2024,
    and uses 2025 as the year for trend prediction.

    :raises KeyboardInterrupt: If the user interrupts input (Ctrl+C).
    """
    city: str = pyip.inputStr("City: ")
    subject: str = pyip.inputChoice(choices=["P", "E", "M", "A"], prompt='Subject (P for polish, E for english, M for math, A for all): ')
    order: str = pyip.inputChoice(choices=["A", "T"], prompt="Order (A for average, T for trend): ")

    subjects = { "P": "polish", "E": "english", "M": "math", "A": "all" }
    orders = { "A": "average", "T": "trend" }

    subject_order = subjects[subject] + "_" + orders[order]

    schools: list[School] = read_schools(["2021", "2022", "2023", "2024"], city)
    school_rows: list[str: float] = list(school.convert_to_dict(2025) for school in schools)

    school_rows.sort(key=lambda item: item[subject_order], reverse=True)
    print(tabulate(school_rows, headers="keys"))

if __name__ == '__main__':
    main()
