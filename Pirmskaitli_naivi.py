'''
Dāvis Kalvāns 02.04.2022

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
'''

from mpi4py import MPI
import time

sakums = time.time() # Cikos programma sāk savu darbu

# Funkcija, kas pārbauda vai skaitlis x ir pirmskaitlis, izdalot to ar visiem mazākiem skaitļiem.
# Atgriež True vai False vērtību.
def pirmskaitla_parbaude(x):
    
    for i in range(2, x): # Iet cauri visiem skaitļiem no 2 līdz x-1
        if x % i == 0: # Vai x dalās bez atlikuma
            return False # Ja dalās bez atlikuma ar kādiem no skaitļiem no 2 lidz x-1, tad x nav pirmskaitlis

    return True # Ja nedalās ar nevienu, tad x arī ir pirmskaitlis
    
comm = MPI.COMM_WORLD  # Komunikātors starp kodoliem
kodola_nr = comm.Get_rank()  # Atrod, kurs kodols no visiem sis ir
kodoli = comm.Get_size()  # Cik kodoli ir iedoti algoritmam 

n = 1000 # Līdz kādam skaitlim atrast pirmskaitļus
savi_pirmskaitli = [2] # Saturēs atrastos pirmskaitļus; jau sākumā ieliek 2

savs_n = int(n/kodoli)+1 # Cik skaitļus katram kodolam pārbaudīt

if kodola_nr == 0: # Pirmais kodols sāk pārbaudi ar skaitli 3
    savs_a = 3 
else:
    savs_a = kodola_nr*savs_n # Katrs nākamais paiet par savs_n uz priekšu

for i in range(savs_a, savs_a + savs_n): # Kodols pārbauda savus skaitļus
    if pirmskaitla_parbaude(i):
        savi_pirmskaitli.append(i) # Ja ir pirmskaitlis, tad papildina pirmskaitļu sarakstu
        
if kodola_nr == 0: # 0-tais kodols ievāc pārējo kodolu atrastos pirmskaitļus

    pirmskaitli = savi_pirmskaitli # Iekopē kopējā pirmskaitļu sarakstā 0-tā kodola atrastos pirmskaitļus
    for kodols in range(1, kodoli):
        kodola_pirmskaitli = comm.recv(source = kodols) 
        pirmskaitli = list(set(pirmskaitli+kodola_pirmskaitli)) # Papildina kopējo pirmskaitļu sarakstu ar katra kodola atrastajiem

else:
    comm.send(savi_pirmskaitli, dest = 0) # Nosūta atrastos pirmskaitļus 0-tajam kodolam
   

if kodola_nr == 0:
    beigas = time.time() # Cikos programma beidz savu darbu
    laiks = beigas - sakums # Cik ilgs laiks bija nepieciešams programmas izpildei
    
    print(f"Lai aprkeinatu visus pirmskaitlus no 1 lidz {n} bija nepieciesamas {laiks} sekundes.")
    print(f'Tika atrasti {len(pirmskaitli)} pirmskaitli.')
    print(pirmskaitli)

