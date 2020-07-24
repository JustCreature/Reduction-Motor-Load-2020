import csv
import subprocess
import base64

read = "C:/Users/Zavarcev-NA/Desktop/data_log.bbld"
write = "C:/Users/Zavarcev-NA/111.csv"

with open(write, 'w', newline='') as write_file:
    writer = csv.writer(write_file, delimiter=';')

    # subprocess.call(['attrib', '-h', read])
    f = open(read, "r")
    decode = base64.b64decode(str.encode(f.read()))
    existing_data = eval(decode.decode())
    print(existing_data[0])

    f.close()
    # subprocess.call(['attrib', '+h', read])


    for row in existing_data:
        # print("qqq", ",".join(row))
        writer.writerow(row)

