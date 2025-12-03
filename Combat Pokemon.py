import random

import numpy as np
import pandas as pds



df2=pds.read_csv("Pokemon.csv",index_col="Name")
print(df2["Type 1"].unique())
df3=df2[-df2["Type 1"].isin(["Normal","Flying","Dragon","Poison","Ghost","Fairy","Fighting","Ice","Dark","Steel","Psychic","Bug"])]
print(df3["Type 1"].unique())
print(df3)
attack=df3["Attack"]
print(attack)

pokemon= df3.index.values.tolist()  # transforme les éléments d'une colonne en liste, on prend index car Name devient un indice
print(pokemon)

j1=random.choices(pokemon,k=60) # liste de pokemon de J1
j2=random.choices(pokemon,k=60) # liste de pokemon de J2 que j'appelle deck


somme_forceJ1 = 0
somme_forceJ2 = 0
for i in j1:  # cette partie reste pour montrer que les deck s'ajuste
    somme_forceJ1 = somme_forceJ1+ attack.loc[i]  # renvoie le total de force du deck pour J1
print(f'Force Total J1 {somme_forceJ1}')
print("Le premier deck de J1 est", j1)
print("Le premier deck de J2 est", j2)


for i in j2:
    somme_forceJ2 = somme_forceJ2 + attack.loc[i]

print(f'Force Total J2: {somme_forceJ2}') #renvoie le total de force du deck  pour J2


while not (1.05*somme_forceJ2)>somme_forceJ1>(0.95*somme_forceJ2): #écart de 10 %

        j1 = random.choices(pokemon, k=60)

        somme_forceJ1 = sum(attack.loc[i] for i in j1) # ici on doit recalculer la force total du deck

print(f'Force Total nouvel de J1: {somme_forceJ1}')
print("Le deck final de j1 est",j1)
print("Le deck final de j2 est",j2)


pok_j1=random.choice(j1)
pok_j2=random.choice(j2)
type_pok_j1=df3.loc[pok_j1,"Type 1"]
type_pok_j2=df3.loc[pok_j2,"Type 1"]
print(f'le pokmeon de j1 est, {pok_j1} et il est de type {type_pok_j1}')
print(f'le pokmeon de j2 est, {pok_j2} et il est de type {type_pok_j2}')



# Fonction Combat

hp=df3["HP"]
att=df3["Attack"]
defense=df3["Defense"]
speed=df3["Speed"]

pv_pok_j1= hp.loc[pok_j1]
pv_pok_j2= hp.loc[pok_j2]
att_pok_j1= att.loc[pok_j1]
att_pok_j2= att.loc[pok_j2]
def_pok_j1= defense.loc[pok_j1]
def_pok_j2= defense.loc[pok_j2]
speed_pok_j1= speed.loc[pok_j1]
speed_pok_j2= speed.loc[pok_j2]



