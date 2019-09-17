from datetime import datetime
import requests
from bs4 import BeautifulSoup

import time

def getIndice ( liste , element ):
    print ( element );
    for i in range ( 0 , len ( liste ) ):

        if liste[i] == element:
            print ( i );
            return i;


def extractProduct(  categorie ):

    indice = 0
    images_product1 = []
    names_product = []
    promptions_product = []
    details_product = []
    pasDetails = []
    pasPromotion = []
    sub_categorie = []
    prices_product = []
    lien=[]
    imageP=[]
    note=[]
    try:
     for i in range ( 1 , 2 ):

        base_url = "https://www.jumia.com.tn/" + categorie + "/?page=" + str ( i )
        print ( " page url : " + base_url )
        response = requests.get ( base_url )
        print(response)
        soup = BeautifulSoup ( response.content , "lxml" )

        products_name = soup.findAll ( 'span' , attrs={"class": u"name"} )
        print(len(products_name ))
        for product_name in products_name:
            names_product.append ( product_name.text )



        products_promotion = soup.findAll ( 'span' , attrs={"class": u"sale-flag-percent"} )
        for product_promotion in products_promotion:
            promptions_product.append ( product_promotion.text )

        details = 0
        products_details = soup.findAll ( 'a' , attrs={"class": u"link"} )
        for product_details in products_details:
            print ( "product :  " + product_details.get ( "href" ) )
            images_product = []
            if (indice >= 1 and indice != 40 and details == 0):
                pasDetails.append ( indice - 1 )
            details = 0
            lien.append(product_details.get ( "href" ) )
            response1 = requests.get ( product_details.get ( "href" ) )
            soup1 = BeautifulSoup ( response1.content , "html5lib" )
            product_images = soup1.findAll ( 'img' , attrs={"class": "lazy"} )
            imageP.append(product_images[0].get ( "data-src" ))

            for product_img in product_images:
                images_product.append ( product_img.get ( "data-src" ) )

            images_product1.append ( images_product )
            products_price = soup1.find ( 'span' , attrs={"class": "price"} )
            if  products_price == None:
                products_price = soup1.find ( 'span' , attrs={"class": "price -no-special"} )
            prices_product.append ( products_price.text )
            print (  products_price.text )
            sub_categorieParent = soup1.findAll ( 'li' , attrs={"class": ""} )
            productPromotion = soup1.findAll ( 'span' , attrs={"class": u"sale-flag-percent"} )
            if (productPromotion == []):
                pasPromotion.append ( indice )

            sub_categorie.append ( sub_categorieParent[2].text )
            print ( "sub cateogorie: " + sub_categorieParent[2].text )
            étoile = soup1.find ( 'div' , attrs={"class": "container"} )
            note.append(étoile.text)
            product_detail1 = soup1.findAll ( 'ul' )
            for prod_detail1 in product_detail1:
                if prod_detail1.get ( "class" ) == None and str ( prod_detail1.contents ).find ( "<a" ) == -1 and str (
                        prod_detail1.contents ).find ( "<span" ) == -1 and str ( prod_detail1.parent ).find (
                        "Voir détails" ) != -1:
                    details_product.append ( prod_detail1.text )
                    details = details + 1
                    print ( details )
            indice = indice + 1
            print ( "*******************************************" )
            print ( "\n" )
        if (details == 0):
            pasDetails.append ( indice - 1 )
    except  Exception  as e:
            print ( "an error occured"+ str(e) )

    finally:
     if len(names_product )==0:
         return []
     CategorieArray = []
     for i in range ( 0 , len ( names_product ) ):
        CategorieProduct = {}
        CategorieProduct["name"] = names_product[i].replace("/","*")
        CategorieProduct["note"] = float(note[i].replace(" ","").replace(",","."))
        CategorieProduct["url"] = lien[i]
        CategorieProduct["image"] = images_product1[i]
        CategorieProduct["imageP"] = imageP[i]
        CategorieProduct["subCategorie"] = sub_categorie[i].replace(" ","_")
        if  (prices_product[i].replace(" TND ","").replace(" ","")).find("-")==-1:
         CategorieProduct["price"] =  int(prices_product[i].replace(" TND ","").replace(" ",""))
        CategorieArray.append ( CategorieProduct )

     j = 0;
     for i in range ( 0 , len ( CategorieArray ) ):
        CategorieProduct = CategorieArray[i]
        if (not i in pasPromotion):
            CategorieProduct["promotion"] = int(promptions_product[j].replace("-","").replace("%",""))
            CategorieArray[i] = CategorieProduct
            j = j + 1;
     j = 0;
     print ( len ( details_product ) )
     for i in range ( 0 , len ( CategorieArray ) ):
        CategorieProduct = CategorieArray[i]
        if (not i in pasDetails):
            CategorieProduct["details"] = details_product[j]
            CategorieArray[i] = CategorieProduct
            j = j + 1;


     return CategorieArray


