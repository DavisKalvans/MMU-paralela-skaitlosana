# MMU-paralela-skaitlosana
MMU 02.04.2022 "Paralēlā skaitļošana" lekcijas izmantotie programmu kodi
Autors: Dāvis Kalvāns

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
