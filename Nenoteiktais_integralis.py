'''
Dāvis Kalvāns 02.04.2022

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
'''

from mpi4py import MPI
import time

sakums = time.time() # Cikos programma sāk savu darbu

def f(x): # Funkcija, kurai rēķinās laukumu zem līknes (šeit f(x)=2x+1)
    return 2*x+1

# Funkcija, kas aprēķina funkcijas f(x) laukumu zem līknes izmantojot tainstūru metodi.
# Intervālu [a, b] sadala n starppunktos ar garumu h = (b-a)/n
# un tad sasummē izveidoto taisntūru laukumus.
def taisnsturu_laukums(a, b, n, h):
    summa = (f(a) + f(b-h))/2 # Vispirms aprēķina funkcijas vērtības pirmajā un pirmspēdējā punktā
    
    x = a
    for i in range(1, int(n)): # Cikls, kas iziet cauri visiem starppunktiem (izņemot pirmo un pēdējo)
        x = x + h # Paiet ar soli h uz nākamo starppunktu
        summa += f(x) # Pieskaita klāt funkcijas vērību šajā starppunktā
     
    laukums = summa * h # Lai iegūtu laukumu, sareizina ar platumu h
    return laukums

comm = MPI.COMM_WORLD  # Komunikātors starp kodoliem
kodola_nr = comm.Get_rank()  # Atrod, kurs kodols no visiem šis ir
kodoli = comm.Get_size()  # Cik kodoli ir iedoti algoritmam

# Šeit varam mainīt intervālu un starppunktu skaitu
a = 1 # Intervāla sākumpunkts
b = 3 # Intervāla galapunkts
n = 10**9 # Starppunktu skaits

h = (b-a)/n # Attālums starp starppunktiem (taisnstūru platums)

# Tālāk intervāls [a, b] jāsadala vienādos mazākos intervālos, ko rēķinās katrs kodols.
# Tam izmanto mainīgo kodola_nr, lai katrs kodols aprēķinātu savu intervālu.

savs_n = n/kodoli # Cik starppunkti katram kodolam
savs_a = a + kodola_nr*savs_n*h # Intervāla sākumpunkts katram kodolam
savs_b = savs_a + savs_n*h -h # Intervāla galapunkts katram kodolam

laukums = taisnsturu_laukums_laukums(savs_a, savs_b, savs_n, h) # Aprēķina sava intervāla taisntūru laukumus

if kodola_nr == 0: # Pirmais kodols sarēķinās savu laukumu un tad iegūs laukumus no pārējiem kodoliem
    kopejais_laukums = laukums # 0-tais kodols pievieno savu aprēķināto laukumu
    
    for kodols in range(1, kodoli): # Ievāc laukumus no pārējiem kodoliem
        laukums = comm.recv(source = kodols)
        kopejais_laukums += laukums # Koplaukumam pieskaita klāt katra kodola laukumu
        
else: # Pārējie kodoli aprēķina savu laukumu un nosūta to 0-tajam kodolam
   comm.send(laukums, dest = 0) # Nosūta aprēķināto laukumu 0-tajam kodolam



if kodola_nr == 0: # Beigās izprintē kopējo rezultātu
    beigas = time.time() # Cikos programma beidz savu darbu
    laiks = beigas - sakums # Cik ilgs laiks bija nepieciešams programmas izpildei
    
    print(f'Funkcijas laukuma zem liknes intervala [{a}, {b}] tuvinata vertiba ir {kopejais_laukums}')
    print(f'Aprekini ar {kodoli} kodoliem un n = {n} starppunktiem aiznema {laiks} sekundes.')