def extractHotel( ville ):
    print ( "ville: " + ville )
    indice = 0
    j1 = 0
    nbHotels = 0
    hotel_photos = []
    names_ville = []
    lieu_ville = []
    notes = []
    mentions = []
    points = []
    etoiles = []
    details = []
    pasEtoiles = []
    pasNote = []
    Resto_à_proximité = []
    interet = []
    proche = []
    aeo=[]
    appartement = []
    hebergement = []
    Hotelsproches = []
    aeoportProches = []
    lieuxInteretProches = []
    lien=[]
    imageP=[]
    restaurent_Marche_proches = []
    try:
     for i in range ( 0 , 30, 15 ):
        base_url = "https://www.booking.com/searchresults.fr.html?tmpl=searchresults&ss=" + ville + "&nflt=ht_id%3D204%3B&rows=15&offset=" + str (
            i ) + "&ss_all=0&ac_langcode=fr&percent_htype_apt=1&percent_htype_hotel=1&shw_aparth=1&rsf="

        print ( " page url : " + base_url )

        response = requests.get ( base_url )
        soup = BeautifulSoup ( response.content , "lxml" )

        ville_hotels = soup.findAll ( 'td' , {"class": "sr_item_legacy_review"} )

        for ville_hotel in ville_hotels:

            if str ( ville_hotel.contents ).find ( "bui-review-score__badge" ) != -1:
                pasNote.append ( j1 )

            j1 = j1 + 1

        villes_name = soup.findAll ( 'span' , attrs={"class": "sr-hotel__name"} )
        for ville_name in villes_name:
            names_ville.append ( ville_name.text )

        hotel_notes = soup.findAll ( 'div' , attrs={"class": "bui-review-score__badge"} )
        for hotel_note in hotel_notes:
            notes.append ( hotel_note.text )
        hotel_mentions = soup.findAll ( 'div' , attrs={"class": "bui-review-score__title"} )

        for hotel_mention in hotel_mentions:
            mentions.append ( hotel_mention.text )

        hotel_links = soup.findAll ( 'a' , attrs={"class": "hotel_name_link url"} )

        for link in hotel_links:
            x = 0
            indice = link.get ( "href" ).find ( "html" )
            url = link.get ( "href" )[:indice + 4]

            base_url1 = "https://www.booking.com" + url.replace ( "\n" , "" )
            print ( base_url1 )
            lien.append( base_url1)
            response1 = requests.get ( base_url1 )
            soup1 = BeautifulSoup ( response1.content , "html5lib" )

            # print(soup1)
            villes_lieu = soup1.findAll ( 'p' , attrs={"class": "address_clean"} )
            lieu_ville.append ( villes_lieu[0].contents[5].text )
            hotel_point = soup1.findAll ( 'div' , attrs={"class": "hp_desc_important_facilities clearfix"} )

            points.append ( hotel_point[0].text.replace ( "Ses points forts" , "" ) )

            images_ville = []
            Hotels__images = soup1.findAll('div',
                                           attrs={"class": "b_nha_hotel_small_images hp_thumbgallery_with_counter"})
            i = 0

            if len ( Hotels__images ) != 0:
                for i in range ( 0 , len ( Hotels__images[0].contents ) ):
                    if Hotels__images[0].contents[i].name == "a" and Hotels__images[0].contents[i].get ( "href" ).find (
                            "http" ) != -1:
                        images_ville.append ( Hotels__images[0].contents[i].get ( "href" ) )

                hotel_photos.append ( images_ville )
                print ( len ( images_ville ) )
                imageP.append ( images_ville[0] )
                Hotels_raisons_reservation = soup1.findAll ( 'div' , attrs={"class": "content-wrapper clearfix"} )
                hebergement.append ( Hotels_raisons_reservation[0].text.replace("\n\n\n\n\n\n\n\n\n"," ").replace("\n\n\n\n\n\n\n\n","\n").replace("\n\n\n\n\n\n\n"," ").replace("Pourquoi réserver sur notre site","") )
            else:
                Hotels__images = soup1.findAll ( 'a' , attrs={"class": "bh-photo-grid-item bh-photo-grid-thumb"} )

                i = 0

                for i in range ( 0 , len ( Hotels__images ) ):
                    if Hotels__images[i].name == "a" and Hotels__images[i].get ( "href" ).find ( "http" ) != -1:
                        images_ville.append ( Hotels__images[i].get ( "href" ) )
                        appartement.append ( nbHotels )



                imageP.append ( images_ville[0] )
                hotel_photos.append ( images_ville )
                print(len( hotel_photos))
                Hotels_raisons_reservation = soup1.findAll ( 'div' , attrs={ "class": "hops__personalised-description js-host-info__description"} )
                if len ( Hotels_raisons_reservation ) == 0:
                    hebergement.append ( "pas d'informations sur l'hote" )
                else:
                    hebergement.append ( Hotels_raisons_reservation[0].text )

            Hotels_proches = soup1.findAll ( 'ul' , attrs={"class": "bui-list bui-list--text hp-poi-list__wrapper"} )
            i = 0
            for i in range ( 0 , len ( Hotels_proches ) ):
                if Hotels_proches[i].previous_element.previous_element.find ( "Les plus proches" ) != -1:
                    Hotelsproches.append ( Hotels_proches[i].text.replace("\n\n\n\n\n\n","\n").replace("\n\n","      ")  )
                    proche.append(nbHotels)
                if Hotels_proches[i].previous_element.previous_element.find (
                        "Lieux d'intérêt les plus populaires" ) != -1:
                    lieuxInteretProches.append ( Hotels_proches[i].text .replace("\n\n\n\n\n\n","\n").replace("\n\n","      ") )
                    interet.append(nbHotels)

                if Hotels_proches[i].previous_element.previous_element.find ( "Aéroports les plus proches" ) != -1:
                    aeoportProches.append ( Hotels_proches[i].text.replace("\n\n\n\n\n\n","\n").replace("\n\n\n","  ") )
                    aeo.append( nbHotels)

                if Hotels_proches[i].previous_element.previous_element.find ( "Restaurants et marchés" ) != -1:
                    restaurent_Marche_proches.append ( Hotels_proches[i].text.replace("\n\n\n\n\n\n\n\n","\n").replace("\n\n\n\n","         ").replace("\n\n\n","         ")   )
                    Resto_à_proximité.append ( nbHotels )

            i = 0
            Hotels_aeo_proches = soup1.findAll ( 'ul' ,
                                                 attrs={"class": "bui-list bui-list--text add hp-poi-list__wrapper"} )
            for i in range ( 0 , len ( Hotels_aeo_proches ) ):
                if Hotels_aeo_proches[i].previous_element.previous_element.find ( "Les plus proches" ) != -1:
                    Hotelsproches.append (Hotels_aeo_proches[i].text.replace("\n\n\n\n\n\n","\n").replace("\n\n","      ") )
                    proche.append ( nbHotels )
                if Hotels_aeo_proches[i].previous_element.previous_element.find (
                        "Lieux d'intérêt les plus populaires" ) != -1:
                    lieuxInteretProches.append (Hotels_aeo_proches[i].text.replace("\n\n\n\n\n\n","\n").replace("\n\n","      ") )
                    interet.append ( nbHotels )
                if Hotels_aeo_proches[i].previous_element.previous_element.find ( "Aéroports les plus proches" ) != -1:
                    aeoportProches.append ( Hotels_aeo_proches[i].text.replace("\n\n\n\n\n\n","\n").replace("\n\n\n","      ")  )
                    aeo.append ( nbHotels )
                if Hotels_aeo_proches[i].previous_element.previous_element.find ( "Restaurants et marchés" ) != -1:
                    restaurent_Marche_proches.append ( Hotels_aeo_proches[i].text.replace("\n\n\n\n\n\n\n\n","\n").replace("\n\n\n\n","        ").replace("\n\n\n","        ") )
                    Resto_à_proximité.append ( nbHotels )

            hotel_details = soup1.find ( 'div' , attrs={"class": "hp_desc_main_content"} )
            details.append ( hotel_details.text )
            étoileH = "non classé"
            étoiles = soup1.findAll ( 'span' , attrs={"class": "invisible_spoken"} )
            for étoile in étoiles:
                if str (étoile.parent.get ( "class" ) ) == "['bk-icon-wrapper', 'bk-icon-stars', 'star_track']":
                    étoileH = étoile.text
                    break
            etoiles.append( étoileH )
            indice = indice + 1
            nbHotels = nbHotels + 1
    except  Exception as e:
        print("an error occured"+str(e))
    finally:

     HotlesArray = []
     if len(names_ville) ==0:
         return []

     for i in range ( 0 , len ( names_ville ) ):
        Hotel = {}
        Hotel["name"] = names_ville[i]
        Hotel["url"]=lien[i]
        Hotel["image"] = hotel_photos[i]
        Hotel["imageP"]=imageP[i]
        Hotel["place"] = lieu_ville[i].replace(" ","_").replace("'","__").replace("\n","_")
        Hotel["point"] = points[i]
        Hotel["details"] = details[i].replace(" ","_").replace("'","__")
        Hotel["étoile"] = etoiles[i]
        HotlesArray.append ( Hotel )


        if (i in appartement):
            Hotel["type"] = "Appartements"
            Hotel["hote"] = hebergement[i]
        else:
            Hotel["type"] = "Hôtels"
            Hotel["réservation"] = hebergement[i]

     j = 0
     for i in range ( 0 , len ( HotlesArray ) ):
        Hotel = HotlesArray[i]
        if (i in pasNote):
            Hotel["note"] = notes[j]
            Hotel["mention"] = mentions[j].replace("Très bien ","Très_bien ")
            HotlesArray[i] = Hotel
            j = j + 1;

     j = 0;
     for i in range ( 0 , len ( HotlesArray ) ):
        Hotel = HotlesArray[i]
        if (i in Resto_à_proximité):
            Hotel["Restaurants"] = restaurent_Marche_proches[j]
            HotlesArray[i] = Hotel
            j = j + 1;

     j = 0;
     for i in range ( 0 , len ( HotlesArray ) ):
         Hotel = HotlesArray[i]
         if (i in proche):
             Hotel["proches"] = Hotelsproches[i]
             HotlesArray[i] = Hotel
             j = j + 1;

     j = 0;
     for i in range ( 0 , len ( HotlesArray ) ):
         Hotel = HotlesArray[i]
         if (i in interet):
             Hotel["intérêt"] = lieuxInteretProches[i]
             HotlesArray[i] = Hotel
             j = j + 1;

     j = 0;
     for i in range ( 0 , len ( HotlesArray ) ):
         Hotel = HotlesArray[i]
         if (i in aeo):
             Hotel["Aéroports"] = aeoportProches[i]
             HotlesArray[i] = Hotel
             j = j + 1;

     return (HotlesArray)




