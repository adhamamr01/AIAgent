from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

print(f"Result for first test:")
print(run_python_file("calculator", "main.py"))


print(f"Result for second text:")
print(run_python_file("calculator", "tests.py"))


print(f"Result for third test:")
print(run_python_file("calculator", "../main.py"))

print(f"Result for fourth test:")
print(run_python_file("calculator", "nonexistent.py"))
