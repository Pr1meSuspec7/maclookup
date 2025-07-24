# MAC Address Vendor Lookup

This Python script allows you to look up the vendor for one or more MAC addresses using a local database file. You can also update the database from [maclookup.app](https://maclookup.app/downloads/json-database).

## Requirements

- Python 3.x
- `requests` library

Install dependencies (if needed):

```sh
pip install requests
```

## Usage

### Lookup MAC Addresses

You can look up one or more MAC addresses (colon, dash, or dot separated):

```sh
python maclookup.py -m 00:16:9C:11:11:11 aa-bb-cc-dd-ee-11 00.16.9C.11.11.11
```

### Update the Database

To download the latest vendor database:

```sh
python maclookup.py -u
```

## Output

For each MAC address, the script prints the vendor name if found, or "Vendor not found" otherwise.

Example:

```
00:16:9C:11:11:11 - Cisco Systems, Inc
AA:BB:CC:DD:EE:11 - Vendor not found
```

## Files

- `maclookup.py`: Main script.
- `mac-vendors-export.json`: Local vendor database (downloaded/used by the script).

## Notes

- Supported MAC address formats: colon (`:`), dash (`-`), dot (`.`).
- The script selects the vendor with the longest-match mac address
