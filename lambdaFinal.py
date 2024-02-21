import boto3
import json
import urllib.parse
import hashlib
from datetime import datetime

s3 = boto3.client('s3')
dynamobd = boto3.resource('dynamodb')
table = dynamobd.Table('ai-technical-test-schavar') # podría guardarse en una variable de entorno o secreto

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        response_get = s3.get_object(Bucket=bucket, Key=key)
        print(response_get)
        
        file = response_get['Body'].read().decode('utf-8')
        lines = file.splitlines()  
        
        md5_extracted = lines[7].split("=")[1]  #extraigo el reglón del hash

        text_for_encode = ""
        items = []
        values = []
        for i in range(len(lines)-1):
            items.append(lines[i].split("=")[0])
            values.append(int(lines[i].split("=")[1]))
            text_for_encode += str(values[i]) + "~"  #concateno solo valores

        text_for_encode = text_for_encode[:-1] #elimino último caracter

        #genero el hash con los datos del archivo
        md5_template = hashlib.md5()
        md5_template.update(texto.encode())
        md5_created = md5_template.hexdigest()

        print("Se comparan los hash:")
        print(str(md5_created) == str(md5_extracted))

        localtime_now = datetime.now().timestamp()

        registry={
            'timestamp':str(localtime_now), #mejor en str para obtener decimales
            items[0]:values[0],
            items[1]:values[1],
            items[2]:values[2],
            items[3]:values[3],
            items[4]:values[4],
            items[5]:values[5],
            items[6]:values[6],
            'hash':md5_extracted
        }

        #inserto registro a la dynamo
        response_put = table.put_item(Item=registry)
        print(response_put)

        #Borro archivo del bucket
        response_delete = s3_cliente.delete_object(Bucket=bucket, Key=key)
        print(response_delete)

        return 0
    except Exception as e:
        print(e)
        raise e