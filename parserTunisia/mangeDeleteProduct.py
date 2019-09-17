import os

def mangeProduct(periode,valeur):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskProductDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\ProductDelete\runDelete.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskProductDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\ProductDelete\runDelete.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskProductDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\ProductDelete\runDelete.bat' /sc daily /mo "+valeur )

