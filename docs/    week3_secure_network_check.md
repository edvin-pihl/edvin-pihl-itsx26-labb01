# Del A – Miljöbeskrivning

Jag använder en lokal Linux-VM med Ubuntu i VirtualBox på min Mac.

Operativsystemet är Ubuntu 26.04.1 LTS (Resolute Raccoon) och datornamnet är itsx26-edvin-vm.

Min VM har två nätverksinterface:

* lo – loopback-interface med adressen 127.0.0.1.
* enp0s8 – det aktiva nätverksinterfacet med den privata IPv4-adressen 192.168.0.115/24.

Interfacet enp0s8 har även en lokal IPv6-adress.

Min default route går via gatewayen 192.168.0.1 genom interfacet enp0s8.

127.0.0.1 är en lokal adress som endast används inom den egna datorn. 192.168.0.115 är en privat IP-adress som används inom mitt lokala nätverk. Min VM har ingen egen direkt publik IP-adress i den här miljön.

Lärardemonstrationen genomförs i Oracle Cloud Infrastructure, medan jag arbetar i en lokal Ubuntu-VM i VirtualBox. Därför skiljer sig bland annat nätverksinterface, IP-adresser och routing från lärarens miljö, men kontrollerna har samma syfte.

# Del B – Manuella observationer

Del B – Manuella observationer

Jag genomförde sex manuella kontroller för att undersöka nätverkskonfiguration, DNS, portar, lokal tjänst och processer i min Ubuntu-VM.

**Kontroll 1 – Interface och IP-adresser**

Jag använde kommandot:

ip addr

Jag identifierade två nätverksinterface:

* lo – loopback-interface med IPv4-adressen 127.0.0.1.
* enp0s8 – det aktiva nätverksinterfacet med IPv4-adressen 192.168.0.115/24.

lo används för lokal kommunikation inom den egna Linuxmiljön.

enp0s8 är interfacet som min virtuella maskin använder för kommunikation med det lokala nätverket.

IP-adressen 192.168.0.115 är en privat IPv4-adress.

Jag kunde även se att enp0s8 hade en lokal IPv6-adress.



**Kontroll 2 – Routing**

Jag använde kommandot:

ip route

Resultatet visade följande default route:

default via 192.168.0.1 dev enp0s8

Det innebär att trafik som ska skickas utanför mitt lokala nätverk går via gatewayen 192.168.0.1 genom nätverksinterfacet enp0s8.

Mitt lokala nätverk är:

192.168.0.0/24

Default route visar alltså vilken väg systemet normalt använder när destinationen inte finns direkt i det lokala nätverket.



**Kontroll 3 – DNS**

Jag använde kommandot:

nslookup google.com

Resultatet blev:

Server:         127.0.0.53
Address:        127.0.0.53#53
Non-authoritative answer:
Name:   google.com
Address: 172.217.20.174
Name:   google.com
Address: 2a00:1450:400f:80f::200e

Resultatet visar att DNS fungerar i min Linuxmiljö eftersom domännamnet google.com kunde översättas till både en IPv4-adress och en IPv6-adress.

DNS-servern visas som 127.0.0.53, vilket är den lokala DNS-resolver som Ubuntu använder för att hantera DNS-frågor.

Jag testade även example.com, men fick då NXDOMAIN. Eftersom google.com kunde slås upp korrekt kunde jag bekräfta att DNS-funktionen i miljön fungerade.



**Kontroll 4 – Portar och tjänster**

Jag använde kommandot:

ss -tuln

Resultatet visade bland annat:
tcp LISTEN 0 5    127.0.0.1:8080       0.0.0.0:*
tcp LISTEN 0 4096 0.0.0.0:22           0.0.0.0:*
tcp LISTEN 0 4096 127.0.0.53%lo:53     0.0.0.0:*
tcp LISTEN 0 4096 [::]:22               [::]:*

Port 8080 användes av den lokala HTTP-servern som jag startade för testet. Eftersom tjänsten lyssnade på 127.0.0.1 var den endast tillgänglig lokalt på VM:n.

Port 22 används av SSH. Jag använder SSH för att ansluta från min Mac till Ubuntu-VM:n.

Port 53 används för DNS-funktionalitet lokalt i systemet.

Kontrollen visar vilka lokala portar som lyssnar efter anslutningar och ger information om vilka tjänster som är aktiva i systemet.



**Kontroll 5 – Lokal tjänst**

Jag startade en lokal HTTP-server med kommandot:

python3 -m http.server 8080 --bind 127.0.0.1

