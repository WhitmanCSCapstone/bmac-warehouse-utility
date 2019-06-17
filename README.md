# bmac-warehouse-utility
This is a loosely put together collection of python scripts used to migrate from the old BMAC warehouse backend to the the new NOSQL JSON based backend hosted on Firebase.

## Access
The scripts are open source but the data used by the scripts is not currently open to the public. If you wish to run the scripts with the corresponding data please contact benlimpich@gmail.com, who will contact the owner of the data and discuss whether to give access.

## Structure of the data:

The scripts are designed to convert seven csv files into JSON, while also editing paticular fields in order to make certain tables reference each other. Each csv file should have its comma-seperated values correspond to the values given below:

**Customers:** customer_id, code, address, city, state, zip, county, contact, phone, email, status, notes

**FundingSources:**  id, code

**Persons:**  unique_id, username, last_name, first_name, address, city, state, zip, phone1, phone2, email, type, status, notes, password

**Products:**  product_id, product_code, funding_source, unit_weight, unit_price, initial_date, initial_stock, minimum_stock, history, current_stock, inventory_date, status, notes

**Providers:**  provider_id, code, type, address, city, state, zip, county, contact, phone, email, status, notes

**Shipments:**  customer_id, funds_source, ship_date, ship_via, ship_items, ship_rate, total_weight, total_price, invoice_date, invoice_no, notes

**Contributions:** provider_id, recieve_date, receive_items, payment_source, billed_amt, notes

## How to run:

If you have the database and/or have a similar database that could use these scripts, here's how you can run them. Put all of your csv files into a directory called `/stub_csvs/`, then, using any version of Python 3, run `python compile_json.py`. The terminal will output updates on its progress and give counts for data that it was unable to create references for and then will create a `master_json.json` file that you can upload directly to your Firebase realtime database.


