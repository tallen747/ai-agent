from functions.get_file_content import get_file_content

content = get_file_content("calculator", "lorem.txt")
print(f"Result for lorem.txt:")
print(f"Length of lorem.txt: {len(content)} characters")
print(f"Last 54 characters of lorem.txt: {content[-54:]}")

content = get_file_content("calculator", "main.py")
print(f"Result for main.py:")
print(f"Content of main.py:\n{content}")

content = get_file_content("calculator", "pkg/calculator.py")
print(f"Result for pkg/calculator.py:")
print(f"Content of pkg/calculator.py:\n{content}")

content = get_file_content("calculator", "/bin/cat")
print(f"Result for /bin/cat:")
print(f"Content of /bin/cat:\n{content}")

content = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"Result for pkg/does_not_exist.py:")
print(f"Content of pkg/does_not_exist.py:\n{content}")