import requests, pprint, csv, json

#############################
API_Key= input("\033[92mEnter your API key to start the code: \033[0m")
#############################
base_url = "https://api.meraki.com/api/v1"
headers = {
    "Authorization": f"Bearer {API_Key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
orgIdlist = []
orgNamelist = []

def updateS2SFw(organizationId, data):
    url = f"{base_url}/organizations/{organizationId}/appliance/vpn/vpnFirewallRules"
    payload = {
        "rules": data,
        "syslogDefaultRule": False
    }
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        # pprint.pprint(response.json())
        print("--- \033[96mCongrats, Meraki rules has been configured.\033[0m")
    else:
        print(f"\033[91mError with configuring site to site VPN: {response.status_code}\033[0m")
        pprint.pprint(response.json())

def readFwFromCsv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rule = {
                "policy": row.get("policy"),
                "protocol": row.get("protocol"),
                "srcCidr": row.get("srcCidr"),
                "srcPort": row.get("srcPort"),
                "destCidr": row.get("destCidr"),
                "destPort": row.get("destPort"),
                "comment": row.get("comment"),
                "syslogEnabled": row.get("syslogEnabled").lower() == 'true'
            }
            data.append(rule)
    return data

def getOrgs():
    url = f"{base_url}/organizations"
    response = requests.get(url, headers=headers)
    return response.json()

def getUserChoice(orgNameList):
    for idx, org in enumerate(orgNameList, start=1):
        print(f"{idx}. {org}")
    while True:
        try:
            userChoice = int(input("\033[92mSelect the Org number: \033[0m"))
            if 1 <= userChoice <= len(orgNameList):
                return userChoice
            else:
                print(f"\033[91mInvalid choice. Please choose a number between 1 and {len(orgNameList)}.\033[0m")
        except ValueError:
            print("\033[91mInvalid input. Please enter a number.\033[0m")

# Capture all the orgs associated with that API key
orgs = getOrgs()

# Save the org list into variables
for org in orgs:
    orgIdlist.append(org['id'])
    orgNamelist.append(org['name'])

# Get the user to select the org from the list
userChoice = getUserChoice(orgNamelist)
selectedOrg = orgIdlist[userChoice - 1]
excelData = readFwFromCsv("fw.csv")
print("--- \033[96mReading the csv data\033[0m")
pprint.pprint(excelData)

try:
    yesorno = input("\033[93mAre you happy for me to configure the rules (Yes/No): \033[0m")
    if yesorno.lower() == "yes" or  yesorno.lower() == "ya" or yesorno.lower() == "yep" or yesorno.lower() == "y":
        print("--- \033[96mConfiguring Meraki site to site VPN firewall rules\033[0m")
        updateS2SFw(selectedOrg, excelData)
    else:
        exit
except Exception as e:
    print(f"\033[91mThis org might not have MX\033[0m")
