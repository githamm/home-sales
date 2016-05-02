import geocoder
import csv
#import time

rows = []
fieldnames = ['address', 'street_number direction_one street street_type direction_two suite', 'city', 'postal', 'lat', 'lng', 'Price', 'Seller_first_name', 'Seller_last_name', 'Buyer_first_name', 'Buyer_last_name', 'Date']

# Change file name to be geocoded
with open('Dubus Excel_05-02-2016.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        g = geocoder.mapquest(line['location'])

        # Add the CSV line data into the Geocoder JSON result
        result = g.json
        result.update(line)

        # Store Geocoder results in a list to save it later
        rows.append(result)

with open('home-sales-master.csv', 'a') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)
    #time.sleep(2)
