from django.shortcuts import render , redirect,reverse
import os
from . import parserSite
from .models import Product,Hotel,Restaurant,Activity,VolOneWay,VolRoundTrip,Bien
from . import  mangeUpdateProduct,mangeUpdateHotel,mangeUpdateRestaurent,mangeUpdateAttraction,mangeUpdateBien,mangeDeleteProduct,manageDeleteHotel,mangeDeleteRestaurent,mangeDeleteAttraction,mangeDeleteBien
from elasticsearch import Elasticsearch
from django.template import RequestContext
import json


# les fonctions d'indexation


def createIndex(keyword,tab):
 es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )
 es.indices.create ( index=keyword.lower ()+tab , body={"settings": {
     "number_of_shards": 1 ,
     "similarity": {
         "scripted_tfidf": {
             "type": "scripted" ,
             "weight_script": {
                 "source": "double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;"
             } ,
             "script": {
                 "source": "double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;"
             }
         }
     }
 }
 } ,request_timeout=30000)

 return es

def indexation(tableau,es,keyword,tab):
    for i in range(0,len(tableau)):
        es.index ( index=keyword+tab , doc_type=keyword+tab , body=tableau[i] , id=i+1 ,request_timeout=30000)


# les fonctions de vérifications base de données
def exist(keyword ):
    es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )
    print(keyword)
    try:
        res = es.get ( index=keyword+"restaurant" , doc_type=keyword+"restaurant"  , id=1 )
        res = es.get ( index=keyword + "attraction" , doc_type=keyword+ "attraction"  , id=1 )
        return True
    except:
        print("hello")
        return False




def find(mot,liste):
    for i in range (0,len(liste)):
        if  liste[i].find(mot) != -1 or mot.find(liste[i]) != -1 :
            return(True)
    return False

def verifyVol(mot_recherche,dateVol,cabinclass,datevolretour):
 if datevolretour=="":
    table = VolOneWay.objects.filter ( **{"depart and destination": mot_recherche} )
    if len ( table ) != 0:
        table = table[0].to_json ()
        if table.find (dateVol+"_volList_"+cabinclass) != -1:
            return ("date");
        else:
            return ("nouvelle date");
    return ("nouvelle depart and destination ")
 else:
     table = VolRoundTrip.objects.filter ( **{"depart and destination": mot_recherche} )
     if len ( table ) != 0:
         table = table[0].to_json ()
         print ( dateVol+"-"+datevolretour+"_volList_ "+cabinclass )
         if table.find ( dateVol+"-"+datevolretour+"_volList_ "+cabinclass ) != -1:
             return ("les vols de " + dateVol + "sont stcokés dans la bd");
         else:
             return ("nouvelle date");

     return ("nouvelle depart and destination ")

def verifyBien(mot_recherche,typeBien,type):
    table = Bien.objects.filter (**{"ville":mot_recherche })
    if len ( table ) != 0:
        table = table[0].to_json ()
        if table.find(typeBien+"_a_"+type)!=-1 :
           return ("les "+ typeBien+"s à "+type +"sont stcokés dans la bd");
        else:
            return ("nouvelle type de bien");
    return("nouvelle ville")


def verifyBD(mot_recherche,categorie):

  if categorie == "produit":
    table = Product.objects.filter(categorie=mot_recherche)
    if len(table) != 0 :
        return(False);
    return(True)

  if categorie == "hotel":
      table = Hotel.objects.filter (villeHotel=mot_recherche )
      if len ( table ) != 0:
          return (False);
      return (True)

  if categorie == "attraction":
      table = Activity.objects.filter ( villeActivites=mot_recherche )
      if len ( table ) != 0:
          return (False);
      return (True)

  if categorie == "restaurent":
      table = Restaurant.objects.filter ( villeRestaurant=mot_recherche )
      if len ( table ) != 0:
          return (False);
      return (True)


# les fonctions de redirection

def redirection(request,categorie,tab):
    table = Product.objects ()
    table1=Hotel.objects ()
    table2=Restaurant.objects ()
    table3=Activity.objects ()
    affiche =""
    afficheH = ""
    afficheR = ""
    afficheA = ""
    if len(table) == 0 or len(table1) == 0 and len(table2) == 0 and len(table3) == 0:
        affiche= "non"

    if len(table1) == 0:
        afficheH = "non"

    if len ( table2 ) == 0:
        afficheR = "non"

    if len ( table3 ) == 0:
        afficheA = "non"

    if categorie == "manageMagasin" and tab =="manage":
        table = Product.objects ()
        categories = []

        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):
                categories.append ( table[i].categorie )

        context = {
            'categories': categories ,
            'categorie': categorie ,
            'tab': tab ,
            'showKeywordbord':affiche,


        }

        return render ( request , 'admin.html' , context )

    if categorie == "manageTravel" and tab == "manage":
        table =Hotel.objects ()
        table1=Restaurant.objects()
        table2=Activity.objects()

        villeH = []
        villeR = []
        villeA =[]

        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):
                villeH.append ( table[i].villeHotel)

        if len ( table1 ) != 0:
            for i in range ( 0 , len ( table1 ) ):
                villeR.append ( table1[i].villeRestaurant )

        if len ( table2 ) != 0:
            for i in range ( 0 , len ( table2 ) ):
                villeA.append ( table2[i].villeActivites )

        context = {

            'categorie': categorie ,
            'tab': tab ,
            'hotel': villeH ,
            'restaurant': villeR ,
            'activity': villeA,
            'showKeywordbord': affiche,
            'afficheH' : afficheH ,
             'afficheR' : afficheR ,
             'afficheA' : afficheA ,
            'afficheTab':"hot"

        }
        return render ( request , 'admin.html' , context )




    if categorie=="manageDeals":

           table = Bien.objects ().to_json ()
           table = json.loads ( table )

           if str(table).find("_vendre")!= -1:
               afficheV= 'true'
           else:
               afficheV ='false'

           if str ( table ).find ( "_louer" ) != -1:
               afficheL = 'true'
           else:
               afficheL = 'false'
           context = {

                'categorie': categorie ,
                'tab': tab ,
                'afficheV':afficheV,
                'afficheL':afficheL,



            }

           return  render( request , 'admin.html',context )

    if  tab == "tableaubord" :

        table = Product.objects ()
        categories = []
        numbers=[]
        productAll =0
        num=[]
        labels=[]

        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):

                categories.append ( table[i].categorie )
                table1 = Product.objects.filter ( categorie=table[i].categorie )
                productAll+= len ( table1[0]["produitList"] )
                numbers.append(len ( table1[0]["produitList"] ))

        num.append(productAll)
        table3 = Restaurant.objects ()
        table4 = Activity.objects()
        table2 = Hotel.objects ()
        offres = 0
        offresA  = 0
        offresR =0
        nums = []

        if len ( table2 ) != 0:
         for i in range ( 0 , len ( table2 ) ):
            table21 = Hotel.objects.filter ( villeHotel=table2[i].villeHotel )
            offres += len ( table21[0]["hotelList"] )



         nums.append(offres)
         labels.append ( "Hôtels" )

        if len ( table3 ) != 0:
            for i in range ( 0 , len ( table3 ) ):
                table31 = Restaurant.objects.filter ( villeRestaurant=table3[i].villeRestaurant )
                offres += len ( table31[0]["restaurantList"] )
                offresR += len ( table31[0]["restaurantList"] )
            nums.append ( offresR )
            labels.append("Restaurants")

        if len ( table4 ) != 0:
            for i in range ( 0 , len ( table4 ) ):
                table41 = Activity.objects.filter ( villeActivites=table4[i].villeActivites )
                offres += len ( table41[0]["activitiesList"] )
                offresA +=len ( table41[0]["activitiesList"] )


            nums.append ( offresA )
            labels.append ( "Attractions touristiques" )


        num.append(offres)




        context = {
            'categories': categories ,
            'numbers': numbers ,
            'categorie': categorie ,
            'tab': tab ,
            'num' : num ,
            'nums' : nums,
            'labels':labels

        }


        return render ( request , 'admin.html' , context )

    if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
            "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
        "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
        "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :
        return render ( request , '404.html' )

