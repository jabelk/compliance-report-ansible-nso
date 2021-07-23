import requests

url = "http://10.10.20.50:8080/restconf/data/tailf-ncs:compliance/reports/report=check-motd/run"

payload = "<input>\n\t<outformat>xml</outformat>\n</input>"
headers = {
  'Content-Type': 'application/yang-data+xml',
  'Authorization': 'Basic YWRtaW46YWRtaW4=',
  'Accept': 'application/yang-data+json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

import os

old_file_name = "~/nso-instance/state/compliance-reports/report_28_admin_1_2021-7-23T12:42:38:0.xml"
new_file_name = "~/nso-instance/state/compliance-reports/report_28_admin_1_2021.xml"

os.rename(old_file_name, new_file_name)

print("File renamed!")


with open('~/nso-instance/state/compliance-reports/report_28_admin_1_2021.xml', 'r') as reader:
    # Further file processing goes here
    print(reader.read())