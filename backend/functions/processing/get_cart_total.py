import boto3
import json
import decimal
import sqlite3
import os
import tempfile
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

INVENTORY_FILE = "inventory.db"


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

    s3 = boto3.client('s3')
    with tempfile.TemporaryFile() as tmp:
        print("Downloading inventory file.")
        s3.download_fileobj(
            Bucket=os.environ("CLIENT_BUCKET"),
            Key=f"admin/{INVENTORY_FILE}",
            Fileobj=tmp
        )
        tmp.seek(0)
            )
            tmp.seek(0)
            conn = create_connection(tmp)
            if conn is None:
                res = {"status": "error", "message": "could not connect to inventory db."}
            else:
                cur = conn.cursor()

                cart_items = []
                if isinstance
        'body': json.dumps(res)
    }
