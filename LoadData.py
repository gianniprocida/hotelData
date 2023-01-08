import mysql.connector
from bot import grab_links
from scraping import hotelWebsite

# Run this script first

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chimica90$"
)



c = mydb.cursor()


Q1 ="""create database if not exists another1_db"""

Q2 ="""use another1_db"""

Q3 ="""create table if not exists ListofHotels (HotelId int(10) auto_increment, 
name varchar(100), Address varchar(100), Stars int, primary key(HotelId));"""

Q4 = """create table if not exists ListofScores (ScoreId int(10) auto_increment, foreign key(ScoreId) references ListofHotels(HotelId), 
Staff numeric(4,2), Facilities numeric(4,2), Cleanliness decimal(4,2), Comfort numeric(4,2), Value_for_money numeric(4,2), 
Location numeric(4,2), Free_WiFi numeric(4,2), primary key(ScoreId));"""

Q5 = """create table if not exists ListofFacilities (FacilitiesId int(10) auto_increment, foreign key(FacilitiesId) 
 references ListofHotels(HotelId), Free_WiFi enum('YES','None'), Family_rooms enum('YES','None'), Pets_allowed enum('YES','None'), 
 NonSmoking_rooms enum('YES','None'), Restaurant enum('YES','None'), Facilities_for_disabled_guests enum('YES','None'), 
 Heating enum('YES','None'), primary key(FacilitiesId));"""

insertIntoParent="""insert into ListofHotels (name, Address, Stars) values (%s,%s,%s);"""

insertIntoChild1 = """insert into ListofScores (ScoreId, Staff, Facilities, Cleanliness, Comfort, 
value_for_money, Location, Free_WiFi) values (%s,%s,%s,%s,%s,%s,%s,%s);"""

insertIntoChild2 = """insert into ListofFacilities (FacilitiesId, Free_WiFi, Family_rooms, Pets_allowed, 
NonSmoking_rooms, Restaurant, Facilities_for_disabled_guests, Heating) values (%s,%s,%s,%s,%s,%s,%s,%s)"""

c.execute(Q1)
c.execute(Q2)
c.execute(Q3)
c.execute(Q4)
c.execute(Q5)





if __name__=='__main__':
   hotelLinks = grab_links()

   objects = [hotelWebsite(i) for i in hotelLinks]

   # Grab general info
   listofHotels, listofScores, listofFacilities = [], [], []

   for i in range(len(objects)):
       try:
           if len(objects[i].get_Info())!=3 or len(objects[i].get_reviews())!=7 or len(objects[i].get_PopularFacilities())!=7:
             continue
           else:
                listofHotels.append(objects[i].get_Info())
                listofScores.append(objects[i].get_reviews())
                listofFacilities.append(objects[i].get_PopularFacilities())
       except Exception:
           continue


       #
       # try:
       #     listofHotels.append(objects[i].get_Info())
       #     listofScores.append(objects[i].get_reviews())
       #     listofFacilities.append(objects[i].get_PopularFacilities())
       # except Exception:
       #     continue

   for n,record in enumerate(listofHotels):
       c.execute(insertIntoParent,record)
       last_id=c.lastrowid
       c.execute(insertIntoChild1,(last_id,) + listofScores[n])
       c.execute(insertIntoChild2,(last_id,)+ listofFacilities[n])

   mydb.commit()

