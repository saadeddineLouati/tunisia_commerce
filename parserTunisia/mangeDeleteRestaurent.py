import os

def mangerestaurant(periode,valeur):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskRestaurentDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\restaurentDelete\runDelete.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskRestaurentDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\restaurentDelete\runDelete.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskRestaurentDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\restaurentDelete\runDelete.bat' /sc daily /mo "+valeur )

