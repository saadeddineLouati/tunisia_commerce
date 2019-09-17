import os

def mangeRestaurent(periode,valeur,ville):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskRestaurent /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateRestaurent\runUpdate.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskRestaurent /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateRestaurent\runUpdate.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskRestaurent /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateRestaurent\runUpdate.bat' /sc daily /mo "+valeur )
  fichier = open ( "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateRestaurent/update.txt" , "w+" )

  for i in range(0,len(ville)) :

       fichier.write ( ville[i]+"\n" )

  fichier.close ()