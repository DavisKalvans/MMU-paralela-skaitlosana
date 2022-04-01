'''
Dāvis Kalvāns 02.04.2022

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
'''

from mpi4py import MPI
import time

sakums = time.time() # Cikos programma sāk savu darbu

# Funkcija, kas pārbauda vai skaitlis x ir pirmskaitlis, izdalot to ar visiem jau atrastajiem pirmskaitliem (pirmskaitli).
# Atgriež True, ja skaitlis x ir pirmskaitlis, False - ja nav.
def pirmskaitla_parbaude(x, pirmskaitli):

    for pirmskaitlis in pirmskaitli: # Cikls, kurā izdala ar visiem atrastajiem pirmskaitļiem
        if x % pirmskaitlis == 0: # Vai x dalās bez atlikuma
            return False # Ja dalās bez atlikuma ar kādu no atrastajiem pirmskaitļiem, tad x nav pirmskaitlis

    return True # Ja nedalās ar nevienu no atrastajiem pirmskaitļiem, tad x arī ir pirmskaitlis


comm = MPI.COMM_WORLD  # Komunikātors starp kodoliem
kodola_nr = comm.Get_rank()  # Atrod, kurs kodols no visiem sis ir
kodoli = comm.Get_size()  # Cik kodoli ir iedoti algoritmam

if kodola_nr == 0: # Šis būs kods 0-tajam kodolam (priekšniekam), kas nodrošinās komunikāciju ar pārējiem kodoliem
    n = 20 # Līdz kādam skaitlim atrast pirmskaitļus
    pirmskaitli = [2] # Saturēs atrastos pirmskaitļus; jau sākumā ieliek 2

    i = 3 # Sāk pārbaudīt ar skaitli 3

    while (i <= n+1): # Cikls, kurā pārbauda visus skaitļus

        for kodols in range(1, kodoli): # Nosūta katram kodolam vienu skaitli ko pārbaudīt un jau atrastos pirmskaitļus
            comm.send([i, pirmskaitli], dest=kodols)
            i += 1

        rezultats = pirmskaitla_parbaude(i, pirmskaitli) # 0-kodols arī pārbauda vienu skaitli
        if rezultats: # Ja skaitlis ir pirmskaitlis, tad papildina sarakstu ar pirmskaitļiem
            pirmskaitli.append(i)

        i += 1

        for kodols in range(1, kodoli):
            ir_pirmskaitlis, skaitlis = comm.recv(source = kodols) # No katra kodola ievāc rezultātus
            if ir_pirmskaitlis: # Ja skaitlis ir pirmskaitlis, tad papildina sarakstu ar pirmskaitļiem
                pirmskaitli.append(skaitlis)

    for kodols in range(1, kodoli): # Kad visi skaitļi pārbaudīti, nosūta komandu pārējiem kodoliem beigt aprēķinus
        comm.send(["stop", "stop"], dest=kodols)

    beigas = time.time() # Cikos programma beidz savu darbu
    laiks = beigas - sakums # Cik ilgs laiks bija nepieciešams programmas izpildei

    print(f"Aprekini tika veikti ar {kodoli} kodoliem.")
    print(f"Lai aprekinatu visus pirmskaitlus no 1 lidz {n} bija nepieciesamas {laiks} sekundes.")
    print(f"Tika atrasti {len(pirmskaitli)} pirmskaitli:")
    print(pirmskaitli)

else: # Kods pārējiem kodoliem
    apstaties = False

    while not apstaties: # Kamēr 0-tais kodols nedod komandu stop, tikmēr turpina strādāt
        skaitlis, pirmskaitli = comm.recv(source = 0) # Saņem jau atrastos pirmskaitļus un skaitli kuru pārbaudīt
        if skaitlis == "stop": # Ja saņem komandu stop, tad apstāsies
           apstaties = True

        else:
            rezultats = pirmskaitla_parbaude(skaitlis, pirmskaitli) # Pārbauda vai pirmskaitlis
            comm.send([rezultats, skaitlis], dest = 0) # Nosūta 0-tajam kodolam rezultātu
