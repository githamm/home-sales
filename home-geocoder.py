#!/usr/bin/env python
import geocoder
import csv
import argparse
import doctest
import sys
#import time

def main(args):
    rows = []
    fieldnames = ['address', 'street_number direction_one street street_type direction_two suite', 'city', 'postal', 'lat', 'lng', 'Price', 'Seller_first_name', 'Seller_last_name', 'Buyer_first_name', 'Buyer_last_name', 'Date']

    # Change file name to be geocoded
    with open(args.filename[0][0]) as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            g = geocoder.mapquest(line['location'], key='Qb2nRPKta84mwdnWUMI4BEIgQo5y6EAX')

            # Fix up the record a little
            if args.date:
                line['Date'] = args.date

            # Add the CSV line data into the Geocoder JSON result
            result = g.json

            # Fix zipcode, removing the hyphen and anything after it if there
            # is a hyphen
            if '-' in result['postal']:
                result['postal'] = result['postal'].split('-')[0]

            result.update(line)

            # Store Geocoder results in a list to save it later
            rows.append(result)

    with open('home-sales-master-template.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
        #time.sleep(2)

def build_parser(args):
    """ This method allows us to test the args.
        >>> parser = build_parser(['-v'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python home-geocoder.py "name of the file.csv"',
                                     description='Geocode stuff in a CSV file.',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true",
                        help="Run doctests, display more info.")
    parser.add_argument("-d", "--date", dest="date",
                        help="Add a date value to add to the output")
    parser.add_argument("filename", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)