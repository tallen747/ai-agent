from functions.get_files_info import get_files_info

info = get_files_info("calculator", ".")
print(f"Result for current directory:")
if isinstance(info, list):
    for i in range(0,len(info)):
        print(info[i])
else:
    print(info)

info = get_files_info("calculator", "pkg")
print(f"Result for 'pkg' directory:")
if isinstance(info, list):
    for i in range(0,len(info)):
        print(info[i])
else:
    print(info)

info = get_files_info("calculator", "/bin")
print(f"Result for '/bin' directory:")
if isinstance(info, list):
    for i in range(0,len(info)):
        print(info[i])
else:
    print(info)

info = get_files_info("calculator", "../")
print(f"Result for '../' directory:")
if isinstance(info, list):
    for i in range(0,len(info)):
        print(info[i])
else:
    print(info)