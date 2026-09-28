with open("data/suspicious_ips.txt", encoding="utf-8") as indicator_file:
    suspicious_ips = {line.strip() for line in indicator_file if line.strip()}

matches = {}

with open("data/access.log", encoding="utf-8") as access_file:
    for line in access_file:
        fields = line.split()
        source_fields = [field for field in fields if field.startswith("src=")]

        if not source_fields:
            continue

        ip_address = source_fields[0].split("=", 1)[1]

        if ip_address in suspicious_ips:
            matches[ip_address] = matches.get(ip_address, 0) + 1