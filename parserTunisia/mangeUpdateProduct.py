import os

def mangeProduct(periode,valeur,categorie):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskProduct /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateProduct\runUpdate.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskProduct /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateProduct\runUpdate.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskProduct /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateProduct\runUpdate.bat' /sc daily /mo "+valeur )
  fichier = open ( "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateProduct/update.txt" , "w+" )

  for i in range(0,len(categorie)) :

    fichier.write ( categorie[i]+"\n")

  fichier.close ()
