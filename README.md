# MMU-paralela-skaitlosana

MMU 02.04.2022 "Paralēlā skaitļošana" lekcijas izmantotie programmu kodi
Autors: Dāvis Kalvāns

# Nepieciešamais programmu kodu palaišanai

### Python versija vismaz 3.8.8
Pieejama šeit: https://www.python.org/

### MPI
Windows operētājsistēmām: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi

Linux un MacOS operētājsistēmām: https://www.open-mpi.org/

# Nenoteiktais_integralis.py

Aprēķina nenoteikto integrāli funkcijai f(x) intervālā [a, b], sadalot intervālu n starppunktos.
Izmanto tainstūru metodi. katra intervāla jeb taisnstūra platums h = (b-a)/n.
Aprēķina funkcijas vērtību šajos starppunktos un pareizina ar platumu h, lai iegūtu
visu taisnstūra laukumu summu.

Paralelizācija notiek sākotnējo intervālu [a, b] sadalot mazākos vienādos intervālos
(to skaits būs vienāds ar kodolu skaitu) un tad katrs kodols aprēķinās
taisnstūru laukumu savā intervālā [savs_a, savs_b] ar starppunktu skaitu savs_n = n/kodoli.

Lai aprēķinus veiktu ar vairākiem kodoliem, tad, izmanto termināli ar komandu
"mpiexec -np [kodolu skaits] python Nenoteiktais_integralis.py"
vietā [kodolu skaits] liekot izmantoto kodolu skaitu.
Piemēram, četriem kodoliem lietotu mpiexec -np 4 python Nenoteiktais_integralis.py

# Pirmskaitli_naivi.py

Paralēls algoritms visu pirmskaitļu atrašanai no 2 līdz n.
Pārbauda vai skaitlis ir pirmskaitlis, izdalot ar visiem iepriekš
atrastajiem pirmskaitļiem.

Paralelizācija ir naiva, jo visus skaitļus n sadala vienādās daļās
katram kodolam pārbaudīt.
Lai pārbaudītu vai skaitlis ir pirmskaitlis, katrs kodols savus skaitļus 
izdala ar pilnīgi visiem, kuri mazāki par šo skaitli

Lai aprēķinus veiktu ar vairākiem kodoliem, tad, izmanto termināli ar komandu
"mpiexec -np [kodolu skaits] python Pirmskaitli_naivi.py"
vietā [kodolu skaits] liekot izmantoto kodolu skaitu.
Piemēram, četriem kodoliem lietotu mpiexec -np 4 python Pirmskaitli_naivi.py

# Pirmskaitli_kludains.py

Paralēls algoritms visu pirmskaitļu atrašanai no 2 līdz n.
Pārbauda vai skaitlis ir pirmskaitlis, izdalot ar visiem iepriekš
atrastajiem pirmskaitļiem.

Paralelizācija notiek pārbaudot skaitļus secīgi katram kodolam, 
izmantojot iepriekš atrastos pirmskaitļus.
Piemēram ar četriem kodoliem 0-tais pārbauda 3, 1-ais pārbauda 4,
2-ais pārbauda 5, 3-ais pārbauda 6 - ja pārbaude veiksmīga tad nosūta 0-tajam kodolam
pozitīvu atbildi un skaitlis tiek pievienots pirmskaitļu srakstam.
Šādu procedūru atkārto līdz pārbaudīti visi skaitļi līdz n.

Piezīme - šis algoritms nav pareizs, jo kāds no kodoliem var atrast jaunu
pirmskaitli, bet citiem kodoliem tas nebūs pieejams pārbaudei - tādēļ
reizēm tiks atrasti lieki skaitļi, kuri patiesībā nav pirmskaitļi.
Algoritmam, kur šī problēma izlabota, skatīt Pirmskaitli_izlabots.py

Lai aprēķinus veiktu ar vairākiem kodoliem, tad, izmanto termināli ar komandu
"mpiexec -np [kodolu skaits] python Pirmskaitli_kludains.py"
vietā [kodolu skaits] liekot izmantoto kodolu skaitu.
Piemēram, četriem kodoliem lietotu mpiexec -np 4 python Pirmskaitli_kludains.py

# Pirmskaitli_izlabots.py

Paralēls algoritms visu pirmskaitļu atrašanai no 2 līdz n.
Pārbauda vai skaitlis ir pirmskaitlis, izdalot ar visiem iepriekš
atrastajiem pirmskaitļiem.

Šī izlabotā versija papildus parbāudei pret atrastajiem pirmskaitļiem,
pārbauda arī nākamos pāris skaitļus no pēdējā atrastā pirmskaitļa (lai izvairītos
no situācijas, kad cits koodls ir atradis pirmskaitli pirms pārbaudāmā skaita, bet
šim kodolam par to vēl nav informācija).

Paralelizācija notiek pārbaudot skaitļus secīgi katram kodolam, 
izmantojot iepriekš atrastos pirmskaitļus.
Piemēram ar četriem kodoliem 0-tais pārbauda 3, 1-ais pārbauda 4,
2-ais pārbauda 5, 3-ais pārbauda 6 - ja pārbaude veiksmīga tad nosūta 0-tajam kodolam
pozitīvu atbildi un skaitlis tiek pievienots pirmskaitļu srakstam.
Šādu procedūru atkārto līdz pārbaudīti visi skaitļi līdz n.

Algoritms ir lēns, jo notiek nepārtraukta komunikācija kodolu starpā,
rezultātā komunikācija aizņem daudz reižu vairāk nekā paši aprēķini un
veicot aprēķinus ar 1 kodolu (ne paralēli) iegūs daudz ātrāku izpildes laiku.

Lai aprēķinus veiktu ar vairākiem kodoliem, tad, izmanto termināli ar komandu
"mpiexec -np [kodolu skaits] python Pirmskaitli_izlabots.py"
vietā [kodolu skaits] liekot izmantoto kodolu skaitu.
Piemēram, četriem kodoliem lietotu mpiexec -np 4 python Pirmskaitli_izlabots.py
