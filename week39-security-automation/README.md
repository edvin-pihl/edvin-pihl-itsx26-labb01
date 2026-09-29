# Security Automation Report – Week 39

## Syfte

Syftet med projektet är att skapa ett defensivt analysverktyg i Python som analyserar syntetiska loggfiler och omvandlar informationen till verifierbara säkerhetsobservationer.

Programmet analyserar autentiseringsloggar, webbloggar och brandväggsloggar. Det identifierar och räknar utvalda säkerhetsrelevanta händelser, sammanställer observerade käll-IP-adresser och jämför adresserna mot en lokal IOC-lista.

Resultatet sammanställs automatiskt i `output/security_report.txt`.

## Dataset

Jag använde **Dataset A: Basic**.

Följande filer analyseras:

- `data/auth.log`
- `data/access.log`
- `data/firewall.log`
- `data/suspicious_ips.txt`

Datasetet är syntetiskt och tillhandahållet för kursuppgiften.

Originalfilerna används som indata och ändras inte av programmet.

## Pythonversion

Programmet är utvecklat och testat med:

`Python 3.9.6`

Pythonversionen kan kontrolleras med:

```bash
python3 --version
```

## Körinstruktion

Programmet ska köras från projektroten:

`week39-security-automation/`

Programmet startas med:

```bash
python3 src/security_report.py
```

Programmet läser indata från `data/` och genererar rapporten:

`output/security_report.txt`

Om programmet körs igen med samma indata skapas rapporten på nytt utifrån samma analys.

## Projektstruktur

```text
week39-security-automation/
├── README.md
├── data/
│   ├── auth.log
│   ├── access.log
│   ├── firewall.log
│   └── suspicious_ips.txt
├── src/
│   └── security_report.py
├── output/
│   └── security_report.txt
├── docs/
│   └── analysis.md
└── tests/
    └── test_data/
        ├── positive
        ├── zero_hits
        └── malformed
```

`tests/` är en extra mapp som innehåller den testdata som användes för att verifiera autentiseringsanalysen.

## Hur programmet fungerar

Programmet börjar med att läsa `data/suspicious_ips.txt` och lagrar indikatoradresserna för senare jämförelse.

Därefter analyseras de tre loggkällorna:

- I `auth.log` söker programmet efter `Failed login` och räknar misslyckade inloggningar per käll-IP.
- I `access.log` söker programmet efter HTTP-status `401` och räknar dessa händelser per käll-IP.
- I `firewall.log` söker programmet efter `DENY` och `DROP` och räknar blockerade händelser per käll-IP.

Programmet extraherar även käll-IP-adresser från giltiga loggrader i de tre loggkällorna och sammanställer dem som observerade käll-IP-adresser.

De observerade käll-IP-adresserna jämförs därefter mot adresserna i `suspicious_ips.txt`. På så sätt kan programmet skilja mellan alla observerade adresser och de adresser som även finns i IOC-listan.

Programmet hanterar även den felaktigt formaterade raden i `auth.log` genom att hoppa över den och redovisa hur många rader som hoppades över.

Resultatet skrivs därefter till `output/security_report.txt`.

## Testning

Programmet verifierades med tre separata testfall för autentiseringsanalysen. Testfilerna finns i `tests/test_data/`.

Under testerna ändrades sökvägen till `auth.log` tillfälligt så att programmet läste respektive testfil. Övriga datakällor ändrades inte.

### Test 1 – Känt positivt utfall

Testfilen `positive` innehöll två misslyckade inloggningar från `203.0.113.15`.

Manuellt förväntat resultat:

- 2 misslyckade inloggningar
- `203.0.113.15`: 2
- 0 hoppade rader

Programmet gav samma resultat.

### Test 2 – Noll träffar

Testfilen `zero_hits` innehöll två lyckade inloggningar och inga misslyckade inloggningar.

Manuellt förväntat resultat:

- 0 misslyckade inloggningar
- inga IP-adresser med misslyckade inloggningar
- 0 hoppade rader

Programmet gav samma resultat.

### Test 3 – Formatfel

Testfilen `malformed` innehöll en korrekt misslyckad inloggning från `203.0.113.15` och en felaktigt formaterad rad.

Manuellt förväntat resultat:

- 1 misslyckad inloggning
- `203.0.113.15`: 1
- 1 hoppad felaktig rad

Programmet gav samma resultat och fortsatte körningen efter den felaktiga raden.

Efter testningen återställdes programmet till `data/auth.log` och kördes på nytt mot Basic-datasetet.

En mer detaljerad beskrivning av testningen och resultaten finns i `docs/analysis.md`.

## Kända begränsningar

Programmet analyserar endast de säkerhetsrelevanta mönster som har definierats i koden:

- `Failed login`
- HTTP 401
- `DENY`
- `DROP`

Andra säkerhetsrelevanta händelser kan därför finnas i loggarna utan att identifieras.

Programmet är utvecklat utifrån formatet i kursens Basic-dataset. Om loggformatet förändras kan programmet behöva anpassas.

Formatkontrollen av `auth.log` är enkel och anpassad efter den aktuella datan. Programmet är därför inte en generell parser för alla typer av loggfiler.

De tre separata testfallen fokuserar på autentiseringsanalysen. Webbloggen och brandväggsloggen fick inte egna separata testdataset.

En matchning mot `suspicious_ips.txt` visar endast att en observerad adress finns i indikatorlistan. Den bevisar inte att IP-adressen tillhör en angripare eller att en säkerhetsincident har inträffat.

Programmet använder endast lokala filer och kontaktar inga externa API:er eller hotdatatjänster.

## AI-redovisning

Jag använde **ChatGPT** som ett hjälpmedel under arbetet med uppgiften.

AI användes främst för att gå igenom uppgiftsbeskrivningen och hjälpa mig kontrollera att jag hade förstått kraven och inte missat någon obligatorisk del. Jag använde även AI för att få förklaringar när något var oklart och för att kontrollera projektstruktur, dokumentation och testning mot uppgiftsbeskrivningen.

Under programmeringen använde jag AI som stöd vid felsökning och för att diskutera vissa delar av koden när jag fastnade.

Den del av `security_report.py` som strukturerar och skriver resultatet till `output/security_report.txt` genererades med hjälp av ChatGPT. Den delen är markerad med en kommentar i källkoden. Jag har själv gått igenom koden och verifierat att rapporten innehåller rätt resultat.

Jag verifierade programmet genom att först köra det mot kursens Basic-dataset. Därefter genomförde jag tre separata testfall med manuellt kända kontrollvärden: ett positivt test, ett test med noll träffar och ett test med en felaktigt formaterad rad.

De manuellt förväntade resultaten jämfördes med programmets resultat och stämde överens i samtliga tre testfall. Efter testerna återställde jag programmet till originaldatasetet och körde det igen för att kontrollera att den normala analysen fortfarande fungerade.

AI användes alltså huvudsakligen som ett hjälpmedel för att förstå, kontrollera, felsöka och kvalitetssäkra arbetet, samt för att generera den markerade delen för rapportgenerering. AI-genererade förslag behandlades inte som automatiskt korrekta utan kontrollerades genom egna körningar och jämförelse med manuella kontrollvärden.