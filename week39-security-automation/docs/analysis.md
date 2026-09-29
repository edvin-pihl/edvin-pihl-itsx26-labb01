# Security Automation Analysis – Week 39

## Metod

Jag använde **Dataset A: Basic** och analyserade följande filer:

- `data/auth.log`
- `data/access.log`
- `data/firewall.log`
- `data/suspicious_ips.txt`

Analysen genomfördes med Pythonprogrammet `src/security_report.py`.

Programmet analyserar tre typer av säkerhetsrelaterade händelser:

- `Failed login` i `auth.log`
- HTTP-status `401` i `access.log`
- `DENY` och `DROP` i `firewall.log`

Programmet extraherar käll-IP-adresser från fältet `src=` i giltiga loggrader och sammanställer de unika adresserna som observerade käll-IP-adresser.

De observerade adresserna jämförs därefter mot indikatoradresserna i `suspicious_ips.txt`.

Programmet sammanställer även de valda säkerhetsrelevanta händelserna per käll-IP.

Programmet hanterar dessutom den felaktigt formaterade raden i `auth.log` genom att hoppa över den och redovisa antalet hoppade rader.

Resultatet från analysen skrivs till `output/security_report.txt`.

## Rådata

Analysen bygger på tre loggfiler och en IOC-lista från Basic-datasetet.

### auth.log

```text
2026-09-24T08:15:03Z auth Failed login user=admin src=203.0.113.15
2026-09-24T08:15:07Z auth Failed login user=root src=203.0.113.15
2026-09-24T08:15:12Z auth Failed login user=admin src=203.0.113.15
2026-09-24T08:18:01Z auth Successful login user=student src=192.0.2.25
2026-09-24T08:22:10Z auth Failed login user=test src=198.51.100.44
Malformed line without source
```

Autentiseringsloggen innehåller misslyckade och lyckade inloggningar samt en felaktigt formaterad rad.

### access.log

```text
2026-09-24T08:21:02Z src=203.0.113.15 method=GET path=/login status=401
2026-09-24T08:21:04Z src=192.0.2.25 method=GET path=/index.html status=200
2026-09-24T08:21:06Z src=203.0.113.15 method=POST path=/login status=401
2026-09-24T08:22:15Z src=198.51.100.44 method=GET path=/admin status=404
```

Webbloggen innehåller HTTP-förfrågningar med statuskoderna 401, 200 och 404.

### firewall.log

```text
2026-09-24T08:16:10Z ALLOW src=192.0.2.25 dst=10.0.0.10 port=443
2026-09-24T08:16:22Z DENY src=203.0.113.15 dst=10.0.0.10 port=22
2026-09-24T08:16:30Z DROP src=203.0.113.99 dst=10.0.0.10 port=3389
```

Brandväggsloggen innehåller en `ALLOW`, en `DENY` och en `DROP`.

### suspicious_ips.txt

```text
203.0.113.15
198.51.100.44
203.0.113.99
```

IOC-listan används för medlemskontroll mot de observerade käll-IP-adresserna.

## Observerade käll-IP-adresser

Programmet identifierade följande unika käll-IP-adresser i de analyserade loggarna:

- `192.0.2.25`
- `198.51.100.44`
- `203.0.113.15`
- `203.0.113.99`

Dessa adresser används som underlag för jämförelsen mot `suspicious_ips.txt`.

Tre av de fyra observerade adresserna finns även i IOC-listan:

- `198.51.100.44`
- `203.0.113.15`
- `203.0.113.99`

`192.0.2.25` observerades i loggdatan men finns inte i IOC-listan.

## Observationer

### Autentiseringslogg

Programmet identifierade totalt **4 misslyckade inloggningar**.

Fördelningen var:

- `203.0.113.15`: 3
- `198.51.100.44`: 1

Programmet identifierade även **1 felaktigt formaterad rad**. Den raden hoppades över och programmet fortsatte analysen.

### Webblogg

Programmet identifierade totalt **2 HTTP 401-händelser**.

Fördelningen var:

- `203.0.113.15`: 2

Båda HTTP 401-händelserna kom från samma käll-IP.

### Brandväggslogg

Programmet identifierade totalt **2 blockerade brandväggshändelser**.

Fördelningen var:

- `203.0.113.15`: 1
- `203.0.113.99`: 1

Händelsen från `203.0.113.15` var en `DENY` och händelsen från `203.0.113.99` var en `DROP`.

### IOC-matchningar

Följande observerade käll-IP-adresser matchade adresser i `suspicious_ips.txt`:

- `198.51.100.44`
- `203.0.113.15`
- `203.0.113.99`

En IOC-matchning behandlas som analysunderlag och inte som ett bevis på att en IP-adress tillhör en angripare.

## Korrelation mellan datakällor

Den tydligaste korrelationen i datasetet finns för `203.0.113.15`.

Adressen förekommer i alla tre analyserade loggkällorna:

- 3 misslyckade inloggningar i `auth.log`
- 2 HTTP 401-händelser i `access.log`
- 1 `DENY`-händelse i `firewall.log`

Adressen finns dessutom i `suspicious_ips.txt`.

`198.51.100.44` förekommer i en misslyckad inloggning och finns även i IOC-listan.

`203.0.113.99` förekommer i en blockerad `DROP`-händelse och finns även i IOC-listan.

`192.0.2.25` förekommer också i loggdatan, bland annat i en lyckad inloggning, en HTTP 200-händelse och en `ALLOW`-händelse. Adressen finns däremot inte i IOC-listan och förekommer inte i de säkerhetsmönster som programmet räknar.

Det finns därför fler säkerhetsrelaterade observationer kopplade till `203.0.113.15` än till de andra observerade adresserna i det tillgängliga datasetet.

## Slutsats

Resultaten stödjer den begränsade slutsatsen att `203.0.113.15` är relevant att prioritera för fortsatt analys.

Anledningen är inte enbart att adressen finns i IOC-listan. Adressen förekommer även i flera typer av säkerhetsrelaterade händelser och i samtliga tre analyserade loggkällor.

`198.51.100.44` och `203.0.113.99` är också relevanta för fortsatt analys eftersom de förekommer i loggdatan och samtidigt finns i IOC-listan. Det finns däremot färre observerade säkerhetsrelaterade händelser kopplade till dessa adresser i det tillgängliga datasetet.

Resultaten är inte tillräckliga för att fastställa att någon av IP-adresserna tillhör en angripare eller att en säkerhetsincident faktiskt har inträffat.

## Osäkerhet

Datasetet innehåller ett begränsat antal logghändelser.

Analysen kan därför inte fastställa vem som kontrollerade en IP-adress, varför trafiken skickades eller vilken avsikt som låg bakom händelserna.

Programmet analyserar endast vissa fördefinierade säkerhetsmönster:

- `Failed login`
- HTTP 401
- `DENY`
- `DROP`

Andra säkerhetsrelevanta händelser kan därför finnas i loggarna utan att identifieras av programmet.

IOC-listan används endast som en lokal referens. Programmet kontaktar inga externa hotdatatjänster och kan därför inte ge ytterligare information om adressernas bakgrund.

## Alternativa förklaringar och falska positiva

De observerade säkerhetshändelserna behöver inte innebära att ett angrepp har inträffat.

En misslyckad inloggning kan exempelvis orsakas av att en legitim användare skriver fel lösenord eller att ett system använder gamla autentiseringsuppgifter.

En HTTP 401-händelse visar att en förfrågan inte blev autentiserad, men den visar inte varför autentiseringen misslyckades.

En `DENY`- eller `DROP`-händelse visar att brandväggen stoppade trafik. Händelsen visar däremot inte automatiskt att trafiken var skadlig. Det kan exempelvis handla om felkonfigurerad eller annan trafik som inte var tillåten enligt brandväggens regler.

Att en adress finns i `suspicious_ips.txt` är ytterligare information för analysen, men är inte tillräckligt för att klassificera adressen som en angripare.

Det är därför kombinationen av flera observationer som gör `203.0.113.15` relevant för fortsatt analys, snarare än en enskild händelse eller IOC-matchning.

## Datakvalitet

Programmet identifierade och hoppade över **1 felaktigt formaterad rad** i `auth.log`.

Den felaktiga raden var:

```text
Malformed line without source
```

Raden räknades inte som en misslyckad inloggning och programmet fortsatte analysen.

Det är viktigt att redovisa bortfallet eftersom en hoppad rad innebär att data inte inkluderades i analysresultatet.

I Basic-datasetet är bortfallet känt och redovisas av programmet. Formatkontrollen är dock relativt enkel och anpassad efter den aktuella datan.

I ett större eller mer varierande dataset skulle mer omfattande validering kunna behövas för att minska risken för tysta felanalyser.

## Säkerhetsbetydelse

Korrelation mellan flera datakällor kan hjälpa till att prioritera vilka observationer som bör undersökas vidare.

En enskild misslyckad inloggning, HTTP 401-händelse eller blockerad brandväggshändelse kan ha en legitim förklaring. Om samma käll-IP däremot förekommer i flera olika typer av säkerhetsrelaterade händelser finns mer underlag för fortsatt analys.

I detta dataset är `203.0.113.15` relevant för fortsatt undersökning eftersom adressen förekommer i autentiseringsloggen, webbloggen och brandväggsloggen och dessutom finns i IOC-listan.

Analysen visar därmed hur automatisering kan användas för att sammanställa information från flera loggkällor och identifiera observationer som kan prioriteras för fortsatt analys utan att automatiskt behandla dem som bekräftade säkerhetsincidenter.

# Testning och verifiering

Programmet verifierades med tre separata testfall för autentiseringsanalysen.

Testfilerna finns under:

`tests/test_data/`

Under testningen ändrades sökvägen till `auth.log` tillfälligt så att programmet läste respektive testfil.

