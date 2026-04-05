from functions import run_python_file as rpf

print(rpf.run_python_file("calculator", "main.py")) #(should print the calculator's usage instructions)
print(rpf.run_python_file("calculator", "main.py", ["3 + 5"])) #(should run the calculator... which gives a kinda nasty rendered result)
print(rpf.run_python_file("calculator", "tests.py")) #(should run the calculator's tests successfully)
print(rpf.run_python_file("calculator", "../main.py")) #(this should return an error)
print(rpf.run_python_file("calculator", "nonexistent.py")) #(this should return an error)
print(rpf.run_python_file("calculator", "lorem.txt")) #(this should return an error)