import unittest
import json
import boto3
from botocore.exceptions import ClientError
from app import validate_md5
from app import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def test_validate_md5(self):
        md5 = "2f941516446dce09bc2841da60bf811f"
        md5_v2="38abbcf1df0f703a39c0b74da324fce6"
        valuesCaseSuccess = [250,25,10,100,100,7,8,"2f941516446dce09bc2841da60bf811f"]
        valuesCaseSuccess_v2 = [250,250,10,101,101,700,8, "2f941516446dce09bc2841da60bf811f"]
        self.assertEqual(validate_md5(md5, valuesCaseSuccess), "Comparition Success")
        self.assertEqual(validate_md5(md5_v2, valuesCaseSuccess_v2), "Comparition Success")
    
    def test_validate_md5_excepcion(self):
        md5 = "2f941516446dce09bc2841da60bf811f"
        valuesCaseFailed = [250,250,10,101,101,700,8, "2f941516446dce09bc2841da60bf811f"]
        with self.assertRaises(Exception):
            validate_md5(md5, valuesCaseFailed)

    def test_lambda_handler_excepcion_permisions(self):
        with open("evento.json") as f:
            raw_data = f.read()
        evento = json.loads(raw_data.encode("utf-8-sig"))
        evento['Records'][0]['s3']['object']['key'] = "test1.txt"
        context = None
        with self.assertRaises(ClientError):
            lambda_handler(evento, context)

    def test_lambda_handler_excepcion_estructure_file(self):
        with open("evento.json") as f:
            raw_data = f.read()
        evento = json.loads(raw_data.encode("utf-8-sig"))
        evento['Records'][0]['s3']['object']['key'] = "test.txt"
        context = None
        with self.assertRaises(IndexError):
            lambda_handler(evento, context)

if __name__ == '__main__':
    unittest.main()