def redirection1(request,manage):
        table = Product.objects ()
        table1=Hotel.objects ()
        table2=Restaurant.objects ()
        table3=Activity.objects ()
        affiche =""
        afficheH = ""
        afficheR = ""
        afficheA = ""
        if len(table) == 0 or len(table1) == 0 and len(table2) == 0 and len(table3) == 0:
          affiche= "non"

        if len(table1) == 0:
          afficheH = "non"

        if len ( table2 ) == 0:
          afficheR = "non"

        if len ( table3 ) == 0:
         afficheA = "non"



        table =Hotel.objects ()
        table1=Restaurant.objects()
        table2=Activity.objects()

        villeH = []
        villeR = []
        villeA =[]

        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):
                villeH.append ( table[i].villeHotel)

        if len ( table1 ) != 0:
            for i in range ( 0 , len ( table1 ) ):
                villeR.append ( table1[i].villeRestaurant )

        if len ( table2 ) != 0:
            for i in range ( 0 , len ( table2 ) ):
                villeA.append ( table2[i].villeActivites )


        context = {

            'categorie': "manageTravel" ,
            'tab': "manage" ,
            'hotel': villeH ,
            'restaurant': villeR ,
            'activity': villeA,
            'showKeywordbord': affiche,
            'afficheH' : afficheH ,
             'afficheR' : afficheR ,
             'afficheA' : afficheA ,
            'afficheTab':manage

        }
        print("dddd")
        return render ( request , 'admin.html' , context )





def manage(request,categorie,tab):
    if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
            "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
        "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
        "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :
        return render ( request , '404.html' )


    if  str(request.POST).find("Parse")!= -1:
        context=parser(request,categorie,tab)
        if context["message"].find("ajoutés") != -1 :
          return redirect("/adminProfile/"+context["categorie"]+"/"+context["tab"]+"/all")

        else:
            return redirect ( "/adminProfile/" + context["categorie"] + "/" + context["tab"] +"/welcome"  )

    elif str ( request.POST ).find ( "Update" ) != -1:
      context = update ( request , categorie , tab )
      return redirect ( "/adminProfile/" + context["categorie"] + "/" + context["tab"] + "/welcome" )

    else:
      if str ( request.POST ) != "<QueryDict: {}>":
        context = delete ( request , categorie , tab )
        return redirect ( "/adminProfile/" + context["categorie"] + "/" + context["tab"] + "/welcome" )

    return render ( request , '404.html' , )


def page_not_found ( request ):
    """
      Page not found Error 404
    """

    print("dddddd")
    return render(request,'404.html')

# les fonctions de gestion de la base de données

def parser(request,categorie,tab):

     if request.method == 'POST':

           if str(request.POST).find("categorieParse") != -1:
             if verifyBD (request.POST['categorieParse'],"produit"):
                 product = parserSite.extractProduct(request.POST['categorieParse'])
                 if len(product)!=0 :
                   es = createIndex ( request.POST['categorieParse'].lower () , "" )
                   indexation ( product , es , request.POST['categorieParse'].lower () , "" )
                   data= {'categorie': request.POST['categorieParse'],'produitList':product}
                   produits=Product(**data)
                   print(len(product))
                   produits.save(validate=True)
                   context = {
                   'message': 'des nouveaux produits sont ajoutés',
                   'categorie'  :categorie,
                   'tab': "show"
                     }

                 else:
                     context = {
                         'message': "svp vous devez verifiez la catégorie saisie ou la connexion",
                         'categorie': categorie ,
                         'tab': tab
                     }

             else :
                 context = {
                     'message' : 'vous avez ajouté cette catégorie' ,
                     'categorie': categorie ,
                     'tab': tab
                 }

             return context

           if str ( request.POST ).find ( "hotelParse" ) != -1:
               if verifyBD ( request.POST['hotelParse'] ,"hotel"):
                     product = parserSite.extractHotel ( request.POST['hotelParse'] )
                     if len ( product ) != 0:
                      es=createIndex(request.POST['hotelParse'].lower(),"hotel" )
                      indexation(product,es,request.POST['hotelParse'].lower() ,"hotel")
                      data = {'villeHotel': request.POST['hotelParse'] , 'hotelList': product}
                      hotels =Hotel(**data)
                      hotels.save(validate=True)
                      context = {
                          'message': 'des nouveaux hotels sont ajoutés' ,
                          'categorie': categorie ,
                          'tab': "showHotels",

                       }

                     else:
                         context = {
                             'message': 'vous devez verifiez la ville saisie ou verifiez la connexion' ,
                             'categorie': categorie ,
                             'tab': tab
                         }

               else:
                   context = {
                       'message': 'vous avez ajouté cette ville hotel' ,
                       'categorie': categorie ,
                       'tab': tab
                   }
               return context

           if str ( request.POST ).find ( "restaurentParse" ) != -1:
               if verifyBD ( request.POST['restaurentParse'] , "restaurent" ):
                   product = parserSite.extractRestaurent( request.POST['restaurentParse'] )
                   if (len ( product ) != 0):
                    es = createIndex ( request.POST['restaurentParse'].lower () , "restaurant" )
                    indexation ( product , es , request.POST['restaurentParse'].lower () , "restaurant" )
                    data = {'villeRestaurant': request.POST['restaurentParse']  , 'restaurantList': product}
                    Restaurants = Restaurant ( **data )
                    Restaurants.save ( validate=True )

                    context = {
                    'message': 'des nouveaux restaurents sont ajoutés' ,
                        'categorie': categorie ,
                        'tab': 'showRestaurents'
                     }

                   else:
                       context = {
                           'message': 'vous devez verifiez la ville saisie ou verifiez la connexion' ,
                           'categorie': categorie ,
                           'tab': tab
                       }

               else:
                   context = {
                       'message': 'vous avez ajouté cette ville ' ,
                       'categorie': categorie ,
                       'tab': tab
                   }
               return context

           if str ( request.POST ).find ( "attractionParse" ) != -1:
               if verifyBD ( request.POST['attractionParse'] , "attraction" ):
                   product = parserSite.extractAttractions(request.POST['attractionParse'] )
                   if (len ( product ) != 0):
                    es = createIndex ( request.POST['attractionParse'].lower () , "attraction" )
                    indexation ( product , es , request.POST['attractionParse'].lower () , "attraction" )
                    data = {'villeActivites': request.POST['attractionParse'] , 'activitiesList': product}
                    activities = Activity ( **data )
                    activities.save ( validate=True )
                    context = {
                    'message': 'des nouvelles activités touristiques sont ajoutés',
                        'categorie': categorie ,
                        'tab': 'showActivities'
                    }

                   else:
                       context = {
                           'message': 'vous devez verifiez la ville saisie ou verifiez la connexion' ,
                           'categorie': categorie ,
                           'tab': tab
                       }

               else:
                   context = {
                       'message': 'vous avez ajouté cette ville attraction' ,
                       'categorie': categorie ,
                       'tab': tab
                   }
               return context



           if str ( request.POST ).find ( "villeBParse" ) != -1:
               res=verifyBien (request.POST['villeBParse'] , request.POST['typeBien'], request.POST['type'])
               if res=="nouvelle type de bien" or res=="nouvelle ville" :
                   product = parserSite.extractBien(request.POST['villeBParse'] ,request.POST['type'] ,request.POST['typeBien'])
                   if len(product) != 0:
                    if res =="nouvelle ville":
                      data = {'ville': request.POST['villeBParse']  ,request.POST['typeBien']+'_a_'+request.POST['type'] : product}
                      biens=Bien( **data )
                      biens.save(validate=True)
                      if str ( request.POST['type'] ).find ( "_vendre" ) != -1:
                          context = {
                              'message': 'nouveaux biens immobliéres ajoutés' ,
                              'categorie': categorie ,
                              'tab': "showSales"
                          }
                      else:
                          context = {
                              'message': 'nouveaux biens immobliéres ajoutés' ,
                              'categorie': categorie ,
                              'tab': "showRent"
                          }

                    else:
                       string=request.POST['typeBien']+"_a_"+request.POST['type']
                       table = Bien.objects.filter ( ville= request.POST['villeBParse'])
                       table[0].update(**{string :product})
                       if    str(request.POST['type']).find("_vendre") != -1 :
                         context = {
                       'message': 'nouveaux biens immobliéres ajoutés',
                        'categorie': categorie ,
                        'tab': "showSales"
                    }
                       else:
                        context = {
                            'message': 'nouveaux biens immobliéres ajoutés' ,
                            'categorie': categorie ,
                            'tab':  "showRent"
                        }
                   else:
                    context = {
                       'message': 'vous devez verifiez la ville saisie ou verifiez la connexion' ,
                        'categorie': categorie ,
                        'tab': tab
                    }
               else:
                   context = {
                       'message': 'vous avez ajouté cette ville ' ,
                       'categorie': categorie ,
                       'tab': tab
                   }
               return context


