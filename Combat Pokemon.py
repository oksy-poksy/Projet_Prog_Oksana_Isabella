import random
import pandas as pds

df=pds.read_csv("Pokemeon.csv")  # si on fait index_col="Name" ca de ne marche pas
print(df)

# rendre équilibrer le jeux plus tard ne pas oublier

pokemon= df["Name"].values.tolist()  # transforme les éléments d'une colonne en liste
print(pokemon)

j1=random.choices(pokemon,k=60) # liste de pokemon de J1

j2=random.choices(pokemon,k=60)

df2=pds.read_csv("Pokemeon.csv",index_col="Name")

attack=df2["Attack"]
print(attack)
somme_forceJ1 = 0
somme_forceJ2 = 0
for i in j1:
    somme_forceJ1 = somme_forceJ1+ attack.loc[i]  # renvoie le total de force du deck pour J1
print(f'Force Total J1 {somme_forceJ1}')
print("Le premier deck de J1 est", j1)
print("Le premier deck de J2 est", j2)


for i in j2:
    somme_forceJ2 = somme_forceJ2 + attack.loc[i]

print(f'Force Total J2: {somme_forceJ2}') #renvoie le total de force du deck  pour J2

somme_forceJ2 = somme_forceJ2
while not (1.05*somme_forceJ2)>somme_forceJ1>(0.95*somme_forceJ2): #écart de 10 %

        j1 = random.choices(pokemon, k=60)

        somme_forceJ1 = sum(attack.loc[i] for i in j1) # ici on doir recalculer la force total du deck

print(f'Force Total nouvel de J1: {somme_forceJ1}')
print("Le deck final de j1 est",j1)
print("Le deck final de j2 est",j2)


pok_j1=random.choice(j1)
pok_j2=random.choice(j2)
print("le pokmeon de j1 est",pok_j1)
print("le pokmeon de j2 est",pok_j2)



# Fonction Combat

hp=df2["HP"]
att=df2["Attack"]
pv_pok_j1= hp.loc[pok_j1]
pv_pok_j2= hp.loc[pok_j2]
att_pok_j1= att.loc[pok_j1]
att_pok_j2= att.loc[pok_j2]

tour=1
while pv_pok_j1>0 and pv_pok_j2>0:

    tour+=1
    print(f'Tour: {tour}')
    pv_pok_j1 = pv_pok_j1 - (att_pok_j2/5)
    print(f'il reste {pv_pok_j1} HP à {pok_j1}')
    pv_pok_j2 = pv_pok_j2 - (att_pok_j1/5)
    print(f'il reste {pv_pok_j2} HP à {pok_j2}')

if pv_pok_j1<pv_pok_j2 and pv_pok_j2>0:
    print(f'{pok_j2} à gagné')
elif pv_pok_j1>pv_pok_j2 and pv_pok_j1>0:
    print(f'{pok_j1} à gagné')
elif pv_pok_j1<=0 and pv_pok_j2<=0:
    print("Match Nul")