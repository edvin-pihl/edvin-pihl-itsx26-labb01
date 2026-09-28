failed_count = 0

with open("data/auth.log", encoding="utf-8") as log_file:
    for line in log_file:
        if "Failed login" in line:
            failed_count += 1
            print(line.strip())

print(f"Failed logins: {failed_count}")