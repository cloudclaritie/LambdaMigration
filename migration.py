#! /usr/bin/python 

import json
import os
import sys
from pprint import pprint

os.system("aws lambda list-functions  > data.json")

if(len(sys.argv) != 3):
    print((sys.argv))
    print("Please give command line inputs for origin region and destintion region")
    print("All lambda will be moved from origin region to destinatipon region") 
    print("e.g: ./migration.py us-east-1 us-east-2 ")
    exit()

region1 = sys.argv[1]
region2 = sys.argv[2]
print(region1)
print(region2)

print("Starting download of all lambda in region " + region1)
with open('data.json') as data_file:    
    data = json.load(data_file)
    counter = 1
    for p in data['Functions']:
        lambdaName = p['FunctionName']
        print("   " + str(counter) + ". Downloading lambda " + lambdaName)
        command = "aws lambda get-function --function-name " + lambdaName + " --query 'Code.Location' | xargs wget -O ./lambda_functions/" +  lambdaName + ".zip "
        counter = counter + 1
#        print(command)
        os.system(command) 

print("\nAll lambda are downloaded\n") 
print("Now starting to upload lambda in region " + region2)

counter = 1
for fileName in os.listdir('./lambda_functions/'):
    if fileName.endswith('.' + "zip"):
        mainFile=fileName.split(".",1)
        print("   " + str(counter) + ". Uploading lambda " + fileName + " in N Virginia reion")
#        print(mainFile[0]) 
        command = "aws lambda create-function --function-name " + mainFile[0] + " --zip-file fileb://lambda_functions/" + fileName + " --handler index.handler --runtime nodejs8.10 --role arn:aws:iam::155184495185:role/lambda-cli-role --region " + region2
#        print(command)
        os.system(command)  
        counter = counter + 1

print("\nAll lambda are uploaded\n")
