from vanitynumber import *
import boto3

def lambda_handler(event, context):
    VanityRet = {}
    # Fetch phone number from event details and format
    PhNum = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
    NewPhNum = PhNum[:2] + "-" +PhNum[2:5] + "-" +PhNum[5:8] + "-" +PhNum[8:]
    
    try:
        dynamodb = boto3.resource('dynamodb')
        VanityNumTable = dynamodb.Table('VanityNum')
        response = VanityNumTable.get_item(
            TableName = 'VanityNum',
            Key = {
                'PhoneNum' : NewPhNum
                }
        )
        
        item = response['Item'] 
        
        # Return Vanity options
        VanityRet["recordFound"] = "True"
        VanityRet["vanity1"] = item["Vanity1"]
        VanityRet["vanity2"] = item["Vanity2"]
        VanityRet["vanity3"] = item["Vanity3"]
        VanityRet["vanity4"] = item["Vanity4"]
        VanityRet["vanity5"] = item["Vanity5"]
        
    except:
    
        resp = all_wordifications(NewPhNum)
        #vanity1 = resp[0]
        VanityRet["recordFound"] = "True"
        VanityRet["vanity1"] = resp[0]
        VanityRet["vanity2"] = resp[1]
        VanityRet["vanity3"] = resp[2]
        VanityRet["vanity4"] = resp[3]
        VanityRet["vanity5"] = resp[4]
        
        response = VanityNumTable.put_item(
            TableName = 'VanityNum',
            Item = {
                'PhoneNum' : NewPhNum,
                'Vanity1' : VanityRet["vanity1"],
                'Vanity2' : VanityRet["vanity2"],
                'Vanity3' : VanityRet["vanity3"],
                'Vanity4' : VanityRet["vanity4"],
                'Vanity5' : VanityRet["vanity5"]
                }
            )
        
    
    return(VanityRet)	