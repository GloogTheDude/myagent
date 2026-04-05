from functions import get_file_content as gfi

print(gfi.get_file_content("calculator", "main.py"))
print(gfi.get_file_content("calculator", "pkg/calculator.py"))
print(gfi.get_file_content("calculator", "/bin/cat")) #(this should return an error string)
print(gfi.get_file_content("calculator", "pkg/does_not_exist.py")) #(this should return an error string)