def extractAttractions( ville ):
    print ( "ville: " + ville )
    indice = 0
    j1 = 0
    type=[]
    images_attractions = []
    names_ville = []
    notes = []
    details = []
    adresse = []
    pasDetails = []
    yimage = []
    phone = []
    yphone = []
    horaire = []
    yhoraire = []
    duree = []
    yduree = []
    prix = []
    yprix = []
    lien=[]
    imageP=[]
    base_url = "https://www.google.tn/search?hl=fr-TN&authuser=0&ei=KjchXIa2NIfSkgWc1rHgDg&q=" + ville + "+activités+oa30+tripadvisor&oq=" + ville + "++activités+tripadvisor"
    try:
     response = requests.get ( base_url )
     soup = BeautifulSoup ( response.content , "lxml" )

     url_attractions = soup.findAll ( 'div' , attrs={"class": "kCrYT"} )

     for url in url_attractions:
        print(url)
        if url.contents[0].get ( "href" ).find ( "tripadvisor.fr" ) != -1 and url.contents[0].get ( "href" ).find (
                "Attractions-g" ) != -1:
            child = url.contents[0].get ( "href" )
            debut = url.contents[0].get ( "href" ).find ( "-c" )
            fin = url.contents[0].get ( "href" ).find ( "-o" )
            child = child.replace ( child[debut:fin] , "" )

            break;

     debut = child.find ( "http" )
     fin = child.find ( "html" )
     url1 = child[debut:fin + 4]
     print(url1)
     for i in range ( 30 , 60 , 30 ):

        if i == 60:
            url1 = url1.replace ( "oa30" , "oa60" )

        response1 = requests.get ( url1 )
        print ( url1 )
        soup1 = BeautifulSoup ( response1.content , "lxml" )
        villes_name = soup1.findAll ( 'div' , attrs={"class": "tracking_attraction_title listing_title"} )

        while str ( villes_name[0].contents[1].get ( "href" ) ).find ( "Attraction_Review" ) == -1:
            response1 = requests.get ( url1 )
            soup1 = BeautifulSoup ( response1.content , "lxml" )
            villes_name = soup1.findAll ( 'div' , attrs={"class": "tracking_attraction_title listing_title "} )

        attraction_type = soup1.findAll ( 'span' , attrs={"class": "matchedTag noTagImg"} )
        print(len(attraction_type ))
        for i in range ( 0 , len ( attraction_type ) ):
            type.append(attraction_type[i].text)

        attractions_prix = soup1.findAll ( 'div' , attrs={"class": "attraction_clarity_cell"} )
        indice1 = 0
        for i in range ( 0 , len ( attractions_prix ) ):
            if attractions_prix[i].text.find ( "Expériences à partir de" ) != -1:
                debut = attractions_prix[i].text.find ( "Expériences" )
                fin = attractions_prix[i].text.find ( "TND" )
                print ( attractions_prix[i].text[debut:fin + 3] )
                prix.append ( attractions_prix[i].text[debut:fin + 3] )
                yprix.append ( indice1 )
                print ( indice1 )
            indice1 = indice1 + 1

        for ville_name in villes_name:
            images_ville = []
            names_ville.append ( ville_name.contents[1].text )
            base_url1 = "https://www.tripadvisor.fr" + ville_name.contents[1].get ( "href" )
            print ( base_url1 )
            lien.append(base_url1 )
            response2 = requests.get ( base_url1 )
            soup2 = BeautifulSoup ( response2.content , "html5lib" )
            attractions_images = soup2.findAll ( 'img' , attrs={"class": "basicImg"} )
            x=0
            if len ( attractions_images ) != 0:

                for i1 in range ( 0 , len ( attractions_images ) ):
                    if attractions_images[i1].get ( "data-lazyurl" ).find ( "http" ) != -1:

                        images_ville.append ( attractions_images[i1].get ( "data-lazyurl" ) )
                        if x==0:
                            imageP.append(attractions_images[i1].get ( "data-lazyurl" ) )
                            i=i+1

                images_attractions.append ( images_ville )
                yimage.append ( j1 )

            attractions_notes = soup2.findAll ( 'span' , attrs={"class": "overallRating"} )
            notes.append ( attractions_notes[0].text )

            attractions_phone = soup2.findAll ( 'div' , attrs={"class": "detail_section phone"} )
            if len ( attractions_phone ):
                phone.append ( attractions_phone[0].text )
                yphone.append ( indice )
            attractions_horaire = soup2.findAll ( 'div' , attrs={
                "class": "attractions-attraction-detail-about-card-AboutSection__sectionWrapper--3PMQg"} )
            if len ( attractions_horaire ) != 0:
                i = 0
                for i in range ( 0 , len ( attractions_horaire ) ):
                    if attractions_horaire[i].text.find ( "horaire" ) != -1 and (
                            attractions_horaire[i].text.find ( "Ouvert" ) != -1 or attractions_horaire[i].text.find (
                            "Fermé à l'heure actuelle" ) != -1):
                        horaire.append ( attractions_horaire[i].text.replace ( "Voir tous les horaires" , "" ).replace (
                            "Fermé à l'heure actuelle" , "" ).replace ( "Ouvert" , "" ) )
                        yhoraire.append ( indice )
                    if attractions_horaire[i].text.find ( "Durée" ) != -1:
                        duree.append ( attractions_horaire[i].text )
                        yduree.append ( indice )
            attractions_infos = soup2.findAll ( 'div' , attrs={
                "class": "attractions-attraction-detail-about-card-AboutSection__sectionWrapper--3vxlo"} )
            if len ( attractions_infos ) != 0:
                if len ( attractions_infos[0].contents ) >= 3:
                    details.append ( attractions_infos[0].contents[2].text.replace ( "Fermé à l'heure actuelle" , "" ) )
                    pasDetails.append ( indice )

            attractions_adress = soup2.findAll ( 'span' , attrs={"class": "street-address"} )
            attractions_adress1 = soup2.findAll ( 'span' , attrs={"class": "locality"} )
            attractions_adress2 = soup2.findAll ( 'span' , attrs={"class": "country-name"} )
            if len(  attractions_adress )!= 0:
             print( attractions_adress[0].text + "," + attractions_adress1[0].text  + attractions_adress2[0].text )
             adresse.append ( attractions_adress[0].text + "," + attractions_adress1[0].text + attractions_adress2[0].text  )

            else:
                print ( attractions_adress1[0].text + attractions_adress2[0].text )
                adresse.append ( attractions_adress1[0].text + attractions_adress2[0].text )
            indice = indice + 1
            j1 = j1 + 1

    except  requests.ConnectionError as e:
       print ( "an error occured" )

    finally:


      AttractionsArray = []
      for i in range ( 0 , len ( names_ville ) ):
        Attraction = {}
        Attraction["name"] = names_ville[i]
        Attraction["url"]=lien[i]

        Attraction["place"] = adresse[i].replace(" ","_").replace(",_","_").replace(",","_").replace("__",'_').replace("'","__")
        Attraction["note"] = notes[i]
        Attraction["type"]=type[i].replace(" ","_").replace("'","__")
        AttractionsArray.append ( Attraction )

      j = 0
      for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yimage):
            Attraction["image"] = images_attractions[j]
            Attraction["imageP"] = imageP[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

      j = 0
      for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yphone):
            Attraction["téléphone"] = phone[j]
            AttractionsArray[i] = Attraction
            j = j + 1;
      j = 0
      for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yhoraire):
            Attraction["horaire"] = horaire[j]
            AttractionsArray[i] = Attraction
            j = j + 1;
      j = 0
      for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yduree):
            Attraction["durée"] = duree[j].replace(" ","_").replace("Durée_conseillée :","").replace("'","_")
            AttractionsArray[i] = Attraction
            j = j + 1;


      return AttractionsArray


