from functions.run_python_file import run_python_file


result = run_python_file("calculator", "main.py")
print(f"Result for running main.py:\n{result}")

result = run_python_file("calculator", "main.py", ["3 + 5"])
print(f"Result for running main.py with arguments ['3 + 5']:\n{result}")

result = run_python_file("calculator", "tests.py")
print(f"Result for running tests.py:\n{result}")

result = run_python_file("calculator", "../main.py")
print(f"Result for running ../main.py:\n{result}") #should return an error since main.py is not in the calculator directory

result = run_python_file("calculator", "nonexistent.py")
print(f"Result for running nonexistent.py:\n{result}") #should return an error since nonexistent.py does not exist

result = run_python_file("calculator", "lorem.txt")
print(f"Result for running lorem.txt:\n{result}") #should return an error since lorem.txt is not a Python file