ip_counts = {}

with open("data/auth.log", encoding="utf-8") as log_file:
    for line in log_file:
        if "Failed login" not in line:
            continue

        source_field = line.split()[-1]
        ip_address = source_field.split("=")[1]
        ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1

for ip_address, count in sorted(ip_counts.items()):
    print(f"{ip_address}: {count}")