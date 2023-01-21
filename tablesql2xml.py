import xml.etree.ElementTree as xml
import xml.etree.cElementTree as ET
import mysql.connector



def getConn():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "Chimica90$"
    )
    cur = cnx.cursor(dictionary=True)
    return cnx,cur



def createSubEl(dic):
    # create Hotel element and append it to the root
    id = [v for k,v in dic.items() if k == "HotelId"][0]
    id = str(id)
    subElementId = xml.SubElement(root,'Hotel')
    subElementId.set('id',id)
    subElementId.text = id

    #create Name element and append it to the root
    subElementName = [key for key in list(dic.keys()) if key == "Name"][0] 
    text = dic[subElementName]
    subElementName = xml.SubElement(subElementId,subElementName)
    subElementName.text = text

   # create Address element and append it to the root
    subElementAddress = [key for key in list(dic.keys()) if key == "Address"][0] 
    text = dic[subElementAddress]
    subElementAddress = xml.SubElement(subElementId,subElementAddress)
    subElementAddress.text = text


    # create Rating element and append it to the root
    subElementRating = [key for key in list(dic.keys()) if key == "Rating"][0]
    Rating = [v for k,v in dic.items() if k == "Rating"][0]
    Rating = str(Rating)
    subElementRating = xml.SubElement(subElementId,subElementRating)
    subElementRating.text = Rating

    return 



def createXML(filename):

    list(map(createSubEl,result))
  
    tree = xml.ElementTree(root)
       
    tree.write(filename)
    
    
if __name__=='__main__':

    cnx, cur = getConn()
    cnx.cursor(dictionary=True)
    cur.execute("use HotelData_db")

    table = "Hotels"
    select_stamt1 = f"""select * from {table}"""

    cur.execute(select_stamt1)

    result = cur.fetchall()

   

    print("Preparing XML file ...")
    
    root = xml.Element(table)

    createXML("HotelData.xml")

 
