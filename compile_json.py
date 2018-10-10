import json
import glob
import csv

csv_files = glob.glob("./stub_csvs/*.csv")

field_names = {
    "providers": [
        "activity_status",
        "address",
        "city",
        "contact_email",
        "contact_name",
        "contact_phone_num",
        "county",
        "id",
        "name",
        "state",
        "type",
        "zip",
    ],

}



#for f in csv_files:
    #file = open(f, "r")
    #reader = csv.DictReader( csvfile, fieldnames)






json_files = glob.glob("./stub_json/*.json")

obj_list = []

for f in json_files:
    with open(f, 'rb') as data:
        obj = json.load(data)
        obj_list.append(obj)

# erase the contents of the file
open("master_json.json", "w").close()

#write the compiled json to master_json.json
with open("master_json.json", "w") as outfile:
    json.dump(obj_list, outfile, indent=4, sort_keys=True)
