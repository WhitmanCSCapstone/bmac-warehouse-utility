import json
import uuid
import glob
from datetime import datetime


def give_uniq_ids(file_name, key):

    file = open(file_name, 'r')
    data = json.loads(file.read())
    file.close()

    objects = data[key]

    new_dict = {key: {}}

    for obj in objects:
        uniq_id = uuid.uuid5(uuid.NAMESPACE_OID, str(obj))

        # make objs self-referential
        obj['uniq_id'] = str(uniq_id)

        date = None
        accessor = None

        if('Shipments' in file_name):
            accessor = 'ship_date'
            date = obj[accessor]
        elif('Products' in file_name):
            accessor = 'initial_date'
            date = obj[accessor]
        elif('Contributions' in file_name):
            accessor = 'recieve_date'
            date = obj[accessor]

        if(accessor is not None and date != ''):
            date = date[0:8]
            try:
                date = datetime.strptime(date, '%y-%m-%d')
            except:
                date = datetime.strptime(date, '%m-%d-%y')

            # get POSIX time
            seconds = (date - datetime(1970,1,1)).total_seconds()
            # convert from UTC to PST
            seconds = seconds + (7 * 60 * 60)
            obj[accessor] = seconds
            if('Shipments' in file_name and obj['invoice_date'] != ''):
                accessor = 'invoice_date'
                date = obj[accessor]
                date = date[0:8]
                try:
                    date = datetime.strptime(date, '%y-%m-%d')
                except:
                    date = datetime.strptime(date, '%m-%d-%y')

                    # get POSIX time
                seconds = (date - datetime(1970,1,1)).total_seconds()
                obj[accessor] = seconds

        new_dict[key][str(uniq_id)] = obj

    with open(file_name, 'w') as outfile:
        json.dump(new_dict, outfile)


# get all the new json files
json_files = glob.glob("./stub_json/*.json")

for file_name in json_files:
    if "Customers" not in file_name and "Providers" not in file_name:
        key = file_name[12:-5].lower()
        give_uniq_ids(file_name, key)
