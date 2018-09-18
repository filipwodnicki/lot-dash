# Data processing Pipeline
# Takes a .csv file with T100 data, reads it line-by-line and inserts in to the database.

import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Airline, Airport, BTS_Record

# engine = create_engine('sqlite:////Users/Filip/code/python/lot-dash/app.db')
engine = create_engine('postgresql://localhost/lotdash_dev')
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Step 1 - Open File
# with open('/Users/Filip/code/python/lot-dash/db/2017_all.csv', newline='') as csvfile:

for i in range(2018,2019):
    print("year",i)
    with open('/Users/Filip/Desktop/T100_International_Segment/' + str(i) +'_80737479_T_T100I_SEGMENT_ALL_CARRIER.csv', newline='') as csvfile:
# with open('/Users/Filip/Desktop/T100_International_Segment/2017_80737479_T_T100I_SEGMENT_ALL_CARRIER.csv', newline='') as csvfile:

        # Step 2 - Read CSV
        csvreader = csv.reader(csvfile, dialect='excel')
        next(csvreader, None)  # skip the headers
        i = 0
        for row in csvreader:
            if i%10==0 and i>0:
                print("Record",i)
            # print(', '.join(row))

            # Read Airline from each Line
            unique_carrier = row[10]
            unique_carrier_name = row[12]
            # print("carrier:", unique_carrier, "carrier_name:", unique_carrier_name)

            ## ONLY DO LOT POLISH AIRLINES ##
            if unique_carrier == "LO":
                # save it
                query = session.query(Airline).filter_by(carrier=unique_carrier, carrier_name=unique_carrier_name).first()
                if query is not None:
                    # print( query.id )
                    this_airline_id = query.id
                else:
                    new_airline = Airline(carrier=unique_carrier, carrier_name=unique_carrier_name)
                    session.add(new_airline)
                    session.commit()
                    this_airline_id = new_airline.id
                    print( "Added new airline:", unique_carrier)
                

                # Read Origin airport from line
                origin_code = row[22]
                origin_city_name = row[23]
                origin_country_code = row[24]
                origin_country_name = row[25]

                # save it
                query = session.query(Airport).filter_by(code=origin_code).first()
                if query is not None:
                    this_origin_id = query.id
                else:
                    new_dest_airport = Airport(code=origin_code, city_name=origin_city_name, country_code=origin_country_code, country_name=origin_country_name)
                    session.add(new_dest_airport)
                    session.commit()
                    this_origin_id = new_dest_airport.id
                    print( "Added new airport:", origin_code)

                # Read Destination airport from line
                dest_code = row[30]
                dest_city_name = row[31]
                dest_country_code = row[32]
                dest_country_name = row[33]
                
                # save it
                query = session.query(Airport).filter_by(code=dest_code).first()
                if query is not None:
                    this_dest_id = query.id
                else:
                    new_dest_airport = Airport(code=dest_code, city_name=dest_city_name, country_code=dest_country_code, country_name=dest_country_name)
                    session.add(new_dest_airport)
                    session.commit()
                    this_dest_id = new_dest_airport.id
                    print( "Added new airport:", dest_code)
                
                # Read Stats from line
                origin_id = this_origin_id
                dest_id = this_dest_id
                airline_id = this_airline_id
                year = row[38]
                quarter = row[39]
                month = row[40]
                departures = int( float( row[1] ) ) #departures_performed
                payload = int( float( row[2] ) )
                seats = int( float( row[3] ) )
                passengers = int( float( row[4] ) )
                freight = int( float( row[5] ) )

                # insert into BTS_Record with foreign keys airline_id, origin_id, dest_id
                new_record = BTS_Record(origin_id=origin_id, dest_id=dest_id, airline_id=airline_id, year=year, quarter=quarter, month=month, departures=departures, payload=payload, seats=seats, passengers=passengers, freight=freight)
                session.add(new_record)
                session.commit()
                i+=1



