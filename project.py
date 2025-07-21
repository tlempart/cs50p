from enum import Enum
import csv
import numpy as np
import pyinputplus as pyip
from sklearn.linear_model import LinearRegression
from tabulate import tabulate

Subject = Enum('Subject', [('POLISH', 1), ('ENGLISH', 2), ('MATH', 3)])

class School:

    def __init__(self, name) -> None:
        self.name = name
        self.results: dict[str, dict[int, float]] = {
            Subject.POLISH: {},
            Subject.ENGLISH: {},
            Subject.MATH: {}
        }

    def has_results(self, subject: Subject) -> bool:
        return len(self.results[subject].values()) > 0

    def add_result(self, subject: Subject, year: int, result: float) -> None:
        self.results[subject][year] = result

    def calculate_average(self, subject: Subject) -> float:
        return sum(self.results[subject].values()) / len(self.results[subject]) if self.has_results(subject) else 0.0

    def calculate_trend(self, subject: Subject, year: int) -> float:
        if not self.has_results(subject):
            return 0.0

        x = np.array(list(self.results[subject].keys())).reshape(-1, 1)
        y = np.array(list(self.results[subject].values()))

        model = LinearRegression()
        model.fit(x, y)

        y_pred = model.predict(np.array([[year]]))

        return np.clip(y_pred[0], 0.0, 100.0)

    def convert_to_dict(self, trend_year: int) -> dict[str, float]:
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
    Converts string containing numeric value to a float. If the string is empty, returns 0.

    :param number_as_string: numeric value to convert to float
    :return: number_as_string converted to float
    :raises: ValueError when number_as_string is non-numeric
    """
    return 0 if not number_as_string else float(number_as_string.replace(",", "."))

def main():
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