def update ( request,categorie,tab ):
    print ( "hello" )
    if categorie == 'manageMagasin':
        categorie1 = request.POST.getlist ( "productCategorieUpdate" )
        periode = request.POST["unite"]
        frequence = request.POST["valeur"]
        mangeUpdateProduct.mangeProduct ( periode , frequence , categorie1 )
        table = Product.objects ()
        if (len ( table )) == 1:
            mangeDeleteProduct.mangeProduct ( "minute" , "2" )
        context = {
            'message': 'La mise à jour atomatique de la table Produit est lancée' ,
            'categorie': categorie ,
            'tab': tab
        }
        return context


    if categorie == 'manageTravel' and len(request.POST.getlist ( "hotelVillesUpdate" ) )!=0:
        print("dddggh")
        villes = request.POST.getlist ( "hotelVillesUpdate" )
        periode = request.POST["unite"]
        frequence = request.POST["valeur"]
        mangeUpdateHotel.mangeHotel ( periode , frequence , villes )
        table = Hotel.objects ()
        print ( len ( table ) )
        if (len ( table )) == 1:
            manageDeleteHotel.mangeHotel ( "minute" , "2" )
        context = {
            'message': 'La mise à jour atomatique de la table Hotel est lancée' ,
            'categorie': categorie ,
            'tab': tab
        }
        return context

    if categorie == 'manageTravel' and len( request.POST.getlist ( "resVillesUpdate" )) != 0:
        villes = request.POST.getlist ( "resVillesUpdate" )
        periode = request.POST["unite"]
        frequence = request.POST["valeur"]
        mangeUpdateRestaurent.mangeRestaurent ( periode , frequence , villes )
        table = Restaurant.objects ()
        print ( len ( table ) )
        if (len ( table )) == 1:
            print ( "dcvgt" )
            mangeDeleteRestaurent.mangerestaurant ( "minute" , "2" )
        context = {
            'message': 'La mise à jour atomatique de la table Restaurent est lancée' ,
            'categorie': categorie ,
            'tab': tab
        }
        return context

    if categorie == 'manageTravel' and len(request.POST.getlist ( "attVillesUpdate" )) != 0:
        villes = request.POST.getlist ( "attVillesUpdate" )
        periode = request.POST["unite"]
        frequence = request.POST["valeur"]
        mangeUpdateAttraction.mangeAttraction ( periode , frequence , villes )
        table = Activity.objects ()
        print ( len ( table ) )
        if (len ( table )) == 1:
            print ( "dcvgt" )
            mangeDeleteAttraction.mangeattraction ( "minute" , "2" )
        context = {
            'message': 'La mise à jour atomatique de la table Activité est lancée' ,
            'categorie': categorie ,
            'tab': tab
        }
        return context

    if categorie == 'manageDeals':
        villes = request.POST.getlist ( "VillesUpdate" )
        periode = request.POST["unite"]
        frequence = request.POST["valeur"]
        mangeUpdateBien.mangeBien ( periode , frequence , villes )
        table = Bien.objects ()
        print ( len ( table ) )
        if (len ( table )) == 1:
            print ( "dcvgt" )
            mangeDeleteBien.mangeBien ( "minute" , "2" )
        context = {
            'message': 'La mise à jour atomatique de la table Bien est lancée' ,
            'categorie': categorie ,
            'tab': tab
        }
        return context



def delete ( request,categorie,tab ):
    if request.method == 'POST':
        critere = str ( request.POST )
        if critere.find ( "categorie" ) != -1:
            table = Product.objects.filter ( categorie=request.POST["categorie"] )
            table.delete ()
            es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )
            es.indices.delete ( index=request.POST["categorie"] .lower ()  , ignore=[400 , 404] )
            table = Product.objects ()
            if (len ( table )) == 0:
                os.popen ( r"SCHTASKS /delete /tn taskProductDelete" )
                os.popen ( r"SCHTASKS /delete /tn taskProduct" )

            fichier = open (
                "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateProduct/update.txt" , "r" )
            contenu = ""
            for ligne in fichier:
                if not (request.POST["categorie"] in ligne):
                    contenu = contenu + "\n" + fichier.readline ( ligne )
            fichier.close ()

            fichier = open (
                'C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateProduct/update.txt' , 'w' )
            fichier.write ( contenu )
            fichier.close ()
            context = {
                'message': 'La suppresion  des produits de :' + request.POST["categorie"] ,
                'categorie': categorie ,
                'tab': tab
            }
            return context

        if critere.find ( "villeH" ) != -1:
            table = Hotel.objects.filter ( villeHotel=request.POST["villeH"] )
            table.delete ()
            es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )
            es.indices.delete ( index=request.POST["villeH"].lower () , ignore=[400 , 404] )
            table = Hotel.objects ()
            if (len ( table )) == 0:
                os.popen ( r"SCHTASKS /delete /tn taskHotelDelete  /f" )
                os.popen ( r"SCHTASKS /delete /tn taskHotel  /f" )

            fichier = open ( "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateHotel/update.txt" ,
                             "r" )
            contenu = ""
            for ligne in fichier:
                if not (request.POST["villeH"] in ligne):
                    contenu = contenu + "\n" + fichier.readline ( ligne )
            fichier.close ()

            fichier = open ( 'C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateHotel/update.txt' ,
                             'w' )
            fichier.write ( contenu )
            fichier.close ()
            context = {
                'message': 'La suppresion des hotels de '+ request.POST["villeH"] ,
                'categorie': categorie ,
                'tab': tab
            }
            return context
        if critere.find ( "villeR" ) != -1:
            table = Restaurant.objects.filter ( villeRestaurant=request.POST["villeR"] )
            table.delete ()
            es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )
            es.indices.delete ( index=request.POST["villeR"].lower () , ignore=[400 , 404] )
            table = Restaurant.objects ()
            if (len ( table )) == 0:
                os.popen ( r"SCHTASKS /delete /tn taskRestaurentDelete  /f" )
                os.popen ( r"SCHTASKS /delete /tn taskRestaurent  /f" )

            fichier = open (
                "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateRestaurent/update.txt" ,
                "r" )
            contenu = ""
            for ligne in fichier:
                if not (request.POST["villeR"] in ligne):
                    contenu = contenu + "\n" + fichier.readline ( ligne )
            fichier.close ()

            fichier = open (
                'C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/UpdateRestaurent/update.txt' ,
                'w' )
            fichier.write ( contenu )
            fichier.close ()
            context = {
                'message': 'La suppresion  des restaurents de' +request.POST["villeR"] ,
                'categorie': categorie ,
                'tab': tab
            }
            return context

        if critere.find ( "villeA" ) != -1:
            table = Activity.objects.filter ( villeActivites=request.POST["villeA"] )
            table.delete ()
            es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )
            es.indices.delete ( index=request.POST["villeA"].lower () , ignore=[400 , 404] )
            table = Activity.objects ()
            if (len ( table )) == 0:
                os.popen ( r"SCHTASKS /delete /tn taskAttractionDelete  /f" )
                os.popen ( r"SCHTASKS /delete /tn taskAttraction  /f" )
                print ( "dddd" )
            fichier = open (
                "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/updateAttraction/update.txt" ,
                "r" )
            contenu = ""
            for ligne in fichier:
                if not (request.POST["villeA"] in ligne):
                    contenu = contenu + "\n" + fichier.readline ( ligne )
            fichier.close ()

            fichier = open (
                'C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/updateAttraction/update.txt' ,
                'w' )
            fichier.write ( contenu )
            fichier.close ()
            context = {
                'message': 'La suppresion  des activités de'+ request.POST["villeA"]  ,
                'categorie': categorie ,
                'tab': tab
            }
            return context

        if critere.find ( "villeBI" ) != -1:
            table = Bien.objects.filter ( ville=request.POST["villeBI"] )
            table.delete ()
            table = Bien.objects ()
            if (len ( table )) == 0:
                os.popen ( r"SCHTASKS /delete /tn taskBienDelete  /f" )
                os.popen ( r"SCHTASKS /delete /tn taskBien  /f" )
                print ( "dddd" )
            fichier = open (
                "C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/updateBien/update.txt" ,
                "r" )
            contenu = ""
            for ligne in fichier:
                if not (request.POST["villeBI"] in ligne):
                    contenu = contenu + "\n" + fichier.readline ( ligne )
            fichier.close ()

            fichier = open (
                'C:/Users/nidou/Desktop/tunisia-commerce/tunisia_commerceUpdate/updateBien/update.txt' ,
                'w' )
            fichier.write ( contenu )
            fichier.close ()
            context = {
                'message': 'La suppresion  des biens immobliers de' + request.POST["villeBI"]  ,
                'categorie': categorie ,
                'tab': tab
            }
            return context

# les fonctions d'affichage