def findPrice ( price ):
    if price.parent.parent.parent.name != 'li' and price.parent.parent.parent.name != 'ul':
        return True;
    return False;



def extractBien( ville , vente , bien ):
    print ( "ville: " + ville )
    indice = 0
    images = []
    names_ville = []
    option = []
    price = []
    annonceur = []
    description = []
    details = []
    adresse = []
    pasDetails = []
    pasimage = []
    pasoption = []
    pasdescription = []
    pasprice = []
    pasannonceur = []
    lien=[]
    adr=[]
    imageP=[]
    try:
     for i in range ( 1 , 4 ):
        base_url = "https://www.menzili.tn/immo/" + bien + "-" + vente + "-" + ville + "?page=" + str ( i )

        response = requests.get ( base_url )
        soup = BeautifulSoup ( response.content , "lxml" )
        print ( base_url )
        villes_name = soup.findAll ( 'a' , attrs={"class": "li-item-list-title"} )
        adresses = soup.findAll ( 'div' , attrs={"class": "col-md-7 col-sm-7 col-xs-12 li-item-list-other"} )
        print(len(adresses))
        for i in range(0, len(adresses)):
            adr.append ( adresses[i].contents[3].text )

        for i in range (2, len(villes_name)):

            names_ville.append ( villes_name[i].text )
            response2 = requests.get ( villes_name[i].get ( "href" ) )
            soup2 = BeautifulSoup ( response2.content , "html5lib" )
            lien.append(villes_name[i].get ( "href" ) )
            bien_adresse = soup2.findAll ( 'div' , attrs={"class": "col-md-8 col-xs-12 col-sm-7 product-title-h1"} )
            adresse.append ( bien_adresse[0].text.replace ( villes_name[i].text , "" ) )

            bien_price = soup2.findAll ( 'div' , attrs={"class": "col-md-4 col-xs-12 col-sm-5 product-price"} )
            if len ( bien_price ) != 0:
                pasprice.append ( indice )
                price.append ( bien_price[0].text )
            bien_description = soup2.findAll ( 'div' , attrs={"class": "col-md-12 col-xs-12 col-sm-12 block-descr"} )

            if len ( bien_description ) != 0:
                pasdescription.append ( indice )
                description.append ( bien_description[0].text.replace ( "Description" , "" ) )

            bien_details = soup2.findAll ( 'div' , attrs={"class": "col-md-12 col-xs-12 col-sm-12 block-detail "} )
            if len ( bien_details ) != 0:
                pasDetails.append ( indice )
                details.append ( bien_details[0].text.replace ( "Détails de bien" , "" ) )

            bien_annoceur = soup2.findAll ( 'span' , attrs={"class": " btn col-md-12 col-xs-12 col-sm-12"} )
            if len ( bien_annoceur ) != 0:
                pasannonceur.append ( indice )
                annonceur.append ( bien_annoceur[0].text )

            bien_option = soup2.findAll ( 'div' , attrs={"class": "col-md-12 col-xs-12 col-sm-12 block-over"} )
            if len ( bien_option ) != 0:
                pasoption.append ( indice )
                option.append ( bien_option[0].text )

            Array = []
            bien_images = soup2.findAll ( 'a' , attrs={"class": "thumbs"} )
            if len ( bien_images ) != 0:
                pasimage.append ( indice )
                for bien_image in bien_images:
                    image = bien_image.contents[1].get ( "src" )
                    Array.append ( image )
                images.append ( Array )
                imageP.append(Array[0])
            indice = indice + 1
    except  Exception as e:
        print ( "an error occured" )
    finally:
     AttractionsArray = []
     print(len( names_ville))
     print(len(adr))
     for i in range ( 0 , len ( names_ville ) ):
        Attraction = {}
        Attraction["name"] = names_ville[i]
        Attraction["lien"]=lien[i]
        Attraction["place"] = adr[i]

        AttractionsArray.append ( Attraction )
     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in pasDetails):
            Attraction['details'] = details[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in pasdescription):
            Attraction['description'] = description[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in pasprice):
            Attraction['price'] = price[j]
            AttractionsArray[i] = Attraction
            j = j + 1;
     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in pasoption):
            Attraction['option'] = option[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in pasimage):
            Attraction['image'] = images[j]
            Attraction["imageP"] = imageP[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in pasannonceur):
            Attraction["annonceur"] = annonceur[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     return AttractionsArray

def get_url ( url , ville ):
    names_ville = []
    images_ville = []
    notes = []
    adresse = []
    specialite = []
    repas = []
    prix = []
    regime = []
    yprix = []
    yregime = []
    yrepas = []
    indice = 0
    images_attractions = []
    yimage = []
    yspecialite = []
    phone = []
    yphone = []
    AttractionsArray=[]
    lien=[]
    imageP=[]
    try:
     for i in range ( 30 , 60 , 30 ):
        print ( i )
        url.replace(" ","_")
        print(url)
        if i >= 60:
            url = url.replace ( "oa"+str(i-30) , "oa"+str(i) )
        if  i<60:
            url = url.replace ( ville  , "oa30-"+ville  )

        response1 = requests.get ( url )
        soup1 = BeautifulSoup ( response1.content , "lxml" )
        print(url)
        print("****************************************************")
        villes_name = soup1.findAll ( 'a' , attrs={"class": "restaurants-list-ListCell__restaurantName--2aSdo"} )

        if len(villes_name)==0:
          villes_name = soup1.findAll ( 'a' , attrs={"class": "property_title"})

        print ( str ( len ( villes_name ) ) + 'hotels' )
        attractions_images = soup1.findAll ( 'img' , attrs={"class": "photo_image"} )
        for ville_image in attractions_images:
            images_ville.append ( ville_image.get ( "src" ) )
        for ville_name in villes_name:
            images_ville = []
            if ville_name.get ( "data-url" ) == None:
                print ( "https://www.tripadvisor.fr/" + ville_name.get ( "href" ) )
                lien.append ( "https://www.tripadvisor.fr/" + ville_name.get ( "href" ) )
                response2 = requests.get ( "https://www.tripadvisor.fr/" + ville_name.get ( "href" ) )
            else:
                print ( ville_name.get ( "data-url" ) )
                lien.append ( ville_name.get ( "data-url" ) )
                response2 = requests.get ( ville_name.get ( "data-url" ) )

            soup2 = BeautifulSoup ( response2.content , "lxml" )
            name = soup2.findAll ( 'h1' , attrs={ "class": "ui_header"} )
            names_ville.append (name[0].text )
            attractions_notes = soup2.findAll ( 'span' , attrs={
                "class": "restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl"} )
            if len ( attractions_notes ) == 0:
                attractions_notes = soup2.findAll ( 'span' , attrs={
                    "class": "restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl"} )

            if len ( attractions_notes ) == 0:
                attractions_notes = soup2.findAll ( 'span' , attrs={
                    "class": "restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--r2Cf6"} )
            notes.append ( attractions_notes[0].text )
            attractions_adress = soup2.findAll ( 'span' , attrs={"class": "street-address"} )
            attractions_adress1 = soup2.findAll ( 'span' , attrs={"class": "locality"} )
            attractions_adress2 = soup2.findAll ( 'span' , attrs={"class": "country-name"} )
            if len ( attractions_adress ) != 0:
                print ( attractions_adress[0].text + "," + attractions_adress1[0].text + attractions_adress2[0].text )
                adresse.append (
                    attractions_adress[0].text + "," + attractions_adress1[0].text + attractions_adress2[0].text )

            else:
                print ( attractions_adress1[0].text + attractions_adress2[0].text )
                adresse.append ( attractions_adress1[0].text + attractions_adress2[0].text )
            attractions_infos = soup2.findAll ( 'div' , attrs={
                "class": "restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"} )
            i = 0
            for i in range ( 0 , len ( attractions_infos ) ):
                if attractions_infos[i].previous_element.find ( "FOURCHETTE DE PRIX" ) != -1:
                    prix.append ( attractions_infos[i].text )
                    yprix.append ( indice )

                if attractions_infos[i].previous_element.find ( "CUISINES" ) != -1:
                    specialite.append ( attractions_infos[i].text )
                    yspecialite.append ( indice )

                if attractions_infos[i].previous_element.find ( "Repas" ) != -1:
                    repas.append ( attractions_infos[i].text )
                    yrepas.append ( indice )

                if attractions_infos[i].previous_element.find ( "Régimes spéciaux" ) != -1:
                    regime.append ( attractions_infos[i].text )
                    yregime.append ( indice )

            attractions_images = soup2.findAll ( 'img' , attrs={"class": "basicImg"} )
            if len ( attractions_images ) != 0:
                i1 = 0
                for i1 in range ( 0 , len ( attractions_images ) ):
                    if attractions_images[i1].get ( "data-lazyurl" ).find ( "http" ) != -1:
                        images_ville.append ( attractions_images[i1].get ( "data-lazyurl" ) )
                images_attractions.append ( images_ville )
                imageP.append(images_ville[0])
                yimage.append ( indice )
            print ( "****************" )

            attractions_phone = soup2.findAll ( 'div' , attrs={
                "class": "restaurants-detail-overview-cards-LocationOverviewCard__detailLink--iyzJI"} )
            if len ( attractions_phone ) != 0:
                phone.append ( attractions_phone[len ( attractions_phone ) - 1].contents[0].get ( "href" ) )
                yphone.append ( indice )

            indice = indice + 1
    except  requests.ConnectionError as e:
        print ( "an error occured" )
    finally:


     for i in range ( 0 , len ( names_ville ) ):
        Attraction = {}
        Attraction["name"] = names_ville[i]
        Attraction["url"]=lien[i]
        Attraction["note"] = notes[i]
        Attraction["adresse"] = adresse[i].replace(" ","_").replace(",_","_").replace(",","_").replace("__",'_').replace("'","__")

        AttractionsArray.append ( Attraction )

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yprix):
            Attraction["prix"] = prix[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yrepas):
            Attraction["repas"] = repas[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yregime):
            Attraction["Régimes"] = regime[j]
            AttractionsArray[i] = Attraction
            j = j + 1;
     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yspecialite):
            Attraction["cuisine"] = specialite[j]
            AttractionsArray[i] = Attraction
            j = j + 1;
     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yimage):
            Attraction["image"] = images_attractions[j]
            Attraction["imageP"]=imageP[j]
            AttractionsArray[i] = Attraction
            j = j + 1;

     j = 0
     for i in range ( 0 , len ( AttractionsArray ) ):
        Attraction = AttractionsArray[i]
        if (i in yphone):
            Attraction["téléphone"] = phone[j]
            AttractionsArray[i] = Attraction
            j = j + 1;


     return  AttractionsArray


def extractRestaurent ( ville ):
    print ( "ville: " + ville )
    VilleJSON=[]
    try:
     base_url = "https://www.google.tn/search?hl=fr-TN&authuser=0&ei=KjchXIa2NIfSkgWc1rHgDg&q=" + ville + "+restaurants+tripadvisor.fr&oq=" + ville + "+restaurants+tripadvisor.fr"
     response = requests.get ( base_url )

     soup = BeautifulSoup ( response.content , "lxml" )
     url_attractions = soup.findAll ( 'div' , attrs={"class": "kCrYT"} )

     child=""

     for i in range(0,len(url_attractions)):

        if url_attractions[i].contents[0].get ( "href" ).find ( "tripadvisor.fr" ) != -1 and url_attractions[i].contents[0].get ( "href" ).find ("Restaurants-g" ) != -1:
            child = url_attractions[i].contents[0].get ( "href" )

            break



    except  :
      print ( "an error occured"  )

    finally:
     debut = child.find ( "http" )
     fin = child.find ( "html" )
     url1 = child[debut:fin + 4]
     VilleJSON = get_url (  url1 , ville )
     return ( VilleJSON )

