import os

def mangeAttraction(periode,valeur,ville):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskAttraction /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateAttraction\runUpdate.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskAttraction /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateAttraction\runUpdate.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskAttraction /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerceUpdate\UpdateAttraction\runUpdate.bat' /sc daily /mo "+valeur )
  fichier = open ( "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateAttraction/update.txt" , "w+" )

  for i in range(0,len(ville)) :

       fichier.write ( ville[i]+"\n" )

  fichier.close ()