def showListe(request,categorie,tab,o):


 if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
            "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
        "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
        "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :
        return render ( request , '404.html' )
 categories = []
 if categorie == 'manageMagasin':
    table = Product.objects.filter ( categorie=o )
    if len ( table ) == 0:
        return render ( request , '404.html' )
    liste = []
    sub_catégorie=[]
    for i in range ( 0 , len ( table[0]["produitList"] ) ):
        liste.append (table[0]["produitList"] [i] )
        if not find ( table[0]["produitList"][i]["subCategorie"] , sub_catégorie ):
            sub_catégorie.append ( table[0]["produitList"][i]["subCategorie"] , )
    table = Product.objects ()
    if len ( table ) != 0:
        for i in range ( 0 , len ( table ) ):
            categories.append ( table[i].categorie )
    context = {
        'productCategorie': categories ,
        'produit': liste ,
        'keyword': o ,
        'categorie': categorie ,
        'tab': tab ,
        'cat': sub_catégorie,
        "showKeywordbord": 'oui'
    }

 if categorie == 'manageTravel':
     table = Hotel.objects ()
     table1 = Restaurant.objects ( )
     table2 = Activity.objects(  )


     afficheA = ""
     afficheH = ""
     afficheR = ""

     if len ( table ) == 0:
         afficheH = "non"

     if len ( table1 ) == 0:
         afficheR = "non"

     if len ( table2 ) == 0:
         afficheA = "non"

     if len(Hotel.objects ().filter(villeHotel =o)) == 0 or len(Restaurant.objects ().filter(villeRestaurant =o)) == 0 or len(Activity.objects ().filter(villeActivites =o)) == 0 :
         affiche ="non"

     else :
         affiche = "oui"
     if tab =="showHotels":

        if len(table) == 0 :
                return render ( request , '404.html' )
        liste = []
        adresses=[]
        table=Hotel.objects().filter(villeHotel=o)
        for i in range ( 0 , len ( table[0]["hotelList"] ) ):
            liste.append ( table[0]["hotelList"][i] )
            adresse = table[0]["hotelList"][i]["place"].replace ( "\n" , " " ).split ( "," )
            if len(adresse)>=3:
             adresse=adresse[len(adresse)-3]
             if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                 adresses.append(adresse)
        table = Hotel.objects ()
        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):
                categories.append ( table[i].villeHotel )
        context = {
            'productCategorie': categories ,
            'produit': liste ,
            'keyword': o ,
            'categorie': categorie ,
            'tab': tab ,
            'arround': adresses ,
             "showKeywordbord": affiche,
            'afficheH': afficheH ,
            'afficheR': afficheR ,
            'afficheA': afficheA
        }

     if tab == "showRestaurents":
         table = Restaurant.objects.filter ( villeRestaurant=o )
         if len ( table ) == 0:
             return render ( request , '404.html' )
         liste = []
         adresses = []
         for i in range ( 0 , len ( table[0]["restaurantList"] ) ):
             liste.append ( table[0]["restaurantList"][i] )
             adresse = table[0]["restaurantList"][i]["adresse"].replace ( "\n" , "" )
             if not find ( adresse , adresses ) and adresse != "":
                     print ( adresse + "dddd1" )
                     adresses.append ( adresse )
         table = Restaurant.objects ()
         if len ( table ) != 0:
             for i in range ( 0 , len ( table ) ):
                 categories.append ( table[i].villeRestaurant )

         context = {
             'productCategorie': categories ,
             'produit': liste ,
             'keyword': o ,
             'categorie': categorie ,
             'tab': tab ,
             'arround': adresses ,
             'showKeywordbord': affiche,
             'afficheH': afficheH ,
             'afficheR': afficheR ,
             'afficheA': afficheA
         }


     if tab == "showActivities":
         table = Activity.objects.filter ( villeActivites=o )
         if len ( table ) == 0:
             return render ( request , '404.html' )
         liste = []
         adresses = []
         type=[]
         for i in range ( 0 , len ( table[0]["activitiesList"] ) ):
             liste.append ( table[0]["activitiesList"][i] )
             adresse = table[0]["activitiesList"][i]["place"].replace ( "\n" , "" )
             if not find ( table[0]["activitiesList"][i]["type"],type ):
                 type.append ( table[0]["activitiesList"][i]["type"] )
             if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                     print ( adresse + "dddd" )
                     adresses.append ( adresse )
         table = Activity.objects ()
         if len ( table ) != 0:
             for i in range ( 0 , len ( table ) ):
                 categories.append ( table[i].villeActivites )

         context = {
             'productCategorie': categories ,
             'produit': liste ,
             'keyword': o ,
             'categorie': categorie ,
             'tab': tab ,
             'arround': adresses ,
             'type': type,
             'showKeywordbord': affiche,
             'afficheH': afficheH ,
             'afficheR': afficheR ,
             'afficheA': afficheA
         }


 if categorie == 'manageDeals':
     table = Bien.objects ()
     if len ( table ) == 0:
         return render ( request , '404.html' )
     table = Bien.objects ().to_json ()
     table = json.loads ( table )



     if str ( table ).find ( "_vendre" ) != -1:
         afficheV = 'true'
     else:
         afficheV = 'false'

     if str ( table ).find ( "_louer" ) != -1:
         afficheL = 'true'
     else:
         afficheL = 'false'

     categories = []
     if len ( table ) != 0:
         for i in range ( 0 , len ( table ) ):
             if tab == "showSales":
                 if str ( table[i] ).find ( "_a_vendre" ):
                     categories.append ( table[i]["ville"] )

             if tab == "showRent":
                 if str ( table[i] ).find ( "_a_louer" ):
                     categories.append ( table[i]["ville"] )

     listeMaison = []
     listeApp = []
     listeTer = []
     adresses = []
     table = Bien.objects.filter ( ville=o ).to_json()
     table = json.loads ( table )
     if tab == "showSales":

         if str ( table[0] ).find ( "maison_a_vendre" ) != -1:

             for i in range ( 0 , len ( table[0]["maison_a_vendre"] ) ):
                 listeMaison.append ( table[0]["maison_a_vendre"][i] )
         if str ( table[0] ).find ( "appartement_a_vendre" ) != -1:
             for i in range ( 0 , len ( table[0]["appartement_a_vendre"] ) ):
                 listeApp.append ( table[0]["appartement_a_vendre"][i] )
         if str ( table[0] ).find ( "terrain_a_vendre" ) != -1:
             for i in range ( 0 , len ( table[0]["terrain_a_vendre"] ) ):
                 listeTer.append ( table[0]["terrain_a_vendre"][i] )

     if tab == "showRent":
         if str ( table[0] ).find ( "maison_a_louer" ) != -1:
             for i in range ( 0 , len ( table[0]["maison_a_louer"] ) ):
                 listeMaison.append ( table[0]["maison_a_louer"][i] )
         if str ( table[0] ).find ( "appartement_a_louer" ) != -1:
             for i in range ( 0 , len ( table[0]["appartement_a_louer"] ) ):
                 listeApp.append ( table[0]["appartement_a_louer"][i] )

     context = {
         'productCategorie': categories ,
         'categorie': categorie ,
         'tab': tab ,
         'maison': listeMaison ,
         'appartement': listeApp ,
         'terrain': listeTer ,
         'keyword': o ,
         'arround': adresses,
         "afficheL":afficheL,
         "afficheV":afficheV
     }



 return render(request, 'showListe.html', context)

