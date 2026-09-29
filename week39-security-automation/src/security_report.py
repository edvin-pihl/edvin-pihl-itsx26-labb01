with open("data/suspicious_ips.txt", "r") as file:
    suspicious_ips = {line.strip() for line in file}


failed_login_count = 0
failed_login_ips = {}
matched_ips = set()
observed_ips = set()
skipped_lines = 0

with open("data/auth.log", "r") as file:
    for line in file:

        if not line.startswith("2026-"):
            skipped_lines += 1
            continue

        parts = line.split()

        for part in parts:
            if part.startswith("src="):
                ip_address = part.replace("src=", "")
                observed_ips.add(ip_address)

        if "Failed login" in line:
            failed_login_count += 1

            parts = line.split()

            for part in parts:
                if part.startswith("src="):
                    ip_address = part.replace("src=", "")

                    if ip_address in suspicious_ips:
                        matched_ips.add(ip_address)

                    if ip_address in failed_login_ips:
                        failed_login_ips[ip_address] += 1
                    else:
                        failed_login_ips[ip_address] = 1


unauthorized_count = 0
unauthorized_ips = {}

with open("data/access.log", "r") as file:
    for line in file:
        parts = line.split()

        for part in parts:
            if part.startswith("src="):
                ip_address = part.replace("src=", "")
                observed_ips.add(ip_address)

        if "status=401" in line:
            unauthorized_count += 1

            parts = line.split()

            for part in parts:
                if part.startswith("src="):
                    ip_address = part.replace("src=", "")

                    if ip_address in unauthorized_ips:
                        unauthorized_ips[ip_address] += 1
                    else:
                        unauthorized_ips[ip_address] = 1
                    if ip_address in suspicious_ips:
                        matched_ips.add(ip_address)


blocked_count = 0
blocked_ips = {}

with open("data/firewall.log", "r") as file:
    for line in file:
        parts = line.split()

        for part in parts:
            if part.startswith("src="):
                ip_address = part.replace("src=", "")
                observed_ips.add(ip_address)

        if "DENY" in line or "DROP" in line:
            blocked_count += 1

            parts = line.split()  

            for part in parts:
                if part.startswith("src="):
                    ip_address = part.replace("src=", "")

                    if ip_address in blocked_ips:
                        blocked_ips[ip_address] += 1
                    else:
                        blocked_ips[ip_address] = 1
                
                    if ip_address in suspicious_ips:
                        matched_ips.add(ip_address)


print("Antal misslyckade inloggningar:", failed_login_count)
print("Misslyckade inloggningar per IP:")
print(failed_login_ips)

print("Hoppade felaktiga rader:", skipped_lines)

print("Observerade käll-IP-adresser:")
for ip in sorted(observed_ips):
    print(ip)

print("Matchade IP-adresser:")
for ip in sorted(matched_ips):
    print(ip)

print("Antal HTTP 401:", unauthorized_count)
print("HTTP 401 per IP:")
print(unauthorized_ips)

print("Antal blockerade brandvägshändelser:", blocked_count)
print("Blockerade händelser per IP:")
print(blocked_ips)

# AI-stöd:
# Den här delen för att strukturera och skriva resultatet till security_report.txt
# skapades med hjälp av ChatGPT. Jag har själv gått igenom koden och verifierat
# resultatet genom att köra programmet och jämföra rapporten med loggfilerna.

with open("output/security_report.txt", "w") as report:
    report.write("SECURITY AUTOMATION REPORT\n")
    report.write("==========================\n\n")

    report.write("Analyserade filer:\n")
    report.write("- data/auth.log\n")
    report.write("- data/access.log\n")
    report.write("- data/firewall.log\n")
    report.write("- data/suspicious_ips.txt\n\n")

    report.write("AUTHENTICATION\n")
    report.write(f"Antal misslyckade inloggningar: {failed_login_count}\n")

    for ip, count in sorted(failed_login_ips.items()):
        report.write(f"- {ip}: {count}\n")

    report.write("\nWEB ACCESS\n")
    report.write(f"Antal HTTP 401: {unauthorized_count}\n")

    for ip, count in sorted(unauthorized_ips.items()):
        report.write(f"- {ip}: {count}\n")

    report.write("\nFIREWALL\n")
    report.write(f"Antal blockerade brandväggshändelser: {blocked_count}\n")

    for ip, count in sorted(blocked_ips.items()):
        report.write(f"- {ip}: {count}\n")

    report.write("\nOBSERVERADE KÄLL-IP-ADRESSER\n")
    for ip in sorted(observed_ips):
        report.write(f"- {ip}\n")

    report.write("\nIOC-MATCHNINGAR\n")

    for ip in sorted(matched_ips):
        report.write(f"- {ip}\n")

    report.write("\nDATAKVALITET\n")
    report.write(f"Antal hoppade felaktiga rader: {skipped_lines}\n")

    report.write("\nOBSERVATION\n")
    report.write(
        "203.0.113.15 förekommer i misslyckade inloggningar, "
        "HTTP 401-händelser och blockerad brandväggstrafik. "
        "Adressen finns även i IOC-listan.\n"
    )

    report.write("\nBEGRÄNSNING\n")
    report.write(
        "En IOC-matchning eller flera säkerhetsrelaterade händelser "
        "bevisar inte att IP-adressen tillhör en angripare.\n"
    )