import os

def mangeattraction(periode,valeur):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskAttractionDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\attractionDelete\runDelete.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskAttractionDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\attractionDelete\runDelete.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskAttractionDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\attractionDelete\runDelete.bat' /sc daily /mo "+valeur )
