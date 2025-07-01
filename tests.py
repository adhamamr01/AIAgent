from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

print(f"Result for first test:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
)

print(f"Result for second text:")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
)

print(f"Result for third test:")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

