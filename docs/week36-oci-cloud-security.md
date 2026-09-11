# Week 36 OCI Cloud Security Lab
## 1. Min OCI-miljö/Min lokala Linux-miljö/Min lokala WSL-miljö
- Tenancy (N/A): Lokal Linux-vm
- Compartment (Endast OCI):
- Region (Endast OCI):
- Availability Domain (Endast OCI):
- VM-namn/hostnamn/WSL-maskinnamn: itsx26-edvin-vm
- Operativsystem:Linux/Ubuntu
- Shape (Hårdvara, gäller alla): Virtualbox 1 CPU och 4096MB RAM
- Inloggningsmetod: SSH med användarnamnet admin och VM:ens IP-adress 
---
## 2. Linux-kommandon
| Kommando | Vad visar det? | CIA-koppling |
|-----------|-----------|-----------|
| whoami |Visar vilken användare som är inloggad.|Konfidentialitet–användarens identitet avgör vilka resurser och filer användaren får åtkomst till.|
| hostname |Visar namnet på datorn/servern.|Integritet – hjälper till att kontrollera att man arbetar mot rätt system.|
| pwd |Visar vilken katalog/sökväg man befinner sig i.|Integritet – hjälper till att kontrollera att man arbetar i rätt katalog.|
| uname -a |Visar information om Linux-kärnan, version och systemarkitektur.|Integritet – informationen kan användas för att kontrollera systemets version och konfiguration.|
| uptime |Visar hur länge systemet varit igång, antal användare och systemets belastning.|Tillgänglighet – visar information om systemets drifttid och status.|
---
## 3. Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
|Kontroll 1 – Identitet och behörigheter|För höga administrativa rättigheter kan göra att en användare kan ändra viktiga delar av systemet.|Jag körde whoami, id och groups för att kontrollera min användare och mina grupper.|Jag såg att jag är inloggad som admin och tillhör grupperna admin och sudo.|Konfidentialitet / Integritet|
|Kontroll 2 – Filrättigheter|Obehöriga användare kan läsa eller ändra filer.|Jag skapade test.txt med touch och ändrade rättigheterna till 600 med chmod 600 test.txt.|Jag använde ls -l test.txt före och efter ändringen. Efteråt kunde endast ägaren läsa och skriva till filen.|Konfidentialitet|
|Kontroll 3 – Systemuppdateringar|Föråldrad programvara kan innehålla kända säkerhetssårbarheter.|Jag körde sudo apt update och apt list --upgradable för att kontrollera om det fanns uppdateringar.|Jag kontrollerade resultatet från kommandona för att se om det fanns tillgängliga uppdateringar.|Integritet|
|Kontroll 6 – SSH|Om SSH är felaktigt konfigurerat kan obehöriga få tillgång till servern.|Jag loggade in på Linux-VM:n från min Mac med SSH genom att använda användarnamnet admin och VM:ns IP-adress.|Jag verifierade anslutningen genom att köra kommandon som whoami, hostname och pwd efter SSH-inloggningen.|Konfidentialitet|
---
## 4. Recovery-plan
### Vad kan gå fel?

SSH kan sluta fungera, servern kan sluta svara, nätverket kan vara felkonfigurerat eller VM:n kan försvinna.

### Hur upptäcker jag problemet?

Jag upptäcker problemet när jag inte längre kan ansluta till servern via SSH eller får ett felmeddelande från SSH.

### Vad kontrollerar jag först?

Jag kontrollerar först att VM:n är igång, att nätverket fungerar, att IP-adressen är korrekt och att SSH-tjänsten körs.

### Hur återställer jag åtkomst?

Jag kontrollerar SSH-tjänsten med:

### När behöver jag hjälp?

Om jag inte kan lösa problemet efter att ha kontrollerat servern, nätverket och SSH skulle jag samla in felmeddelanden och annan relevant information och sedan be läraren eller en administratör om hjälp.

---
## 5. Backup
### Vad har jag sparat?

Jag har sparat mina scripts, dokumentation och annat arbete som jag har lagt i GitHub.

### Vad finns i GitHub?

Mitt arbete som jag har pushat till GitHub, exempelvis scripts och dokumentation.

### Vad kan återskapas?

Jag kan skapa en ny Linux-VM, installera de program som behövs och hämta mina scripts och dokumentation från GitHub.

### Vad går inte att återskapa?

Filer, inställningar och program som endast fanns lokalt på den gamla VM:n och inte hade säkerhetskopierats kan gå förlorade.

---
## 6. Cleanup
### VM-instans

Jag kontrollerar att VM:n finns kvar och stänger av den om den inte längre behöver vara igång.

### Diskar

Jag kontrollerar att det inte finns onödiga diskar kopplade till VM:n.

### Backuper

Jag kontrollerar att eventuella backuper eller snapshots som behövs finns kvar.

### Publika IP-adresser

Jag kontrollerar att VM:n inte har någon onödig publik IP-adress.

### GitHub-evidens

Jag kontrollerar att mitt arbete är sparat och pushat till GitHub.

---
## 7. CIA-reflektion
### Konfidentialitet

Jag har arbetat med användarbehörigheter och filrättigheter. Exempelvis gjorde chmod 600 så att endast filens ägare kunde läsa och ändra filen. SSH skyddar dessutom kommunikationen genom kryptering.

### Integritet

Jag har kontrollerat systemets användare, grupper, filer, processer och systeminformation. Uppdateringar är också viktiga eftersom de kan åtgärda säkerhetssårbarheter och hjälpa till att hålla systemet korrekt och säkert.

### Tillgänglighet

Jag har använt uptime för att kontrollera systemets drifttid och status. Jag har även lärt mig hur SSH och nätverket kan felsökas om åtkomsten till servern försvinner.

---
## 8. Reflektion
### Vad fungerade bra?

Jag kunde ansluta till Linux-VM:n via SSH och använda olika Linux-kommandon för att undersöka systemet. Jag kunde även kontrollera användare, grupper, filrättigheter och processer.

### Vad var svårt?

Det var svårt att konfigurera SSH-anslutningen och förstå skillnaden mellan VM:ns nätverksanslutning och Macens nätverk. Det var även lite svårt att förstå hur filrättigheter och sudo fungerar.

### Vad lärde jag mig?

Jag lärde mig hur man ansluter till en Linux-server med SSH och hur man använder grundläggande Linux-kommandon. Jag lärde mig även hur användarbehörigheter, filrättigheter, processer och uppdateringar påverkar säkerheten. Dessutom lärde jag mig hur CIA-triaden – Confidentiality, Integrity och Availability – kan användas för att tänka kring säkerheten i ett system.
