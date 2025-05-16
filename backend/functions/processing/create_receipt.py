import json
import decimal
import boto3
import os
from datetime import datetime
import sqlite3
import tempfile


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


# status list
# -----------
# 100: open
# 110: payment-failed
# 120: paid
# 200: processing
# 210: shipped
# 300: delivered
# 500: cancelled
# 600: rejected
def lambda_handler(event, context):
    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)
    print(event)
    data = json.loads(event["Records"][0]["body"])

    orderId = data["orderId"]
    userId = data["userId"]

    # GET ITEMS FOR ORDER
    dynamodb = boto3.resource('dynamodb')
    order_table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    with tempfile.TemporaryFile() as tmp:
        response = order_table.get_item(
            Key={
                "orderId": orderId,
            }
        )
        # additional file operations using tmp can be added here
