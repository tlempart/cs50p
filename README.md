# 📊 School Exam Results Analyzer

This Python project analyzes standardized 8th-grade exam results of schools across Poland. It allows users to interactively compare average scores and performance trends in Polish, English, and Math subjects over multiple years.

📍 Data Source:
The exam results are obtained from the official website of the Central Examination Board of Poland (Centralna Komisja Egzaminacyjna – CKE):
🔗 https://mapa.wyniki.edu.pl/MapaEgzaminow/

## 🚀 Features

* Reads standardized exam results for multiple years.
* Supports Polish, English, and Math subjects.
* Calculates per-school:
  * Subject-wise averages
  * Subject-wise trend predictions (using linear regression)
* Sorts and displays results in tabular format.
  * Interactive command-line input for:
  * City selection
  * Subject selection
  * Sort order (average or trend)
    
## 🧱 Project Structure

```
.
├── main.py
├── resources/
│   ├── e8-schools-2021.csv
│   ├── e8-schools-2022.csv
│   ├── e8-schools-2023.csv
│   └── e8-schools-2024.csv
```

## 📦 Requirements

Install dependencies via pip:

```
pip install numpy scikit-learn pyinputplus tabulate
```

## 📝 Usage

Run the script:

```
python main.py
```

### Example Prompts

```
City: Warsaw
Subject (P for polish, E for english, M for math, A for all): A
Order (A for average, T for trend): A
```

### Output

A nicely formatted table like:

| school   | polish_average | polish_trend | english_average | english_trend | math_average | math_trend | all_average | all_trend |
|----------|----------------|--------------|-----------------|---------------|--------------|------------|-------------|-----------|
| School A | 75.0           | 78.2         | 82.0            | 84.5          | 90.0         | 92.3       | 82.3        | 85.0      | 
| School B | 70.0           | 71.1         | 75.0            | 76.8          | 85.0         | 86.2       | 76.7        | 78.0      | 
| ...      |                |              |                 |               |              |            |             |           |

## 📁 Input File Format

CSV files must be placed in the `resources/` folder and named like:

```
e8-schools-2021.csv
e8-schools-2022.csv
...
```

### CSV Columns Required:
- `city`
- `school`
- `polish_average`
- `english_average`
- `math_average`

### Example CSV Row:

```
city;school;polish_average;english_average;math_average
Warsaw;School A;75,0;82,0;90,0
```
Note: Decimal numbers use a comma (,) and are internally converted to floats.

### 📈 How Trends Are Calculated

The program uses `LinearRegression` from `scikit-learn` to fit a line to past results and predict the performance for the next year (hardcoded as 2025).

### 🧪 Example Function

```
def calculate_trend(self, subject: Subject, year: int) -> float:
# Fits linear regression to past years and predicts result for given year
```

### ❓ Why Use This

This tool is useful for:
- Educators comparing school performances over years
- Analysts exploring exam result trends
- Report generation for school administrators

### 📄 License

MIT License (or specify your preferred license)
