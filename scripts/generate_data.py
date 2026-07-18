import os
import csv

def generate_courses_csv(file_path: str = "data/courses.csv"):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    courses = [
        {"Course_ID": "1", "Title": "Java Beginners Tutorial", "Category": "Core Programming", "Difficulty": "Beginner", "Avg_Rating": "4.8"},
        {"Course_ID": "2", "Title": "Python Beginners Tutorial", "Category": "Core Programming", "Difficulty": "Beginner", "Avg_Rating": "4.9"},
        {"Course_ID": "3", "Title": "C++ Beginners Tutorial", "Category": "Core Programming", "Difficulty": "Intermediate", "Avg_Rating": "4.7"},
        {"Course_ID": "4", "Title": "C Language Tutorial for Beginners", "Category": "Core CS", "Difficulty": "Intermediate", "Avg_Rating": "4.6"},
        {"Course_ID": "5", "Title": "Rust Programming Course for Beginners", "Category": "Systems Programming", "Difficulty": "Advanced", "Avg_Rating": "4.5"}
    ]
    
    headers = ["Course_ID", "Title", "Category", "Difficulty", "Avg_Rating"]
    
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(courses)
    print(f"[OK] Courses generated at {file_path}")

def generate_modules_csv(file_path: str = "data/modules.csv"):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    modules = [
        # Course 1: Java
        {
            "Course_ID": "1",
            "Module_ID": "1_1",
            "Title": "Java Setup & First Code",
            "URL": "https://www.youtube.com/watch?v=WOUpItam-r4",
            "Module_Order": "1",
            "Puzzle_Question": "Fix the syntax: public static void main(String args[]) { System.out.print('Hello') }",
            "Puzzle_Hint": "Java statements must end with a semicolon.",
            "Puzzle_Answer": "System.out.print('Hello');"
        },
        {
            "Course_ID": "1",
            "Module_ID": "1_2",
            "Title": "Variables & Data Types",
            "URL": "https://www.youtube.com/watch?v=SHIT5VeehI4",
            "Module_Order": "2",
            "Puzzle_Question": "Declare an integer variable named 'age' and assign it the value 20.",
            "Puzzle_Hint": "Use the 'int' keyword followed by the variable name, an equals sign, and the value.",
            "Puzzle_Answer": "int age = 20;"
        },
        {
            "Course_ID": "1",
            "Module_ID": "1_3",
            "Title": "Classes & Objects",
            "URL": "https://www.youtube.com/watch?v=8S69GfQrkCg",
            "Module_Order": "3",
            "Puzzle_Question": "Instantiate a new object of class 'Car' named 'myCar'.",
            "Puzzle_Hint": "Use the 'new' keyword to call the class constructor.",
            "Puzzle_Answer": "Car myCar = new Car();"
        },
        # Course 2: Python
        {
            "Course_ID": "2",
            "Module_ID": "2_1",
            "Title": "Python Basics",
            "URL": "https://www.youtube.com/watch?v=aqvDTCYhK3w",
            "Module_Order": "1",
            "Puzzle_Question": "Print the string 'Hello World' to the console.",
            "Puzzle_Hint": "Use the print() function with single or double quotes around the string.",
            "Puzzle_Answer": "print('Hello World')"
        },
        {
            "Course_ID": "2",
            "Module_ID": "2_2",
            "Title": "Lists & Tuples",
            "URL": "https://www.youtube.com/watch?v=vLqTf2b6GZw",
            "Module_Order": "2",
            "Puzzle_Question": "Create a list named 'fruits' containing 'apple' and 'banana'.",
            "Puzzle_Hint": "Use square brackets to enclose comma-separated string elements.",
            "Puzzle_Answer": "fruits = ['apple', 'banana']"
        },
        {
            "Course_ID": "2",
            "Module_ID": "2_3",
            "Title": "Loops",
            "URL": "https://www.youtube.com/watch?v=cfJruaCgVjY",
            "Module_Order": "3",
            "Puzzle_Question": "Write a for loop syntax to iterate over a list named 'items' using variable 'i'.",
            "Puzzle_Hint": "Start with 'for i in', reference the list, and end with a colon.",
            "Puzzle_Answer": "for i in items:"
        },
        # Course 3: C++
        {
            "Course_ID": "3",
            "Module_ID": "3_1",
            "Title": "C++ Structure",
            "URL": "https://www.youtube.com/watch?v=18c3MTX0PK0",
            "Module_Order": "1",
            "Puzzle_Question": "Include the standard input/output stream library.",
            "Puzzle_Hint": "Use preprocessor directive #include followed by angle brackets containing iostream.",
            "Puzzle_Answer": "#include <iostream>"
        },
        {
            "Course_ID": "3",
            "Module_ID": "3_2",
            "Title": "Pointers",
            "URL": "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
            "Module_Order": "2",
            "Puzzle_Question": "Declare an integer pointer named 'ptr'.",
            "Puzzle_Hint": "Use 'int*' or 'int *' followed by the name, ending with a semicolon.",
            "Puzzle_Answer": "int* ptr;"
        },
        {
            "Course_ID": "3",
            "Module_ID": "3_3",
            "Title": "Object Oriented C++",
            "URL": "https://www.youtube.com/watch?v=wN0x9eLdg1s",
            "Module_Order": "3",
            "Puzzle_Question": "Create a public class named 'Dog'.",
            "Puzzle_Hint": "Use the class keyword, dog name, curly braces enclosing 'public:', and a semicolon at the end.",
            "Puzzle_Answer": "class Dog { public: };"
        },
        # Course 4: C Language
        {
            "Course_ID": "4",
            "Module_ID": "4_1",
            "Title": "C Basics",
            "URL": "https://www.youtube.com/watch?v=aZb0iu4uGwA",
            "Module_Order": "1",
            "Puzzle_Question": "Write the syntax to return 0 from the main function.",
            "Puzzle_Hint": "Use the return keyword followed by 0 and a semicolon.",
            "Puzzle_Answer": "return 0;"
        },
        {
            "Course_ID": "4",
            "Module_ID": "4_2",
            "Title": "Control Flow",
            "URL": "https://www.youtube.com/watch?v=aZb0iu4uGwA&t=3600",
            "Module_Order": "2",
            "Puzzle_Question": "Write an if statement checking if x is equal to 5.",
            "Puzzle_Hint": "Do not use curly braces or semicolons, just the basic if condition statement.",
            "Puzzle_Answer": "if (x == 5)"
        },
        {
            "Course_ID": "4",
            "Module_ID": "4_3",
            "Title": "Memory Management",
            "URL": "https://www.youtube.com/watch?v=aZb0iu4uGwA&t=7200",
            "Module_Order": "3",
            "Puzzle_Question": "Use malloc to allocate memory for an integer pointer 'p'.",
            "Puzzle_Hint": "Assign malloc to p casting it to int* and specifying sizeof(int).",
            "Puzzle_Answer": "p = (int*)malloc(sizeof(int));"
        },
        # Course 5: Rust
        {
            "Course_ID": "5",
            "Module_ID": "5_1",
            "Title": "Cargo & Setup",
            "URL": "https://www.youtube.com/watch?v=MsocPEZBd-M",
            "Module_Order": "1",
            "Puzzle_Question": "Write the cargo command to create a new project.",
            "Puzzle_Hint": "Use cargo followed by new. Do not specify a project name.",
            "Puzzle_Answer": "cargo new"
        },
        {
            "Course_ID": "5",
            "Module_ID": "5_2",
            "Title": "Variables & Mutability",
            "URL": "https://www.youtube.com/watch?v=MsocPEZBd-M&t=1200",
            "Module_Order": "2",
            "Puzzle_Question": "Declare a mutable integer variable named 'count' initialized to 0.",
            "Puzzle_Hint": "Use 'let mut' followed by the variable name, equals sign, and value.",
            "Puzzle_Answer": "let mut count = 0;"
        },
        {
            "Course_ID": "5",
            "Module_ID": "5_3",
            "Title": "Ownership & Borrowing",
            "URL": "https://www.youtube.com/watch?v=MsocPEZBd-M&t=2400",
            "Module_Order": "3",
            "Puzzle_Question": "Pass a variable 's' as an immutable reference to a function.",
            "Puzzle_Hint": "Prefix the variable name with an ampersand.",
            "Puzzle_Answer": "&s"
        }
    ]
    
    headers = ["Course_ID", "Module_ID", "Title", "URL", "Module_Order", "Puzzle_Question", "Puzzle_Hint", "Puzzle_Answer"]
    
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(modules)
    print(f"[OK] Modules generated at {file_path}")

def generate_all():
    generate_courses_csv("data/courses.csv")
    generate_modules_csv("data/modules.csv")

if __name__ == "__main__":
    generate_all()
