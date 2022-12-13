import os

from datetime import timezone
import datetime


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from geopy import distance
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from helpers import apology, login_required,  usd, company_required, dict_from_row


# Configure  SQLite database
con = sqlite3.connect("socialwork.db")


with con:
    # create dict table
    con.row_factory = sqlite3.Row

cur = con.cursor()  


# cur.execute("Select *, address1 || ', ' || city || ', ' || zipcode address FROM user ")
# users = cur.fetchall()

# geolocator = Nominatim(user_agent="MyApp")

# for row in users:
#     print("test")
#     userid = row["id"]    
#     if geolocator.geocode(row["address"]):
#         location = geolocator.geocode(row["address"])         
#         lat = location.latitude
#         long = location.longitude
#         print(long)       
#         cur.execute("INSERT INTO  geo_location values(NULL, ? ,?, ?)",[ userid, lat, long] )
#         con.commit()
#         con.close

# def geo(userid):      
#     #get the address of the user
#     cur.execute("SELECT id, address1 || ', ' || city || ', ' || zipcode address FROM user WHERE id = ? ",[userid])  
#     user = cur.fetchone()         
#     # get the address geo location
#     geolocator = Nominatim(user_agent="MyApp")
#     if geolocator.geocode(user["address"]):
#         location = geolocator.geocode(user["address"])         
#         lat = location.latitude
#         long = location.longitude

#         # check if the user exists in the user table
#         cur.execute("SELECT userid FROM geo_location where userid = ?",[userid])  
#         geo = cur.fetchone()

#         # insert or update the geo table 
#         if geo == None:
#             cur.execute("INSERT INTO  geo_location values(NULL, ? ,?, ?)",[ userid, lat, long] )
#             con.commit()
#             con.close
#         else:
#             cur.execute("UPDATE geo_location SET latitude = ?, longitude = ? where userid = ?",[lat, long, userid] )
#             con.commit()
#             con.close

# geo(6)
    
from datetime import datetime, timedelta

companyid=34
 
# select the company information
cur.execute("SELECT c.id companyid, c.company, c.image, c.hour_start, c.hour_end,  c.website, u.address1, u.address2, u.city, u.state, u.phone, u.zipcode,  \
    address1 || ', ' || city || ', ' || zipcode address  \
    FROM company c LEFT JOIN user u on c.id = u.companyid where c.typeid = 2 and c.id=?", [companyid])
cafe = cur.fetchone()  

(start_min, start_sec)=cafe["hour_start"].split(":")

(end_min, end_sec)=cafe["hour_end"].split(":")

print(start_min, start_sec, end_min, end_sec)


def datetime_range(start, end, delta):
    current = start
    while current <= end:        
        yield current        
        current += delta          
     

dts = [(str(dt).split(" ",1)[1])[:-3] for dt in 
       datetime_range(datetime(1900, 1, 1,int(start_min),int(start_sec)), datetime(1900, 1, 1, int(end_min), int(end_sec)), 
       timedelta(minutes=15))        
       ]
        










# dts = [dt.strftime('%Y-%m-%d :%H:%M') for dt in 
#        datetime_range(datetime(1900, 1, 1, 9), datetime(1900, 1, 1, 20), 
#        timedelta(minutes=15))        
#        ]


print(dts)






# # get the user address longitude and latitude
# geolocator = Nominatim(user_agent="MyApp")
# cur.execute("SELECT address1 || ', ' || city || ', ' || zipcode as address FROM user WHERE id = 6" )
# user=cur.fetchone()
# location = geolocator.geocode(user["address"])  
# locuser = (location.latitude , location.longitude)

#  # get a list of the vendors 
# cur.execute("SELECT c.id companyid, c.company, c.image, c.hour_start, c.hour_end,  c.website, u.address1, u.address2, u.city, u.state, u.phone, u.zipcode,  \
#     address1 || ', ' || city || ', ' || zipcode address  \
#     FROM company c LEFT JOIN user u on c.id = u.companyid where c.typeid = 2")
# cafes = cur.fetchall()
# cafelist = []

# # get the longitude and latitude of the cafes 
# for cafe in cafes: 
#     location = geolocator.geocode(cafe["address"])  
#     loccafe = (location.latitude , location.longitude)  
#     #find the distence from the user
#     dist = round(geodesic(locuser,loccafe).kilometers,2)     
#     # create dict from row
#     dictcafe = dict_from_row(cafe)
#     # append distence to the dict  
#     dictcafe['distance']  = dist 
#     # append dict to list of rows
#     cafelist.append(dictcafe)    

# # sort the dicts in the list of cafes   
# cafelist = sorted(cafelist, key = lambda i: i['distance'])


7
    
















# geolocator = Nominatim(user_agent="MyApp")
# location = geolocator.geocode("189 Dizengoff St Tel Aviv 60000")
# print(location.address)
# print(location.raw)

# userlat = location.latitude
# userlon = location.longitude

# loc1 = (location.latitude , location.longitude)
# print (loc1)


# location2 = geolocator.geocode("176 dizengoff tel aviv 63462")
# print(location2.raw)
# userlat2 = location2.latitude
# userlon2 = location2.longitude

# loc2 = (location2.latitude , location2.longitude)
# print (loc2)

# print(geodesic(loc1,loc2).kilometers)

# dist = geodesic(loc1,loc2).kilometers

# print(round(dist,2))














# cur.execute("SELECT id,name FROM countries") 

# rows = cur.fetchall()
    
# for row in rows:    

#     # print( "{} {}"
#     # .format(row["id"], row["name"]))
#     print(row["id"])
      


  

# for row in countryDict:
#     print(row)


    

