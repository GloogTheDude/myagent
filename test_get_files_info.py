from functions import get_files_info as gf

print(gf.get_files_info("calculator", "."))
print(gf.get_files_info("calculator", "pkg"))
print(gf.get_files_info("calculator", "/bin"))
print(gf.get_files_info("calculator", "../"))