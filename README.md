# Linode Dynamic DNS
This project aims to create dynamic dns like functionality using Linode.

## Rationale
You already pay for one or more Linodes and host your DNS through Linode, then you 
can use this script.

## How it Works
Leverages the Linode API to store and manage DNS for an IP Address.

- Uses whatsmyip service to get your current IP Address
- From that address, it checks to see if the IP Address has changed since the last poll by checking the contents of ip.txt
- If the ip addresses differ, then use the Linode API to change a specified DNS entry in a domain.  
- Only contacts linode if the address has changed, so linode is polled only when an address changes.
- Written in Python and can customize it

## Configuration example

```
[default]
token = linode_api_key_token
domains = 12222333
records = 3344555
```

token = Linode token

domains = id of the domain

records = the record to change

## Usage

```bash

python dydns.py --configuration config.py

```