def showDetails(request,categorie,tab,keyword,name,c):

  if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
          "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
      "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
      "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :

      return render ( request , '404.html' )


  if categorie =="manageMagasin":
   if keyword !="all"  :
    table = Product.objects.filter ( categorie=keyword )
   else:
       table = Product.objects ()
       table = Product.objects.filter ( categorie=  table[0].categorie  )

   if len ( table ) == 0:
       return render ( request , '404.html' )

   for i in range ( 0 , len ( table[0]["produitList"] ) ):
         if table[0]["produitList"][i]["name"] ==name:
             product=table[0]["produitList"][i]
             context = {
                 'produit': product ,
                 'categorie': categorie ,
                 'tab': tab,
                 'keyword':keyword
             }


             return render ( request , 'showDetails.html' , context )

   return render ( request , '404.html' , )
  if categorie == "manageTravel":
    table = Hotel.objects.filter (  )
    table1 = Restaurant.objects.filter (  )
    table2 = Activity.objects.filter (  )

    afficheA = ""
    afficheH = ""
    afficheR = ""

    if len ( table ) == 0:
      afficheH = "non"

    if len ( table1 ) == 0:
          afficheR = "non"

    if len ( table2 ) == 0:
          afficheA = "non"

    if tab =="showHotels":


      if keyword != "all":
             table = Hotel.objects.filter ( villeHotel=keyword )
      else:
             table = Hotel.objects ()
             table = Hotel.objects.filter ( villeHotel=table[0]. villeHotel )

      if len ( table ) == 0:
          return render ( request , '404.html' )

      for i in range ( 0 , len ( table[0]["hotelList"] ) ):
         print(table[0]["hotelList"][i]["name"])
         if table[0]["hotelList"][i]["name"].find(name) != -1 or name.find(table[0]["hotelList"][i]["name"])!=-1 :

             product=table[0]["hotelList"][i]
             context = {
                 'produit': product ,
                 'categorie': categorie ,
                 'tab': tab,
                 'keyword':keyword,
                'afficheH': afficheH ,
                'afficheR': afficheR ,
                'afficheA': afficheA
             }

             return render ( request , 'showDetails.html' , context )

      return render ( request , '404.html' ,  )
    if tab =="showRestaurents":
      if keyword != "all":
             table = Restaurant.objects.filter ( villeRestaurant=keyword )
      else:
             table = Restaurant.objects ()
             table = Restaurant.objects.filter ( villeRestaurant=table[0]. villeRestaurant )

      if len ( table ) == 0:
          return render ( request , '404.html' )
      for i in range ( 0 , len ( table[0]["restaurantList"] ) ):
         print(table[0]["restaurantList"][i]["name"])
         if table[0]["restaurantList"][i]["name"].find(name) != -1 or name.find(table[0]["restaurantList"][i]["name"])!=-1 :

             product=table[0]["restaurantList"][i]
             context = {
                 'produit': product ,
                 'categorie': categorie ,
                 'tab': tab,
                 'keyword':keyword,
                       'afficheH': afficheH ,
                                   'afficheR': afficheR ,
             'afficheA': afficheA
             }

             return render ( request , 'showDetails.html' , context )

    if tab == "showActivities":
        if keyword != "all":
            table = Activity.objects.filter ( villeActivites=keyword )
        else:
            table = Activity.objects ()
            table = Activity.objects.filter ( villeActivites=table[0].villeActivites )
        if len ( table ) == 0:
            return render ( request , '404.html' )
        for i in range ( 0 , len ( table[0]["activitiesList"] ) ):
            print ( table[0]["activitiesList"][i]["name"] )
            if table[0]["activitiesList"][i]["name"].find ( name ) != -1 or name.find (
                    table[0]["activitiesList"][i]["name"] ) != -1:
                product = table[0]["activitiesList"][i]
                context = {
                    'produit': product ,
                    'categorie': categorie ,
                    'tab': tab ,
                    'keyword': keyword,
                          'afficheH': afficheH ,
                                      'afficheR': afficheR ,
                'afficheA': afficheA
                }
                print(afficheA)
                return render ( request , 'showDetails.html' , context )
    return render ( request , '404.html' , )


def showDetails1(request,categorie,tab,keyword,typeBien,name,c):
      product=""
      if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
              "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
          "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
          "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :
          return render ( request , '404.html' )

      if keyword == 'all':
       table = Bien.objects ().to_json ()
       table = json.loads ( table )
       keyword = table[0]["ville"]
      else :
       table = Bien.objects.filter ( ville=keyword ).to_json ()
       table = json.loads ( table )



      if len ( table ) == 0:
          return render ( request , '404.html' )

      table = Bien.objects ().to_json ()
      table = json.loads ( table )

      if str ( table ).find ( "_vendre" ) != -1:
          afficheV = 'true'
      else:
          afficheV = 'false'

      if str ( table ).find ( "_louer" ) != -1:
          afficheL = 'true'
      else:
          afficheL = 'false'

      if tab == "showSales":
          if typeBien == "maison" :
            print ( "hello" )
            for i in range ( 0 , len ( table[0]["maison_a_vendre"] ) ):

                if name== table[0]["maison_a_vendre"][i] ["name"] :
                    product= table[0]["maison_a_vendre"][i]
                    break

          if typeBien == "appartement" :
              for i in range ( 0 , len ( table[0]["appartement_a_vendre"] ) ):
                  if name == table[0]["appartement_a_vendre"][i]["name"]:
                      product = table[0]["appartement_a_vendre"][i]
                      break
          if   typeBien == "terrain" :
              for i in range ( 0 , len ( table[0]["terrain_a_vendre"] ) ):
                  if name.replace ( "terrain" , "" ) == table[0]["terrain_a_vendre"][i]["name"]:
                      product = table[0]["terrain_a_vendre"][i]
                      break

      if tab == "showRent":
          if typeBien == "maison" :
              for i in range ( 0 , len ( table[0]["maison_a_louer"] ) ):
                  if name == table[0]["maison_a_louer"][i]["name"]:
                      product = table[0]["maison_a_louer"][i]
                      break

          if typeBien == "appartement" :
              for i in range ( 0 , len ( table[0]["appartement_a_louer"] ) ):
                  if name == table[0]["appartement_a_louer"][i]["name"]:
                      product = table[0]["appartement_a_louer"][i]
                      break

      if product == "":
          return render ( request , '404.html' , )
      context = {

          'categorie': categorie ,
          'tab': tab ,
          'produit': product ,
          'keyword':keyword,
          'afficheL' :afficheL,
          'afficheV' : afficheV


      }

      return render ( request , 'showDetails.html' , context=context )

def show(request,categorie,tab):

    if  categorie == 'manageMagasin':
        table = Product.objects ()
        categories = []
        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):
                categories.append ( table[i].categorie )


            table = Product.objects.filter ( categorie=categories[0] )
            if len ( table ) == 0:
                return render ( request , '404.html' )
            liste = []
            sub_catégorie=[]
            for i in range ( 0 , len ( table[0]["produitList"] ) ):
                liste.append ( table[0]["produitList"][i] )
                if not find(table[0]["produitList"][i] ["subCategorie"],sub_catégorie) :
                    sub_catégorie.append(table[0]["produitList"][i] ["subCategorie"],)

            context = {
                'productCategorie': categories ,
                'categorie': categorie ,
                'tab': tab,
                'all': liste ,
                'keyword': 'all' ,
                'cat':sub_catégorie
            }

            return render ( request , 'admin.html' , context=context )

    if categorie == 'manageTravel':
      table = Hotel.objects ()
      table1 = Restaurant.objects ()
      table2 = Activity.objects ()
      afficheA=""
      afficheH=""
      afficheR=""
      if len(table) == 0 :
          afficheH = "non"

      if len(table1) == 0:
          afficheR = "non"

      if len(table2) == 0 :
          afficheA  ="non"
      if tab=="showHotels":

        categories = []
        if len ( table ) != 0:
            for i in range ( 0 , len ( table ) ):
                categories.append ( table[i].villeHotel )

            table = Hotel.objects.filter ( villeHotel=categories[0] )

            if len ( table ) == 0:
                return render ( request , '404.html' )
            liste = []

            adresses = []
            for i in range ( 0 , len ( table[0]["hotelList"] ) ):
                liste.append ( table[0]["hotelList"][i] )
                adresse = table[0]["hotelList"][i]["place"].replace("\n","").split ( "," )
                if len ( adresse ) >= 3:
                    adresse = adresse[len ( adresse ) - 3]
                    if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                        print(adresse+"dddd")
                        adresses.append ( adresse )

            context = {
                'productCategorie': categories ,
                'categorie': categorie ,
                'tab': tab ,
                'all': liste,
                'keyword':'all',
                'arround':adresses,
                'afficheH':afficheH,
                'afficheR': afficheR ,
                'afficheA' : afficheA
            }

            return render ( request , 'admin.html' , context=context )

      if tab == "showRestaurents":

            categories = []
            if len ( table1 ) != 0:
                for i in range ( 0 , len ( table1 ) ):
                    categories.append ( table1[i].villeRestaurant )

                table = Restaurant.objects.filter ( villeRestaurant=categories[0] )

                if len ( table ) == 0:
                    return render ( request , '404.html' )

                liste = []
                adresses = []
                for i in range ( 0 , len ( table[0]["restaurantList"] ) ):
                    liste.append ( table[0]["restaurantList"][i] )
                    adresse = table[0]["restaurantList"][i]["adresse"].replace ( "\n" , "" )
                    if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                            print ( adresse + "dddd" )
                            adresses.append ( adresse )
                context = {
                    'productCategorie': categories ,
                    'categorie': categorie ,
                    'tab': tab ,
                    'all': liste ,
                    'keyword': 'all' ,
                    'arround': adresses,
                    'afficheH': afficheH ,
                    'afficheR': afficheR ,
                    'afficheA': afficheA

                }

                return render ( request , 'admin.html' , context=context )

      if tab == "showActivities":

            categories = []
            if len ( table2 ) != 0:
                for i in range ( 0 , len ( table2 ) ):
                    categories.append ( table2[i]. villeActivites)

                table = Activity.objects.filter ( villeActivites=categories[0] )

                if len ( table ) == 0:
                    return render ( request , '404.html' )
                liste = []
                adresses = []
                type=[]
                for i in range ( 0 , len ( table[0]["activitiesList"] ) ):
                    liste.append ( table[0]["activitiesList"][i] )
                    adresse = table[0]["activitiesList"][i]["place"].replace ( "\n" , "" )
                    if not find ( table[0]["activitiesList"][i]["type"] ,type ):
                      type.append(table[0]["activitiesList"][i]["type"])

                    if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                            print ( adresse + "dddd" )
                            adresses.append ( adresse )
                context = {
                    'productCategorie': categories ,
                    'categorie': categorie ,
                    'tab': tab ,
                    'all': liste ,
                    'keyword': 'all' ,
                    'arround': adresses,
                    'type':type,
                    'afficheH': afficheH ,
                    'afficheR': afficheR ,
                    'afficheA': afficheA

                }

                return render ( request , 'admin.html' , context=context )
    if categorie == 'manageDeals':

            table = Bien.objects ().to_json ()
            table = json.loads ( table )


            if str ( table ).find ( "_vendre" ) != -1:
                afficheV = 'true'
            else:
                afficheV = 'false'

            if str ( table ).find ( "_louer" ) != -1:
                afficheL = 'true'
            else:
                afficheL = 'false'


            categories = []
            if len ( table ) != 0:
             for i in range ( 0 , len ( table ) ):
              if tab=="showSales":
                 if str(table[i]).find("_a_vendre"):
                    categories.append ( table[i]["ville"] )

              if tab == "showRent":
                  if str ( table[i] ).find ( "_a_louer" ):
                      categories.append ( table[i]["ville"] )


            listeMaison = []
            listeApp=[]
            listeTer=[]
            adresses = []
            if tab == "showSales":
                 print( table[0])
                 if str(table[0]).find("maison_a_vendre") != -1 :

                  for i in range ( 0 , len ( table[0]["maison_a_vendre"] ) ):
                      listeMaison.append ( table[0]["maison_a_vendre"][i] )
                 if str ( table[0] ).find ( "appartement_a_vendre" ) != -1:
                  for i in range ( 0 , len ( table[0]["appartement_a_vendre"] ) ):
                      listeApp .append ( table[0]["appartement_a_vendre"][i] )
                 if str ( table[0] ).find ( "terrain_a_vendre" ) != -1:
                     for i in range ( 0 , len ( table[0]["terrain_a_vendre"] ) ):
                         listeTer .append ( table[0]["terrain_a_vendre"][i] )

            if tab == "showRent":
                if str ( table[0] ).find ( "maison_a_louer" ) != -1:
                    for i in range ( 0 , len ( table[0]["maison_a_louer"] ) ):
                        listeMaison.append ( table[0]["maison_a_louer"][i] )
                if str ( table[0] ).find ( "appartement_a_louer" ) != -1:
                    for i in range ( 0 , len ( table[0]["appartement_a_louer"] ) ):
                        listeApp .append ( table[0]["appartement_a_louer"][i] )

            print(categories)
            context = {
                    'productCategorie': categories ,
                    'categorie': categorie ,
                    'tab': tab ,
                    'maison': listeMaison ,
                    'appartement': listeApp ,
                     'terrain':listeTer,
                    'keyword': 'all' ,
                    'arround': adresses,
                'afficheV': afficheV ,
                'afficheL': afficheL

                }

            return render ( request , 'admin.html' , context=context )

    if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
            "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
        "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
        "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :
        return render ( request , '404.html' )

