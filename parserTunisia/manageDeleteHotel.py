import os

def mangeHotel(periode,valeur):

  if periode.find("minute")!= -1:
     sortie = os.popen(r"SCHTASKS /create /tn taskHotelDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\hotelDelete\runDelete.bat' /sc minute /mo "+valeur)

  elif periode.find ( "heure" ) != -1:
      sortie = os.popen ( r"SCHTASKS /create /tn taskHotelDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\hotelDelete\runDelete.bat' /sc hourly /mo "+valeur )
  else:
      sortie = os.popen (r"SCHTASKS /create /tn taskHotelDelete /tr 'C:\Users\nidou\Desktop\tunisia-commerce\tunisia_commerDelete\hotelDelete\runDelete.bat' /sc daily /mo "+valeur )


