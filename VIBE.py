#Nnadozie Nwachukwu
#CIS261
#VIBE coding

from dataclasses import dataclass
from typing import List

DATA_FILE = "student_grades.txt"


@dataclass
class Student:
    name: str
    student_id: str
    test1: float
    test2: float
    test3: float
    average: float = 0.0
    grade: str = "N/A"

    def __post_init__(self) -> None:
        self.calculate_results()

    def calculate_results(self) -> None:
        self.average = round((self.test1 + self.test2 + self.test3) / 3.0, 2)
        self.grade = self.letter_grade()

    def letter_grade(self) -> str:
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"

    def to_pipe_line(self) -> str:
        return f"{self.name}|{self.student_id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"

    @classmethod
    def from_pipe_line(cls, line: str):
        parts = [part.strip() for part in line.strip().split("|")]
        if len(parts) != 7:
            raise ValueError("Invalid record format")
        name, student_id, test1, test2, test3, _, _ = parts
        return cls(
            name=name,
            student_id=student_id,
            test1=float(test1),
            test2=float(test2),
            test3=float(test3),
        )


def input_float(prompt: str, min_value: float = 0.0, max_value: float = 100.0) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if value < min_value or value > max_value:
                print(f"Please enter a number between {min_value:.2f} and {max_value:.2f}.")
                continue
            return value
        except ValueError:
            print("Invalid score. Please enter a numeric value.")


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be blank. Please try again.")


def load_records(filename: str) -> List[Student]:
    records: List[Student] = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    records.append(Student.from_pipe_line(line))
                except Exception as error:
                    print(f"Warning: skipped invalid line {line_number}: {error}")
    except FileNotFoundError:
        print(f"No existing data file found. A new '{filename}' file will be created when you save records.")
    except OSError as error:
        print(f"Error loading records: {error}")
    return records


def save_records(filename: str, records: List[Student]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in records:
                file.write(student.to_pipe_line() + "\n")
    except OSError as error:
        print(f"Error saving records: {error}")


def find_student_by_id(records: List[Student], student_id: str):
    return next((student for student in records if student.student_id == student_id), None)


def add_student(records: List[Student]) -> None:
    student_id = input_non_empty("Enter student ID: ")
    if find_student_by_id(records, student_id) is not None:
        print(f"A student with ID '{student_id}' already exists.")
        return

    name = input_non_empty("Enter student name: ")
    test1 = input_float("Enter Test 1 score (0-100): ")
    test2 = input_float("Enter Test 2 score (0-100): ")
    test3 = input_float("Enter Test 3 score (0-100): ")

    student = Student(name=name, student_id=student_id, test1=test1, test2=test2, test3=test3)
    records.append(student)
    print("Student record added successfully.")


def display_all_students(records: List[Student]) -> None:
    if not records:
        print("No student records to display.")
        return

    headers = ["Name", "ID", "Test1", "Test2", "Test3", "Average", "Grade"]
    rows = [
        [student.name, student.student_id, f"{student.test1:.2f}", f"{student.test2:.2f}", f"{student.test3:.2f}", f"{student.average:.2f}", student.grade]
        for student in records
    ]
    widths = [max(len(str(value)) for value in column) for column in zip(headers, *rows)]

    header_line = " | ".join(header.ljust(widths[idx]) for idx, header in enumerate(headers))
    divider = "-+-".join("-" * width for width in widths)
    print(header_line)
    print(divider)
    for row in rows:
        print(" | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(row)))


def calculate_class_statistics(records: List[Student]) -> None:
    if not records:
        print("No student records available to calculate statistics.")
        return

    averages = [student.average for student in records]
    highest = max(averages)
    lowest = min(averages)
    class_average = round(sum(averages) / len(averages), 2)

    highest_students = [student for student in records if student.average == highest]
    lowest_students = [student for student in records if student.average == lowest]

    print(f"Class average: {class_average:.2f}")
    print(f"Highest average: {highest:.2f} ({', '.join(student.name for student in highest_students)})")
    print(f"Lowest average: {lowest:.2f} ({', '.join(student.name for student in lowest_students)})")


def search_student_by_name(records: List[Student]) -> None:
    query = input_non_empty("Enter student name to search: ")
    lowercase_query = query.lower()
    matches = [student for student in records if lowercase_query in student.name.lower()]

    if not matches:
        print(f"No students found matching '{query}'.")
        return

    print(f"Found {len(matches)} student(s) matching '{query}':")
    display_all_students(matches)


def view_student_record(records: List[Student]) -> None:
    if not records:
        print("No student records available.")
        return
    
    student_id = input_non_empty("Enter student ID to view: ")
    student = find_student_by_id(records, student_id)
    
    if student is None:
        print(f"Student with ID '{student_id}' not found.")
        return
    
    print(f"\n--- Student Record ---")
    print(f"Name: {student.name}")
    print(f"ID: {student.student_id}")
    print(f"Test 1: {student.test1:.2f}")
    print(f"Test 2: {student.test2:.2f}")
    print(f"Test 3: {student.test3:.2f}")
    print(f"Average: {student.average:.2f}")
    print(f"Grade: {student.grade}")
    print()


def print_menu() -> None:
    print("\nStudent Record Manager")
    print("1. Add new student")
    print("2. Display all students")
    print("3. Search student by name")
    print("4. View student record")
    print("5. Class statistics")
    print("6. Save records")
    print("7. Exit")
    print("Press ESC or type '7' to exit.")


def main() -> None:
    records = load_records(DATA_FILE)
    if records:
        print(f"Loaded {len(records)} student record(s) from '{DATA_FILE}'.")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(records)
            save_records(DATA_FILE, records)
        elif choice == "2":
            display_all_students(records)
        elif choice == "3":
            search_student_by_name(records)
        elif choice == "4":
            view_student_record(records)
        elif choice == "5":
            calculate_class_statistics(records)
        elif choice == "6":
            save_records(DATA_FILE, records)
            print(f"Records saved to '{DATA_FILE}' successfully.")
        elif choice == "7" or choice.upper() == "ESC" or choice == "\x1b":
            save_records(DATA_FILE, records)
            print("Saving records and exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()

