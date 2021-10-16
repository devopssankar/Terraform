import urllib.request, json, csv, sys, argparse, time

header = ['Key', 'subscriber', 'notificationsSuppressed', 'destination', 'productId', 'versionId', 'email', 'universe', 'seedData', 'fileTransferProfile', 'createdDate', 'lastUpdatedDate', 'deliveryFrequency', 'notificationType', 'status', 'dunsCount', 'globalUltimateCount', 'subscriberName', 'state', 'suppressionDate', 'contractExpiryDate', 'familyTree']
fileOutput = "monitoringreg.csv"
outputFile = open(fileOutput, 'w')
output = csv.writer(outputFile)
output.writerow(header)

try:
    api = sys.argv[1]
    with urllib.request.urlopen(api) as url:
        records = json.loads(url.read().decode())
        for record in records:
            row = []
            row.append(record['key'])
            row.append(record['subscriber'])
            row.append(record['notificationsSuppressed'])
            row.append(record['registration']['destination']['type'])
            if "productId" in record['registration']:
                row.append(record['registration']['productId'])
            else:
                row.append('NA')
            if "versionId" in record['registration']:
                row.append(record['registration']['versionId'])
            else:
                row.append('NA')
            row.append(record['registration']['email'])
            if "universe" in record['registration']:
                row.append(record['registration']['universe'])
            else:
                row.append('LOD')
            row.append(record['registration']['seedData'])
            if "fileTransferProfile" in record['registration']:
                row.append(record['registration']['fileTransferProfile'])
            else:
                row.append('NA')
            row.append(record['registration']['createdDate'])
            row.append(record['registration']['lastUpdatedDate'])
            row.append(record['registration']['deliveryFrequency'])
            row.append(record['registration']['notificationType'])
            row.append(record['status'])
            row.append(record['dunsCount'])
            row.append(record['globalUltimateCount'])
            row.append(record['subscriberName'])
            row.append(record['state'])
            row.append(record['suppressionDate'])
            row.append(record['contractExpiryDate'])
            row.append(record['familyTree'])
            output.writerow(row)
except (IndexError):
    print("Please provide monitoring API URL as input when executing this script. \nfor e.g. python3 monitoringreg.py https://url")
