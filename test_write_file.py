from functions import write_file as wf

x = wf.write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(x)
x =wf.write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(x)
x=wf.write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(x)