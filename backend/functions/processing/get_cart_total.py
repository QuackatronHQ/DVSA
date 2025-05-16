import boto3
import json
import decimal
import sqlite3
import os
import tempfile
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

INVENTORY_FILE = "inventory.db"
INVENTORY_PATH = [INVENTORY_FILE]


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def lambda_handler(event, context):
    print(json.dumps(event))
    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    total = 0
    missing = {}
    cart = json.loads(event['body'])
    inventory_file_path = None

    for i_path in INVENTORY_PATH:
        if os.path.exists(i_path):
            inventory_file_path = i_path
            print("inventory db file already exists")
            break

    if inventory_file_path is None:
        s3 = boto3.client('s3')
        print("Downloading inventory file.")
        with tempfile.TemporaryFile() as tmp:
            s3.download_fileobj(
                Bucket=os.environ("CLIENT_BUCKET"),
                Key=f"admin/{INVENTORY_FILE}",
                Fileobj=tmp
            )
            tmp.seek(0)
            tmp.read()
        inventory_file_path = INVENTORY_FILE
                        'statusCode': 200,
                        'body': json.dumps(res)
                    }
                if quantity < qty:
                    missing[obj] = qty - quantity
                    qty = quantity

                total = total + (qty*price)

            res = {"status": "ok", "total": float(total), "missing": missing}
        print(f"return value: {json.dumps(res)}")
        return {
            'statusCode': 200,
            'body': json.dumps(res)
        }
