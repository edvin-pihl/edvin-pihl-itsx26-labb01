# Evidence – Secure Network Check

Den här filen innehåller sanerad exempelutdata från tester av secure_network_check.sh.

**Normalfall 1 – DNS fungerar**

DNS-kontrollen kördes mot google.com.

Relevant output:

[INFO] Kontrollerar DNS för google.com
[OK] DNS-uppslag fungerade för google.com

Detta visar att skriptet kunde genomföra ett fungerande DNS-uppslag.



**Normalfall 2 – Lokal tjänst svarar**

En lokal HTTP-server startades med:

python3 -m http.server 8080 --bind 127.0.0.1

Därefter kördes:

./secure_network_check.sh

Relevant output:

[INFO] Kontrollerar localhost på port 8080
[OK] Lokal tjänst svarar på port 8080

När alla kontroller fungerade visade skriptet:

Lyckades: 4
Misslyckades: 0

Detta visar att skriptet kunde identifiera att den lokala tjänsten var tillgänglig på port 8080.

Efter testet stoppades webbservern med Ctrl+C.



**Felfall 1 – Ogiltigt domännamn**

DNS-målet ändrades till ett medvetet ogiltigt domännamn för att kontrollera skriptets felhantering.

Testdomän:
finns-inte-test.invalid

Relevant output:

[INFO] Kontrollerar DNS för finns-inte-test.invalid
[FAIL] DNS-uppslag misslyckades för finns-inte-test.invalid

Skriptet ska ge FAIL för DNS-kontrollen men fortsätta köra övriga kontroller utan att krascha.

I samma körning var även den lokala tjänsten på port 8080 avstängd, vilket gjorde att sammanfattningen blev:

Lyckades: 2
Misslyckades: 2


**Felfall 2 – Ingen lokal tjänst på port 8080**

Skriptet kördes när ingen lokal HTTP-server var startad på port 8080.

Relevant output:

[INFO] Kontrollerar localhost på port 8080
[FAIL] Ingen lokal tjänst svarar på port 8080

Sammanfattningen visade:

Lyckades: 3
Misslyckades: 1

Detta visar att skriptet kunde upptäcka att tjänsten inte var tillgänglig och hantera felet utan att krascha.



**Exempel på full körning med ett misslyckat test**

[INFO] Godkänt lokalt mål: localhost
[INFO] Godkänt lokalt mål: 127.0.0.1
[INFO] Secure Network Check startar
[INFO] Kontrollerar nätverksmiljö
[OK] Default route hittades
[INFO] Kontrollerar DNS för google.com
[OK] DNS-uppslag fungerade för google.com
[INFO] Kontrollerar lokalt lyssnande portar
[OK] Portöversikt skapades
[INFO] Kontrollerar localhost på port 8080
[FAIL] Ingen lokal tjänst svarar på port 8080
[INFO] Cleanup genomfört
==============================
 Secure Network Check
==============================
Lyckades: 3
Misslyckades: 1
Loggfil: /home/admin/secure-network-logs/network_check_2026-09-18_09-38-05.log



**Loggning**

Skriptet skapar en tidsstämplad loggfil i:

/home/admin/secure-network-logs/

Exempel:

network_check_2026-09-18_09-38-05.log

Loggfilen innehåller bland annat:

* tidsstämplade statusmeddelanden
* IP- och adressinformation
* routinginformation
* resultat från DNS-kontrollen
* lokalt lyssnande portar
* resultat från tjänstekontrollen


**Sanering**

Evidensen har granskats innan publicering.

Inga lösenord, privata nycklar, tokens eller andra hemligheter inkluderas i denna fil.

DNS-kontrollen mot google.com användes endast för namnuppslag. Ingen portskanning eller annan aktiv testning genomfördes mot domänen.