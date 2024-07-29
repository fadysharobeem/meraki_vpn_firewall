# Meraki Site to site vpn firewall updater
This project allows you to update the firewall rules of site to site VPN of a Cisco Meraki organization using data from a CSV file. It uses the Meraki API to fetch organization details and update the firewall rules of site to site VPN.

## Prerequisites

- Python 3.x
- `requests` library
- A valid Meraki API key

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/meraki_vpn_firewall.git
    cd meraki_vpn_firewall
    ```

2. Install the required libraries:
    ```sh
    pip3 install requests
    ```

## Configuration

1. Ensure your CSV file (`fw.csv`) has the following columns:
    - `policy`
    - `protocol`
    - `srcCidr`
    - `srcPort`
    - `destCidr`
    - `destPort`
    - `comment`
    - `syslogEnabled` (values should be "true" or "false")

## Usage

1. Run the script:
    ```sh
    python3 app.py
    ```

2. The script will ask for your API key.

3. The script will fetch the organizations associated with your API key and display a list of them. Select the organization number from the list.

4. The script will read the firewall rules from the `fw.csv` file and update the selected organization's firewall rules.

## Example `fw.csv`

```csv
policy,protocol,srcCidr,srcPort,destCidr,destPort,comment,syslogEnabled
allow,tcp,192.168.1.0/24,80,10.0.0.0/24,8080,Allow traffic,true
deny,udp,192.168.2.0/24,,10.0.1.0/24,53,Deny DNS,false
