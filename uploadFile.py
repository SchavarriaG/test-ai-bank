import boto3
import os

s3 = boto3.resource('s3')
bucket = s3.Bucket('ai-technical-test-schavar')

file_name = 'test5.txt'
#try:
#    if(os.path.exists(file_name)):
#        print('y')
#except:
#    print("error encontrando el archivo a subir")
#    exit()
#
print("el base name es " + os.path.basename(file_name))
obj = bucket.Object(os.path.basename(file_name))
print(obj.upload_file(file_name))


print("Archivos del bucket:")
for o in bucket.objects.all():
    print(f"\t{o.key}")