`access.log`, `firewall.log` och `suspicious_ips.txt` fortsatte att använda Basic-datasetet under testerna.

Bedömningen av testfallen gjordes därför utifrån:

- antal misslyckade inloggningar
- misslyckade inloggningar per IP-adress
- antal hoppade felaktiga rader

## Test 1 – Känt positivt utfall

Testfilen `positive` innehöll:

```text
2026-09-24T08:15:03Z auth Failed login user=admin src=203.0.113.15
2026-09-24T08:15:07Z auth Failed login user=root src=203.0.113.15
```

### Manuellt kontrollvärde

Genom att läsa testfilen manuellt fastställde jag följande förväntade resultat:

- 2 misslyckade inloggningar
- `203.0.113.15`: 2
- 0 hoppade felaktiga rader

### Programmets resultat

```text
Antal misslyckade inloggningar: 2
Misslyckade inloggningar per IP:
{'203.0.113.15': 2}
Hoppade felaktiga rader: 0
```

Programmets resultat stämde med det manuellt räknade kontrollvärdet.

## Test 2 – Noll träffar

Testfilen `zero_hits` innehöll:

```text
2026-09-24T08:18:01Z auth Successful login user=student src=192.0.2.25
2026-09-24T08:19:01Z auth Successful login user=student src=192.0.2.25
```

### Manuellt kontrollvärde

Testfilen innehåller inga `Failed login`.

Förväntat resultat var:

- 0 misslyckade inloggningar
- inga IP-adresser med misslyckade inloggningar
- 0 hoppade felaktiga rader

### Programmets resultat

```text
Antal misslyckade inloggningar: 0
Misslyckade inloggningar per IP:
{}
Hoppade felaktiga rader: 0
```

Programmets resultat stämde med det manuellt fastställda kontrollvärdet.

Testet visade att programmet inte räknar lyckade inloggningar som misslyckade inloggningar.

## Test 3 – Formatfel

Testfilen `malformed` innehöll:

```text
2026-09-24T08:15:03Z auth Failed login user=admin src=203.0.113.15
Malformed line without source
```

### Manuellt kontrollvärde

Testfilen innehåller en korrekt misslyckad inloggning och en felaktigt formaterad rad.

Förväntat resultat var:

- 1 misslyckad inloggning
- `203.0.113.15`: 1
- 1 hoppad felaktig rad

### Programmets resultat

```text
Antal misslyckade inloggningar: 1
Misslyckade inloggningar per IP:
{'203.0.113.15': 1}
Hoppade felaktiga rader: 1
```

Programmets resultat stämde med det manuellt fastställda kontrollvärdet.

Den felaktiga raden hoppades över och programmet kunde fortsätta analysen.

## Sammanställning av testresultat

| Test | Manuellt förväntat resultat | Programmets resultat |
|---|---|---|
| Känt positivt utfall | 2 misslyckade inloggningar | 2 misslyckade inloggningar |
| Noll träffar | 0 misslyckade inloggningar | 0 misslyckade inloggningar |
| Formatfel | 1 misslyckad inloggning och 1 hoppad rad | 1 misslyckad inloggning och 1 hoppad rad |

Samtliga tre testfall gav samma resultat som de manuellt fastställda kontrollvärdena.

## Testernas avgränsning

De tre separata testfallen verifierade specifikt analysen av `auth.log`.

Under testerna fortsatte `access.log` och `firewall.log` att använda Basic-datasetet. Resultaten från dessa filer förekom därför fortfarande i programmets fullständiga utskrift.

Testbedömningen baserades därför på autentiseringsresultatet och antalet hoppade rader.

Efter testerna återställdes programmet till:

```python
with open("data/auth.log", "r") as file:
```

Programmet kördes därefter på nytt från projektroten med:

```bash
python3 src/security_report.py
```

Den slutliga körningen mot Basic-datasetet gav:

- 4 misslyckade inloggningar
- 4 observerade käll-IP-adresser
- 3 IOC-matchningar
- 2 HTTP 401-händelser
- 2 blockerade brandväggshändelser
- 1 hoppad felaktig rad

Det verifierade att den normala analysen fortfarande fungerade efter testningen.

# Begränsningar och förbättringsmöjligheter

Programmet är utvecklat för kursens Basic-dataset och analyserar ett begränsat antal fördefinierade säkerhetsmönster.

De separata testfallen fokuserar på autentiseringsanalysen. Ett möjligt nästa steg skulle vara att skapa motsvarande separata testdata även för `access.log` och `firewall.log`.

Felhanteringen skulle också kunna utvecklas med mer detaljerad validering av vilka fält som måste finnas i varje typ av loggrad.

I en större lösning skulle de olika analysdelarna även kunna delas upp i separata funktioner. Det skulle göra dem enklare att testa var för sig och göra programmet lättare att underhålla.

Dessa förbättringar påverkar inte resultaten från det aktuella Basic-datasetet, men skulle kunna göra programmet mer robust för andra eller mer varierande loggformat.