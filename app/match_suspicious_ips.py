with open("data/suspicious_ips.txt", "r") as file:
    suspicious_ips = {line.strip() for line in file}

match_count = 0
matched_ips = set()
skipped_line = 0

with open("data/access.log", "r") as file:
    for line in file:
        parts = line.split()

        if len(parts) >= 2:
            ip_address = parts[1].replace("src=", "")

            if ip_address in suspicious_ips:
                match_count += 1
                matched_ips.add(ip_address)
            
        else:
            skipped_line += 1
        
print("Dataset: data/access.log")
print("Misstänkta IP-adresser: data/suspicious_ips.txt")

print("Antal matchade loggrader:", match_count)

print("Matchade IP-adresser:")
for ip in matched_ips:
    print(ip)

print("Bortfall:", skipped_line)