def showFilter(request,categorie,filter,tab,keyword):

  print(tab)
  if tab == "show":
    produit=[]

    table = Product.objects ()
    categories = []

    if len ( table ) != 0:
        for i in range ( 0 , len ( table ) ):
            categories.append ( table[i].categorie )


        es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )

        e1 = {'query': {"bool": {

            "must": []}}}

        if   int(request.POST["count1" ])!= 0 :
            e1["query"]["bool"]["must"].append(  {"range": {
                        "price": {
                            "gte": int(request.POST["count" ]) ,
                            "lte":  int(request.POST["count1" ]),

                        }
                    }
                })

        if  len(request.POST.getlist ( "note" ))!= 0:
                    note = int(request.POST.getlist ( "note" )[0])
                    e1["query"]["bool"]["must"].append ( {"range": {
                        "note": {

                            "gte": note ,

                        }
                    }
                    } )



        if len(request.POST.getlist ( "catégorie" ))!= 0:
                    e1["query"]["bool"]["must"].append (
                        {"match": {"subCategorie": {'query':str(request.POST.getlist ( "catégorie" ) ).replace("[","").replace("]","").replace(","," ").replace("'","") , "operator": "or" , "analyzer": "standard"}}} )

        print(e1)
        k = keyword
        if keyword == "all":
            keyword = categories[0]

        res = es.search ( index=keyword.lower ()  , body=e1 , request_timeout=300 , size="10000" )
        for hit in res['hits']['hits']:
            produit.append ( hit["_source"] )

        adresses = []
        table = Product.objects.filter ( categorie=keyword )
        sub_catégorie = []
        for i in range ( 0 , len ( table[0]["produitList"] ) ):
            if not find ( table[0]["produitList"][i]["subCategorie"] , sub_catégorie ):
                sub_catégorie.append ( table[0]["produitList"][i]["subCategorie"] , )



        context = {
            'productCategorie': categories ,
            'categorie': categorie ,
            'tab': tab ,
            'all': produit,
            'keyword':k,
            'arround':adresses,
            'cat': sub_catégorie
        }

        return render ( request , 'admin.html' , context=context )


  if categorie == "manageTravel" :

   table = Hotel.objects ()
   table1 = Restaurant.objects ()
   table2 = Activity.objects ()

   afficheA = ""
   afficheH = ""
   afficheR = ""

   if len ( table ) == 0:
          afficheH = "non"

   if len ( table1 ) == 0:
          afficheR = "non"

   if len ( table2 ) == 0:
          afficheA = "non"

   if tab == "showHotels":

    categories = []
    if len ( table ) != 0:
        for i in range ( 0 , len ( table ) ):
            categories.append ( table[i].villeHotel )


        es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )

        e1 = {'query': {"bool": {

            "must": []}}}

        if len(request.POST.getlist ( "étoile" ))!= 0:
                    e1["query"]["bool"]["must"].append (
                        {"match": {"étoile": {"query": "hôtel "+str(request.POST.getlist ( "étoile" )).replace("[","").replace("]","") , "operator": "and" , "analyzer": "standard"}}} )

        if  len(request.POST.getlist ( "Arrondissements" ))!= 0:
                    e1["query"]["bool"]["must"].append (
                        {"match": {"place": {'query': str(request.POST.getlist ( "Arrondissements" )).replace("[","").replace("]","").replace(","," ").replace("'",""), "operator": "or" , "analyzer": "standard"}}} )
        if len(request.POST.getlist ( "équipement" ))!= 0:
                    e1["query"]["bool"]["must"].append (
                        {"match": {"point": {'query':str(request.POST.getlist ( "équipement" ) ).replace("[","").replace("]","").replace(","," ").replace("'","") , "operator": "and" , "analyzer": "standard"}}} )

        if len(request.POST.getlist ( "type" ))!= 0:
                    e1["query"]["bool"]["must"].append (
                        {"match": {"type": {'query':str(request.POST.getlist ( "type" ) ).replace("[","").replace("]","").replace(","," ").replace("'","") , "operator": "and" , "analyzer": "standard"}}} )

        if len ( request.POST.getlist ( "note" ) ) != 0:
            note = str ( request.POST.getlist ( "note" ) ).replace ( "Fabuleux : 9+" , "Fabuleux" ).replace("Superbe : 8,5+","Superbe").replace (
                "Très_bien : 8+" , "Très_bien" ).replace ( "Bien: 7 +" , "Bien" ).replace ( "Agréable: 6" , "Agréable" )

            e1["query"]["bool"]["must"].append (
                {"match": {"mention": {
                    'query': note.replace ( "[" , "" ).replace ( "]" , "" ).replace (
                        "," , " " ).replace ( "'" , "" ) , "operator": "or" , "analyzer": "standard"}}} )

        hotels=[]
        k=keyword
        if keyword == "all":
         keyword = categories[0]
        adresses = []
        table = Hotel.objects.filter ( villeHotel=keyword )
        for i in range ( 0 , len ( table[0]["hotelList"] ) ):
            adresse = table[0]["hotelList"][i]["place"].replace ( "\n" , " " )
            if not find(adresse.replace("\n"," "),adresses) and  adresse != "":
               adresses.append ( adresse )

        res = es.search ( index=keyword.lower()+"hotel" , body=e1 , request_timeout=300 , size="10000" )
        for hit in res['hits']['hits']:
            hotels.append( hit["_source"] )

        context = {
            'productCategorie': categories ,
            'categorie': categorie ,
            'tab': tab ,
            'all': hotels,
            'keyword':k,
            'arround':adresses,
            'afficheA':afficheA ,
            'afficheH': afficheH ,
             'afficheR': afficheR
        }

        return render ( request , 'admin.html' , context=context )


   if tab == "showRestaurents":
        table1 = Restaurant.objects ()

        categories = []
        if len ( table1 ) != 0:
            for i in range ( 0 , len ( table1 ) ):
                categories.append ( table1[i].villeRestaurant )

            es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )

            e1 = {'query': {"bool": {

                "must": []}}}

            if len ( request.POST.getlist ( "repas" ) ) != 0:
                e1["query"]["bool"]["must"].append (
                    {"match": {"repas": {
                        "query":   str ( request.POST.getlist ( "repas" ) ).replace ( "[" , "" ).replace (
                            "]" , "" ) , "operator": "and" , "analyzer": "standard"}}} )

            if len ( request.POST.getlist ( "Arrondissements" ) ) != 0:
                e1["query"]["bool"]["must"].append (
                    {"match": {"adresse": {
                        'query': str ( request.POST.getlist ( "Arrondissements" ) ).replace ( "'" , "" ) .replace ( "[" , "" ).replace ( "]" ,
                                                                                                                   "" ) , "operator": "or" ,
                        "analyzer": "standard"}}} )
            if len ( request.POST.getlist ( "régime" ) ) != 0:
                e1["query"]["bool"]["must"].append (
                    {"match": {"Régimes": {
                        'query': str ( request.POST.getlist ( "régime" ) ).replace ( "[" , "" ).replace ( "]" ,
                                                                                                              "" ).replace (
                            "," , " " ).replace ( "'" , "" ) , "operator": "and" , "analyzer": "standard"}}} )

            if len ( request.POST.getlist ( "cuisine" ) ) != 0:
                e1["query"]["bool"]["must"].append (
                    {"match": {"cuisine": {
                        'query': str ( request.POST.getlist ( "cuisine" ) ).replace ( "[" , "" ).replace ( "]" ,
                                                                                                        "" ).replace (
                            "," , " " ).replace ( "'" , "" ) , "operator": "and" , "analyzer": "standard"}}} )


            print(e1)
            restaurents = []
            k = keyword
            if keyword == "all":
                keyword = categories[0]
            adresses = []
            table = Restaurant.objects.filter ( villeRestaurant=keyword )
            for i in range ( 0 , len ( table[0]["restaurantList"] ) ):
                adresse = table[0]["restaurantList"][i]["adresse"].replace ( "\n" , "" )
                if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                        print ( adresse + "dddd" )
                        adresses.append ( adresse )

            res = es.search ( index=keyword.lower ()+"restaurant" , body=e1 , request_timeout=300 , size="10000" )
            if str ( e1 ).find ( "adresse" ) != -1:
             for hit in res['hits']['hits']:
                if(hit["_source"]["adresse"] in request.POST.getlist ( "Arrondissements" )  ):
                   restaurents.append ( hit["_source"] )

            else :
                for hit in res['hits']['hits']:
                        restaurents.append ( hit["_source"] )
            context = {
                'productCategorie': categories ,
                'categorie': categorie ,
                'tab': tab ,
                'all': restaurents ,
                'keyword': k ,
                'arround': adresses,
                 'afficheA':afficheA ,
                 'afficheH': afficheH ,
                  'afficheR': afficheR
            }

            return render ( request , 'admin.html' , context=context )

   if tab == "showActivities":
      table2 = Activity.objects ()

      categories = []
      if len ( table2 ) != 0:
          for i in range ( 0 , len ( table2 ) ):
              categories.append ( table2[i].villeActivites )

          es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )

          e1 = {'query': {"bool": {

              "must": []}}}

          if len ( request.POST.getlist ( "note" ) ) != 0:
              e1["query"]["bool"]["must"].append (
                  {"match": {"note": {
                      "query": str ( request.POST.getlist ( "note" ) ).replace ( "[" , "" ).replace (
                          "]" , "" ) , "operator": "or" , "analyzer": "standard"}}} )

          if len ( request.POST.getlist ( "Arrondissements" ) ) != 0:
              e1["query"]["bool"]["must"].append (
                  {"match": {"place": {
                      'query': str ( request.POST.getlist ( "Arrondissements" ) ).replace ( "'" , "" ).replace ( "[" ,
                                                                                                                 "" ).replace (
                          "]" ,
                          "" ) , "operator": "or" ,
                      "analyzer": "standard"}}} )
          if len ( request.POST.getlist ( "durée" ) ) != 0:
              e1["query"]["bool"]["must"].append (
                  {"match": {"durée": {
                      'query': str ( request.POST.getlist ( "durée" ) ).replace ( "[" , "" ).replace ( "]" ,
                                                                                                        "" ).replace (
                          "," , " " ).replace ( "'" , "" ) , "operator": "or" , "analyzer": "standard"}}} )

          if len ( request.POST.getlist ( "type" ) ) != 0:
              e1["query"]["bool"]["must"].append (
                  {"match": {"type": {
                      'query': str ( request.POST.getlist ( "type" ) ).replace ( "[" , "" ).replace ( "]" ,
                                                                                                         "" ).replace (
                          "," , " " ).replace ( "'" , "" ) , "operator": "or" , "analyzer": "standard"}}} )


          print(e1)
          attractions = []
          k = keyword
          if keyword == "all":
              keyword = categories[0]
          adresses = []
          type=[]
          table = Activity.objects.filter ( villeActivites=keyword )
          for i in range ( 0 , len ( table[0]["activitiesList"] ) ):
              adresse = table[0]["activitiesList"][i]["place"].replace ( "\n" , "" )
              if not find ( table[0]["activitiesList"][i]["type"] , type ):
                  type.append ( table[0]["activitiesList"][i]["type"] )
              if not find ( adresse.replace ( "\n" , " " ) , adresses ) and adresse != "":
                adresses.append ( adresse )

          res = es.search ( index=keyword.lower () + "attraction" , body=e1 , request_timeout=300 , size="10000" )
          if str ( e1 ).find ( "place" ) != -1:
              for hit in res['hits']['hits']:
                  if (hit["_source"]["place"] in request.POST.getlist ( "Arrondissements" )):
                      attractions.append ( hit["_source"] )

          else:
              for hit in res['hits']['hits']:
                  attractions.append ( hit["_source"] )

          context = {
              'productCategorie': categories ,
              'categorie': categorie ,
              'tab': tab ,
              'all': attractions ,
              'keyword': k ,
              'arround': adresses,
              'type' : type,
              'afficheA':afficheA,
              'afficheH':afficheH,
              'afficheR':afficheR
          }

          return render ( request , 'admin.html' , context=context )

  if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
          "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
      "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
      "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :

      return render ( request , '404.html' )