Terminalen visade:
Serving HTTP on 127.0.0.1 port 8080 (http://127.0.0.1:8080/) ...

Det visar att webbservern startades på localhost och port 8080.

Jag kunde även se med ss -tuln att port 8080 började lyssna på adressen 127.0.0.1.

Mitt Bash-verktyg kunde därefter kontrollera tjänsten och gav resultatet:
[OK] Lokal tjänst svarar på port 8080

Det visar att den lokala tjänsten gick att nå när webbservern var igång.

När webbservern inte var startad fick jag i stället:
[FAIL] Ingen lokal tjänst svarar på port 8080

Det visar att kontrollen kan skilja mellan en tillgänglig och en otillgänglig lokal tjänst.

Efter testningen stoppade jag webbservern med Ctrl+C.


**Kontroll 6 – Process eller systemstatus**

Jag använde kommandot:

ps aux | head

för att kontrollera vilka processer som kördes i systemet.

Resultatet visade bland annat systemprocessen systemd och flera kernel-processer.

Exempel:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.5  26480 17332 ?        Ss   16:20   0:00 /usr/lib/systemd/systemd --switched-root
root         2  0.0  0.0      0     0 ?        S    16:20   0:00 [kthreadd]

Den lokala HTTP-servern kördes med processen python3 genom kommandot:

python3 -m http.server 8080 --bind 127.0.0.1

Det innebär att processen python3 körde HTTP-tjänsten som lyssnade på port 8080.

Kontrollen visar sambandet mellan process, tjänst och port: en process kör tjänsten och tjänsten lyssnar på en nätverksport.


# Del C – Bash-verktyget

Jag skapade skriptet:

script/secure_network_check.sh

Syftet med skriptet är att automatiskt kontrollera grundläggande nätverksfunktioner i min Linuxmiljö.

Skriptet arbetar endast mot localhost, lokala portar och ett definierat domännamn. Det genomför ingen extern portskanning.

Skriptet innehåller följande kontroller:

* nätverksinformation och default route
* DNS-uppslag
* lokalt lyssnande portar
* lokal tjänst på port 8080
* sammanfattning av lyckade och misslyckade kontroller

Skriptet använder variabler för bland annat domännamn, testport och loggkatalog.

Det använder även funktioner för att dela upp de olika kontrollerna, bland annat:

* log_message
* check_environment
* check_dns
* check_ports
* check_local_service
* cleanup
* summary

För att göra resultatet tydligt används statusarna:

* INFO
* OK
* WARN
* FAIL

Skriptet skapar även en tidsstämplad loggfil i:

/home/admin/secure-network-logs/

Ett exempel på en loggfil är:

network_check_2026-09-18_09-38-05.log

Skriptet avslutas med exitkod 0 om alla kontroller lyckas och exitkod 1 om minst en kontroll misslyckas.

Exempel på lyckad körning

När DNS fungerade och den lokala webbservern kördes lyckades samtliga kontroller.

Resultatet blev:
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
[OK] Lokal tjänst svarar på port 8080
[INFO] Cleanup genomfört


Sammanfattningen visade:
Lyckades: 4
Misslyckades: 0

# Del D – Testning

Jag genomförde två normalfall och två felfall för att kontrollera att skriptet fungerar både när tjänster fungerar korrekt och när fel uppstår.

**Testfall 1 – Fungerande DNS**

Test:
DNS-uppslag genomfördes mot google.com.

Förväntat resultat:
DNS-uppslaget ska lyckas och skriptet ska visa status OK.

Faktiskt resultat:
[OK] DNS-uppslag fungerade för google.com

Slutsats:
Testet lyckades. Skriptet kunde kontrollera att DNS fungerade och hanterade ett fungerande DNS-uppslag korrekt.

**Testfall 2 – Lokal tjänst fungerar**

Jag startade en lokal webbserver med:
python3 -m http.server 8080 --bind 127.0.0.1

Förväntat resultat:
Skriptet ska kunna nå den lokala tjänsten på port 8080 och visa status OK.

Faktiskt resultat:
[OK] Lokal tjänst svarar på port 8080

Slutsats:
Testet lyckades. Skriptet kunde identifiera att den lokala tjänsten var tillgänglig.

**Testfall 3 – Misslyckat DNS-uppslag**

Jag testade tidigare DNS-uppslag mot example.com.

Förväntat resultat:
Om DNS-uppslaget inte lyckas ska skriptet visa FAIL utan att krascha.

Faktiskt resultat:
[FAIL] DNS-uppslag misslyckades för example.com

Vid en manuell kontroll med:
nslookup example.com

fick jag:
server can't find example.com: NXDOMAIN

Jag testade därefter google.com, vilket fungerade korrekt.

Slutsats:
Skriptet hanterade det misslyckade DNS-uppslaget korrekt utan att krascha. Eftersom google.com kunde slås upp korrekt kunde jag även bekräfta att DNS-funktionen i min Linuxmiljö fungerade.

**Testfall 4 – Ingen lokal tjänst på port 8080**

Jag körde skriptet utan att den lokala webbservern var startad.

Förväntat resultat:
Skriptet ska upptäcka att ingen lokal tjänst svarar på port 8080 och visa FAIL.

Faktiskt resultat:
[FAIL] Ingen lokal tjänst svarar på port 8080

Skriptets sammanfattning visade då:
Lyckades: 3
Misslyckades: 1

Slutsats:
Skriptet upptäckte korrekt att den lokala tjänsten inte var tillgänglig och hanterade felet utan att krascha.

# Del E – CIA-analys

**Konfidentialitet**

Nätverksutdata kan innehålla information som kan vara känslig.

Exempel på sådan information är:

* IP-adresser
* hostnames
* MAC-adresser
* nätverksinterface
* öppna och lyssnande portar
* information om aktiva tjänster
* information från loggfiler

Denna information kan ge en utomstående bättre förståelse för hur ett system eller nätverk är uppbyggt.

Innan jag publicerar terminalutdata eller loggar i GitHub granskar jag därför innehållet och tar bort eller maskerar information som inte behöver vara offentlig.

Lösenord, privata nycklar, tokens och andra hemligheter ska aldrig finnas i skriptet, loggfilerna eller GitHub-repot.



Integritet

Integritet handlar bland annat om att kunna lita på att resultatet är korrekt och spårbart.

Mitt verktyg skapar tidsstämplade loggfiler, vilket gör att jag kan se när en kontroll genomfördes och vilket resultat den gav.

Statusarna INFO, OK, WARN och FAIL gör resultaten tydligare och minskar risken för att de misstolkas.

Git och GitHub ger dessutom versionshistorik för skriptet. Det gör det möjligt att se vilka ändringar som har gjorts i koden över tid.

Genom att kombinera loggar, tydliga statusmeddelanden och versionshistorik blir det enklare att kontrollera hur ett resultat har uppstått och att upptäcka förändringar i verktyget.



Tillgänglighet

Verktyget använder flera kontroller för att undersöka om nätverket och tjänster är tillgängliga.

Routing:
ip route kontrollerar att systemet har en default route och därmed en väg till nätverk utanför det lokala nätverket.

DNS:
DNS-kontrollen verifierar att ett domännamn kan översättas till en IP-adress. Om DNS inte fungerar kan tjänster som använder domännamn bli otillgängliga även om nätverket i övrigt fungerar.

Portar:
ss -tuln visar vilka lokala portar som lyssnar och ger information om vilka tjänster som är redo att ta emot anslutningar.

Lokal tjänst:
Kontrollen med curl verifierar att den lokala tjänsten på port 8080 faktiskt går att nå och svarar.

Tillsammans gör kontrollerna det möjligt att skilja mellan olika typer av nätverksproblem. En fungerande route betyder exempelvis inte automatiskt att DNS eller en specifik tjänst fungerar.



Avvägning mellan säkerhet och tillgänglighet

Ett exempel på en säkerhetsåtgärd som kan påverka tillgängligheten är en brandvägg.

En korrekt konfigurerad brandvägg förbättrar säkerheten genom att blockera trafik och portar som inte behövs.

Om brandväggen konfigureras fel kan den däremot blockera en tjänst som faktiskt behövs.

I min miljö skulle ett exempel vara att SSH-porten blockeras. Eftersom jag använder SSH för att administrera Ubuntu-VM:n från min Mac skulle jag då inte längre kunna ansluta till systemet.

Det visar att en säkerhetsåtgärd måste testas efter konfiguration så att säkerheten förbättras utan att nödvändiga funktioner blir otillgängliga.


# Del F – Reflektion och förbättring

**Vilken kontroll gav mest värde och varför?**

Kontrollen av den lokala tjänsten gav mest värde eftersom den inte bara visar att en port finns, utan även verifierar att tjänsten faktiskt går att nå.

När webbservern inte var startad fick jag:

[FAIL] Ingen lokal tjänst svarar på port 8080

När jag sedan startade webbservern ändrades resultatet till:

[OK] Lokal tjänst svarar på port 8080

Det gjorde det tydligt hur verktyget kan användas för att skilja mellan en fungerande och en otillgänglig tjänst.



**Vilken miljöskillnad påverkade mitt arbete?**

Lärardemonstrationen genomförs i Oracle Cloud Infrastructure medan jag använder Ubuntu i en lokal VirtualBox-VM på min Mac.

Det innebär att nätverksinterface, IP-adresser och delar av nätverkskonfigurationen ser annorlunda ut.

Min VM använder exempelvis interfacet enp0s8 och en privat adress i mitt lokala nätverk.

Jag använder dessutom Ubuntu, som använder pakethanteraren apt. Vissa Linuxinstruktioner använder i stället dnf, vilket inte är rätt pakethanterare för min Ubuntu-miljö.

Trots skillnaderna kan jag genomföra samma typer av kontroller och uppnå samma kontrollsyfte.



**Vilket fel var svårast att tolka?**

Ett av de svårare felen uppstod när SSH-anslutningen mellan min Mac och Ubuntu-VM:n bröts.

Jag fick bland annat:

No route to host
Broken pipe

Det visade att SSH-klienten inte längre kunde nå VM:n över nätverket.

Felet var svårare att tolka eftersom problemet inte låg i SSH-kommandot i sig, utan i nätverksanslutningen mellan datorn och VM:n.

Efter att nätverksanslutningen fungerade igen kunde jag ansluta med SSH som vanligt.



**Vad skulle jag förbättra i version 2?**

I en version 2 skulle jag göra verktyget mer portabelt och robust.

Skriptet skulle exempelvis kunna kontrollera vilka DNS-verktyg som finns installerade och automatiskt välja mellan:

* getent
* nslookup
* dig

Jag skulle även kunna förbättra loggningen genom att lägga till mer detaljerad information om varför en kontroll misslyckades.

En annan förbättring skulle vara att automatisera hanteringen av en tillfällig lokal testserver så att skriptet själv kan starta och stoppa den på ett kontrollerat sätt.



**Hur kan verktyget användas i verklig drift utan att bli riskabelt?**

Verktyget skulle kunna användas som en enkel hälsokontroll av en Linuxserver.

Det skulle exempelvis kunna köras efter:

* systemuppdateringar
* återställning från backup
* nätverksändringar
* ändringar i brandvägg eller säkerhetsinställningar
* installation eller förändring av tjänster

Verktyget skulle då snabbt kunna kontrollera om routing, DNS, lokala portar och viktiga tjänster fortfarande fungerar.

För att verktyget inte ska bli riskabelt bör det endast arbeta mot den egna miljön eller uttryckligen godkända mål. Det ska inte användas för extern portskanning eller för att samla information från system som användaren inte har tillstånd att testa.



**Säkerhetsregler**

Under uppgiften har jag endast arbetat mot min egen Ubuntu-VM, localhost, min egen gateway och google.com för att kontrollera att DNS-funktionen i skriptet fungerade. google.com användes endast för DNS-uppslag och ingen portskanning eller annan aktiv testning genomfördes mot domänen.

Jag har inte genomfört någon nätverks- eller portskanning mot andra system.

Jag har inte ändrat brandväggsregler eller blockerat SSH som en del av uppgiften.

Skriptet innehåller inga hårdkodade lösenord, privata nycklar eller tokens.

Jag kör inte hela skriptet med sudo, eftersom kontrollerna i skriptet inte kräver administrativa rättigheter.

Den lokala webbservern används endast under testningen och stoppas med Ctrl+C efter att testet är färdigt.

Skriptet skapar inga temporära filer som behöver tas bort. Loggfilerna sparas avsiktligt som dokumentation av kontrollerna.



**AI-användning**

Jag använde ChatGPT som stöd under uppgiften.

Jag använde AI för att:

* tolka delar av uppgiftsinstruktionen
* förstå hur Bash-skriptet kunde struktureras
* felsöka syntax- och variabelfel i skriptet
* förstå vissa nätverkskommandon och felmeddelanden
* strukturera dokumentationen

Jag använde inte AI-resultat utan kontroll. Jag körde själv kommandona och skriptet i min Ubuntu-VM och verifierade resultaten genom både normalfall och felfall.

Jag testade bland annat DNS, routing, lokala portar och en lokal HTTP-tjänst.

Jag anpassade själv skriptet till min miljö och ansvarar för att kunna förklara hur kontrollerna och koden fungerar.



**Leverabler och inlämning**

Följande filer ingår i min inlämning:

Bash-skript

scripts/secure_network_check.sh

Individuell rapport

docs/week3_secure_network_check.md

Evidens

Relevant och sanerad exempelutdata finns i rapporten och vid behov i:

evidence/

I Canvas lämnar jag direktlänkar till rapporten och Bash-skriptet i GitHub-repot.

Jag laddar alltså inte upp själva filerna separat i Canvas.

Innan inlämning kontrollerar jag länkarna i ett privat webbläsarfönster för att säkerställa att de går att öppna.



**Definition of Done**

Före inlämning kontrollerar jag att:

* Bash-skriptet går att läsa och köra.
* Skriptets obligatoriska funktioner finns.
* Två normalfall och två felfall är dokumenterade.
* Loggen innehåller tidsstämpel och tydliga statusar.
* Rapporten innehåller förklaringar av resultaten.
* CIA-analysen är kopplad till mina faktiska kontroller.
* Skillnaden mellan VirtualBox och OCI är dokumenterad.
* Cleanup och hantering av testserver är beskriven.
* Inga lösenord, tokens eller privata nycklar finns i repot.
* AI-användningen är dokumenterad.
* GitHub-länkarna är kontrollerade och inlagda i Canvas.