avantage={"Fire":"Grass","Water":"Fire","Grass":"Ground","Ground":"Rock","Rock":"Electric","Electric":"Water"}
# mettre fleche sur interface si possible ex: fleche vers haut rouge type avantageux
tour=1
while pv_pok_j1>0 and pv_pok_j2>0:
    esquive_J1 = np.random.binomial(1, speed_pok_j1 / 300)
    esquive_J2 = np.random.binomial(1, speed_pok_j2 / 300)
    if avantage.get(type_pok_j2)==type_pok_j1:

        tour+=1
        print(f'Tour: {tour}')
        if esquive_J1==1:
            print(f'{pok_j1} à ésquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:

            pv_pok_j1 = pv_pok_j1 - ((att_pok_j2/def_pok_j1)*13*1.35)
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        if esquive_J2==1:
            print(f'{pok_j2} à esquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:
            pv_pok_j2 = pv_pok_j2 - ((att_pok_j1/def_pok_j2)*13)
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')

    elif avantage.get(type_pok_j1)==type_pok_j2:
        tour+=1
        print(f'Tour: {tour}')
        if esquive_J1==1:
            print(f'{pok_j1} à ésquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:

            pv_pok_j1 = pv_pok_j1 - ((att_pok_j2/def_pok_j1)*13)
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        if esquive_J2==1:
            print(f'{pok_j2} à esquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:
            pv_pok_j2 = pv_pok_j2 - ((att_pok_j1/def_pok_j2)*13*1.35)
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')

    else:
        tour += 1
        print(f'Tour: {tour}')

    if esquive_J1 == 1:
        print(f'{pok_j1} à ésquivé')
        print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        print(f'il reste {pv_pok_j2} HP à {pok_j2}')
    else:

        pv_pok_j1 = pv_pok_j1 - ((att_pok_j2 / def_pok_j1) * 13)
        print(f'il reste {pv_pok_j1} HP à {pok_j1}')
    if esquive_J2 == 1:
        print(f'{pok_j2} à esquivé')
        print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        print(f'il reste {pv_pok_j2} HP à {pok_j2}')
    else:
        pv_pok_j2 = pv_pok_j2 - ((att_pok_j1 / def_pok_j2) * 13)
        print(f'il reste {pv_pok_j2} HP à {pok_j2}')



if pv_pok_j1<pv_pok_j2 and pv_pok_j2>0:
    print(f'{pok_j2} à gagné')
elif pv_pok_j1>pv_pok_j2 and pv_pok_j1>0:
    print(f'{pok_j1} à gagné')
elif pv_pok_j1<=0 and pv_pok_j2<=0:
    print("Match Nul")


# Fonction Combat

hp=df3["HP"]
att=df3["Attack"]
defense=df3["Defense"]
speed=df3["Speed"]

pv_pok_j1= hp.loc[pok_j1]
pv_pok_j2= hp.loc[pok_j2]
att_pok_j1= att.loc[pok_j1]
att_pok_j2= att.loc[pok_j2]
def_pok_j1= defense.loc[pok_j1]
def_pok_j2= defense.loc[pok_j2]
speed_pok_j1= speed.loc[pok_j1]
speed_pok_j2= speed.loc[pok_j2]



avantage={"Fire":"Grass","Water":"Fire","Grass":"Ground","Ground":"Rock","Rock":"Electric","Electric":"Water"}
# mettre fleche sur interface si possible ex: fleche vers haut rouge type avantageux
tour=1
while pv_pok_j1>0 and pv_pok_j2>0:
    esquive_J1 = np.random.binomial(1, speed_pok_j1 / 300)
    esquive_J2 = np.random.binomial(1, speed_pok_j2 / 300)
    if avantage.get(type_pok_j2)==type_pok_j1:

        tour+=1
        print(f'Tour: {tour}')
        if esquive_J1==1:
            print(f'{pok_j1} à ésquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:

            pv_pok_j1 = pv_pok_j1 - ((att_pok_j2/def_pok_j1)*13*1.35)
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        if esquive_J2==1:
            print(f'{pok_j2} à esquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:
            pv_pok_j2 = pv_pok_j2 - ((att_pok_j1/def_pok_j2)*13)
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')

    elif avantage.get(type_pok_j1)==type_pok_j2:
        tour+=1
        print(f'Tour: {tour}')
        if esquive_J1==1:
            print(f'{pok_j1} à ésquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:

            pv_pok_j1 = pv_pok_j1 - ((att_pok_j2/def_pok_j1)*13)
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        if esquive_J2==1:
            print(f'{pok_j2} à esquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:
            pv_pok_j2 = pv_pok_j2 - ((att_pok_j1/def_pok_j2)*13*1.35)
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')

    else:
        tour += 1
        print(f'Tour: {tour}')

    if esquive_J1 == 1:
        print(f'{pok_j1} à ésquivé')
        print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        print(f'il reste {pv_pok_j2} HP à {pok_j2}')
    else:

        pv_pok_j1 = pv_pok_j1 - ((att_pok_j2 / def_pok_j1) * 13)
        print(f'il reste {pv_pok_j1} HP à {pok_j1}')
    if esquive_J2 == 1:
        print(f'{pok_j2} à esquivé')
        print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        print(f'il reste {pv_pok_j2} HP à {pok_j2}')
    else:
        pv_pok_j2 = pv_pok_j2 - ((att_pok_j1 / def_pok_j2) * 13)
        print(f'il reste {pv_pok_j2} HP à {pok_j2}')



if pv_pok_j1<pv_pok_j2 and pv_pok_j2>0:
    print(f'{pok_j2} à gagné')
elif pv_pok_j1>pv_pok_j2 and pv_pok_j1>0:
    print(f'{pok_j1} à gagné')
elif pv_pok_j1<=0 and pv_pok_j2<=0:
    print("Match Nul")