def showBord(request,categorie,tab,keyword,showKeywordbord):

  if categorie != "manageMagasin" and categorie != "manageTravel" and categorie != "manageDeals" or tab != "manage" and tab.find (
          "showActivities" ) == -1 and tab.find ( "showRestaurents" ) == -1 and tab.find (
      "showHotels" ) == -1 and tab.find ( "showActivities" ) == -1 and tab.find ( "showSales" ) == -1 and tab.find (
      "showRent" ) == -1 and tab != "show" and tab != "tableaubord" :
      return render ( request , '404.html' )


  if categorie == "manageTravel":
    table = Hotel.objects.filter ( villeHotel=keyword  )
    table1 = Restaurant.objects.filter ( villeRestaurant=keyword )
    table2 = Activity.objects.filter ( villeActivites=keyword )

    if len(table) == 0 or len(table2) ==0 or len(table1) == 0 :
        return render ( request , '404.html' )

    offres =0
    nums = []
    labels = []
    top =[]
    values =[]
    etoiles =[]
    valuese=[]
    places=[]
    valuesp=[]
    topr =[]
    valuesr =[]
    repas =[]
    cuisine=[]
    valr=[]
    valc=[]
    topa=[]
    valuesa=[]
    type = []
    valT = []
    duree = []
    vald = []

    if len ( table ) != 0:
        for i in range ( 0 , len ( table) ):

            offres += len ( table[0]["hotelList"] )

        nums.append ( offres )
        labels.append ( "Hôtels" )
    offres = 0
    if len ( table1 ) != 0:
        for i in range ( 0 , len ( table1 ) ):

            offres += len ( table1[0]["restaurantList"] )

        nums.append ( offres )
        labels.append ( "Restaurants" )
    offres = 0
    if len ( table2 ) != 0:
        for i in range ( 0 , len ( table2 ) ):
            offres += len ( table2[0]["activitiesList"] )

        nums.append ( offres )
        labels.append ( "Activités" )




    es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )

    res = es.search ( index=keyword.lower()+"hotel" , body={"query": {"match_all": {}} , "sort": [
        {"note.keyword": {"order": "desc"}}
    ]}
                      , request_timeout=300 , size="10000" )

    for i in range ( 0 , 5 ):
        top.append ( res['hits']['hits'][i]["_source"]["name"] )
        values.append ( res['hits']['hits'][i]["_source"]["note"] .replace(",","."))

    res = es.search ( index=keyword.lower()+"hotel"  , body={"aggs": {
        "group_by_place": {
            "terms": {
                "field": "place.keyword"
            }
        }
    }}, request_timeout=300 , size="10000" )
    for i in range ( 0 , len(res["aggregations"] ["group_by_place"]["buckets"])):
      if  res["aggregations"] ["group_by_place"]["buckets"][i] ["key"].find("voir_la_carte")== -1 :
        places.append (res["aggregations"] ["group_by_place"]["buckets"][i] ["key"].replace("_"," "))
        valuesp.append ( res["aggregations"] ["group_by_place"]["buckets"][i] ["doc_count"] )

    res = es.search ( index=keyword.lower () + "hotel" , body={"aggs": {
        "group_by_étoile": {
            "terms": {
                "field": "étoile.keyword"
            }
        }
    }} , request_timeout=300 , size="10000" )
    for i in range ( 0 , len ( res["aggregations"]["group_by_étoile"]["buckets"] ) ):
        etoiles.append ( res["aggregations"]["group_by_étoile"]["buckets"][i]["key"] )
        valuese.append ( res["aggregations"]["group_by_étoile"]["buckets"][i]["doc_count"] )

    res = es.search ( index=keyword.lower () + "restaurant" , body={"query": {"match_all": {}} , "sort": [
        {"note.keyword": {"order": "desc"}}
    ]}
                      , request_timeout=300 , size="10000" )

    for i in range ( 0 , 5 ):
        topr.append ( res['hits']['hits'][i]["_source"]["name"] )
        valuesr.append ( res['hits']['hits'][i]["_source"]["note"].replace ( "," , "." ) )

    res = es.search ( index=keyword.lower () + "restaurant" , body={"aggs": {
        "group_by_repas": {
            "terms": {
                "field": "repas.keyword"
            }
        }
    }} , request_timeout=300 , size="10000" )
    for i in range ( 0 , len ( res["aggregations"]["group_by_repas"]["buckets"] ) ):
            repas.append ( res["aggregations"]["group_by_repas"]["buckets"][i]["key"].replace ( "_" , " " ) )
            valr.append ( res["aggregations"]["group_by_repas"]["buckets"][i]["doc_count"] )

    res = es.search ( index=keyword.lower () + "restaurant" , body={"aggs": {
        "group_by_cuisine": {
            "terms": {
                "field": "cuisine.keyword"
            }
        }
    }} , request_timeout=300 , size="10000" )
    for i in range ( 0 , len ( res["aggregations"]["group_by_cuisine"]["buckets"] ) ):
        cuisine.append ( res["aggregations"]["group_by_cuisine"]["buckets"][i]["key"] )
        valc.append ( res["aggregations"]["group_by_cuisine"]["buckets"][i]["doc_count"] )

    res = es.search ( index=keyword.lower () + "attraction" , body={"query": {"match_all": {}} , "sort": [
        {"note.keyword": {"order": "desc"}}
    ]}
                      , request_timeout=300 , size="10000" )

    for i in range ( 0 , 5 ):
        topa.append ( res['hits']['hits'][i]["_source"]["name"] )
        valuesa.append ( res['hits']['hits'][i]["_source"]["note"].replace ( "," , "." ) )

    res = es.search ( index=keyword.lower () + "attraction" , body={"aggs": {
        "group_by_type": {
            "terms": {
                "field": "type.keyword"
            }
        }
    }} , request_timeout=300 , size="10000" )
    for i in range ( 0 , len ( res["aggregations"]["group_by_type"]["buckets"] ) ):

            type.append ( res["aggregations"]["group_by_type"]["buckets"][i]["key"].replace ( "_" , " " ) )
            valT.append ( res["aggregations"]["group_by_type"]["buckets"][i]["doc_count"] )

    res = es.search ( index=keyword.lower () + "attraction" , body={"aggs": {
        "group_by_durée": {
            "terms": {
                "field": "durée.keyword"
            }
        }
    }} , request_timeout=300 , size="10000" )
    for i in range ( 0 , len ( res["aggregations"]["group_by_durée"]["buckets"] ) ):
        duree.append ( res["aggregations"]["group_by_durée"]["buckets"][i]["key"].replace("_"," ") )
        vald.append ( res["aggregations"]["group_by_durée"]["buckets"][i]["doc_count"] )

    table = Hotel.objects ()
    categories = []

    if len ( table ) != 0:
        for i in range ( 0 , len ( table ) ):
          if exist(table[i].villeHotel.lower() ) :
            categories.append ( table[i].villeHotel )

    print(categories)
    context = {
        'categories':categories,
        'categorie': categorie ,
        'tab': tab ,
        'keyword': keyword ,
        'nums': nums ,
        'labels': labels ,
        'showKeywordbord': 'oui',
        'top':top ,
        'values': values,
        'etoiles' : etoiles,
        'valuese':valuese,
        'places': places ,
        'valuesp': valuesp,
        'topr':topr,
        'valuesr':valuesr,
        'repas': repas ,
        'valr': valr ,
        'cuisine': cuisine ,
        'valc': valc ,
        'topa': topa ,
        'valuesa': valuesa ,
        'type': type ,
        'valT': valT ,
        'duree': duree ,
        'vald': vald ,
    }
    return render ( request , 'admin.html' , context=context )

  if categorie == "manageMagasin" :

      table = Product.objects.filter ( categorie=keyword )
      if len ( table ) == 0:
          return render ( request , '404.html' )

      top = []
      values = []
      categories1 = []
      valc = []
      priceH = []
      valH = []
      priceC = []
      valC = []
      promotion =[]
      valp =[]

      es = Elasticsearch ( [{'host': 'localhost' , 'port': 9200}] )

      res = es.search ( index=keyword.lower ()  , body={"query": {"match_all": {}} , "sort": [
          {"note": {"order": "desc"}}
      ]}
                        , request_timeout=300 , size="10000" )

      for i in range ( 0 , 5 ):
          top.append ( res['hits']['hits'][i]["_source"]["name"] )
          values.append ( res['hits']['hits'][i]["_source"]["note"])

      res = es.search ( index=keyword.lower () , body={"query": {"match_all": {}} , "sort": [
          {"price": {"order": "desc"}}
      ]}
                        , request_timeout=300 , size="10000" )

      for i in range ( 0 , 5 ):
          priceH.append ( res['hits']['hits'][i]["_source"]["name"][0:int(3*(len(res['hits']['hits'][i]["_source"]["name"]))/4)]+"..." )
          valH.append ( str(res['hits']['hits'][i]["_source"]["price"]).replace ( "," , "." ) )

      res = es.search ( index=keyword.lower () , body={"query": {"match_all": {}} , "sort": [
          {"price": {"order": "asc"}}
      ]}
                        , request_timeout=300 , size="10000" )

      for i in range ( 0 , 5 ):
          priceC.append ( res['hits']['hits'][i]["_source"]["name"] )
          valC.append ( str(res['hits']['hits'][i]["_source"]["price"]).replace ( "," , "." ) )

      res = es.search ( index=keyword.lower ()  , body={"aggs": {
          "group_by_subCategorie": {
              "terms": {
                  "field": "subCategorie.keyword"
              }
          }
      }} , request_timeout=300 , size="10000" )
      for i in range ( 0 , len ( res["aggregations"]["group_by_subCategorie"]["buckets"] ) ): 
              categories1.append ( res["aggregations"]["group_by_subCategorie"]["buckets"][i]["key"].replace ( "_" , " " ) )
              valc.append ( res["aggregations"]["group_by_subCategorie"]["buckets"][i]["doc_count"] )

      res = es.search ( index=keyword.lower () , body={"query": {"match_all": {}} , "sort": [
          {"promotion": {"order": "desc"}}
      ]}
                        , request_timeout=300 , size="10000" )

      for i in range ( 0 , 5 ):
          promotion.append ( res['hits']['hits'][i]["_source"]["name"])
          valp.append ( res['hits']['hits'][i]["_source"]["promotion"] )

      table = Product.objects ()
      categories = []

      if len ( table ) != 0:
          for i in range ( 0 , len ( table ) ):
              categories.append ( table[i].categorie )

      context = {
          'categories':categories ,
          'categorie': categorie ,
          'tab': tab ,
          'keyword': keyword ,
          'showKeywordbord': 'oui' ,
          'top': top ,
          'values': values ,
          'categories1' :  categories1,
          "valc" : valc,
          "priceH" : priceH,
          "valH" :valH,
          "priceC" : priceC,
          "valC" :valC,
          "promotion" :promotion ,
           "valp" : valp

      }
      return render ( request , 'admin.html' , context=context )

      

      
      
      
      
   










