# Del 3 - Identifiera hot

## Beskrivning

Utgå från ett enkelt scenario: ett företag använder e-post, Microsoft 365, mobiltelefoner och ett HR-system.
Identifiera 3 hot, 3 sårbarheter och 3 skyddsåtgärder. Dokumentera i hotanalys.md.

# E-post
## Hot
När det kommer till e-post finns det följande hot ett företag kan utsättas för, Phising, Spoofing och Ransome Ware.

## Sårbarhet
Dessa sårbarheter finns mot e-post för företag. Personal saknar utbildning om hur de ska upptäcka misstänksamma mail, Personal har möjlighet att öppna filer från okända användare och Filter som ej upptäcker misstänktsamma 

## Skyddskyddsåtgärder
Företag kan implementera dessa åtgärder för att göra sitt e-post system säkrare. 2FA för att verifiera att det är rätt användare som loggar in och inte någon som att tagit över ett lösenord. Filter som tar bort spam och skadligkod som kan ligga gömt i filer. Använda sig av DKIM för att göra så att användare kan se direkt om mailet har kommit från en troende kontakt.

# Microsoft 365

## Hot
De hot som finns mot Microsoft 365 påminner en del av de som finns mot e-post, då båda har möjlighet att skicka och ta emot meddelande. Men det hot som är mer vanliga i Mircrosoft 365 är Account takeover, det kan vara ett konto från en tidigare anställd som ej  blivit borttagaet och där lösenordet ej har byts till ett mer säkert. Sen finns det ockås risk för phising, där någon kan förfalska ett konto så att det ser ut som att det kommer från en chef och skickar meddalnde direkt till anställda med länkar eller filer. 

## Sårbarhet
Man blir väldigt beroende på molnet och kan få problem om Microsofts servrar skulle gå ner. Om man implemnterar Co-pilot kan man riskera att den har tillgångar till alla filer i företaget konto och kan då ta information från dessa och berättar det för personer som ej ska ha tillgång till detta, så där måste man se till att man sätter bra regler för Co-pilot om vilka filer de får och inte får tillgång till. Här är ännu en gång det med konton från tidigare naställda att de kan vara extra sårbara då man ej uppdaterar deras lösenord och att de kan bli lättare att knäcka. 

## Skyddskyddsåtgärder
Här får man också köra med 2FA för att säkerställa att ingen har kommit över ett gammalt konto eller lösenord, och kan ta sig in på bara ett löenord. Microsoft Defender finns också inbyggt som extra hjälp om någon obehörig fil skulle laddas ner av en anställd. Man kan även använda sig av Conditional Access för att göra ännu svåare för någon som inte är behörig från att logga in, då man kan förbjuda anslutning utifrån geografiska punkter. 

# Mobiltelefoner

## Hot
För mobiltelefoner blir phising även aktuelt då man kan få SMS med skadliga filer eller länkar. Sedan är öppna nätverk ett problem då det kan leda till att någon kan läsa allt data som skickas mellan telefonen och t.ex företagets servrar. Stulna enheter kan också bli ett stort problem, om användaren inte har ett starkt lösenord kan de snabbt ta sig in i den och få tillgång till alla information på den.

## Sårbarhet
Om en anställd skulle logga in på sin privata mobil där IT inte kan ha gjort extra skydd, kan snabbt leda till att data blir stulen. Dåliga lösenord är ett stort problem då det låter de stulna enheter bli öppnade utan större prboblem. Om man låter de anställda ladda ner vilka appar de vill på sina telefoner kan det leda till att appar med skadlig kod laddas ner och kan finnas risk att detta har möjlighet att utför Password skimming. 

## Skyddskyddsåtgärder
Företag kan implementera Mobile Device Managment, där IT avdelningen på företag kan bestämma över alla telefoner vilka appar som får laddas ner, vilka hemsidor som får besökas och om telefonerna får ansluta sig till öppna nätverk. De kan också använda sig av Mobile Threat Defense för att styrka sina skydd mot cyberhot. Den lättaste är att se till att man utbildar sina anställda på de risker som finns och vad de ska ska göra för att mina risker att någon kan hända. 

# HR - System

## Hot
De hot som finns mot HR - system är ransomware, Phising och data breach. Och alla tre går oftast ut på att pressa företag på pengar.

## Sårbarhet
Sårbarhet för systemen kan vara svaga 2FA eller om de inte finns alls. Vilket gör det lätt för personer utanför men även inne i företaget att ta del av infroamtion i dessa system som sedan kan spridas. Legacy system som inte får säkerhetsuppdateringar längre vilket kan leda till expolits som kan tan utnyttja för att komma åt data. Sårbar API vilket kan leda till att hackare kan använda sig av detta för att komma åt den känsliga informationen.

## Skyddskyddsåtgärder
Om företag använder sig av rollbaserad behörighet kommer det leda till att bara de som ska se filer har möjlighet att logga in i systemen och om man kopplar detta till MFA så blir mycket svårt för någon som bara har kommit över ett lösenord att ta sig in. Man ska okcås se till att all data blir krypterad då det blir extremt svårt för någon att göra någon med datan om de har fått tag på det på något sätt.