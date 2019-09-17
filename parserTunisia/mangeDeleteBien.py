import os

def mangeBien(periode,valeur):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskBienDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\bienDelete\runDelete.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskBienDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\bienDelete\runDelete.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskBienDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\bienDelete\runDelete.bat' /sc daily /mo "+valeur )