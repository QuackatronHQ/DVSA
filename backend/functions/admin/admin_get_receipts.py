import json
import boto3
import os
import zipfile
import tempfile

def download_dir(client, resource, dist, local, bucket=os.environ["RECEIPTS_BUCKET"]):
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        if result.get('Contents') is not None:
            for file in result.get('Contents'):
                target_path = os.path.join(local, file.get('Key'))
                if not os.path.exists(os.path.dirname(target_path)):
                    os.makedirs(os.path.dirname(target_path))
                resource.meta.client.download_file(bucket, file.get('Key'), target_path)
    return


def lambda_handler(event, context):
    client = boto3.client('s3')
    resource = boto3.resource('s3')
    m = ""
    d = ""
    y = event["year"]
    if "month" in event:
        m = event["month"] + "/"
        if "day" in event:
            d = event["day"] + "/"

    prefix = "{}/{}{}".format(y, m, d)
    bucket = os.environ["RECEIPTS_BUCKET"]
    zip_file = "{}dvsa-order-receipts.zip".format(prefix.replace("/", "-"))

    with tempfile.TemporaryDirectory() as local_dir:
        download_dir(client, resource, prefix, local_dir, bucket)
        with tempfile.TemporaryFile() as tmp:
            zf = zipfile.ZipFile(tmp, "w")
            for dirname, subdirs, files in os.walk(local_dir):
                zf.write(dirname, arcname=os.path.relpath(dirname, local_dir))
                for filename in files:
                    if filename.endswith(".txt"):
                        filepath = os.path.join(dirname, filename)
                        zf.write(filepath, arcname=os.path.relpath(filepath, local_dir))
            zf.close()
            tmp.seek(0)
            client.upload_fileobj(tmp, bucket, "zip/" + zip_file)

    signed_link = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': "zip/" + zip_file},
                                                ExpiresIn=3600)

    res = {"status": "ok", "download_url": signed_link}
    return res
    res = {"status": "ok", "download_url": signed_link}
    return res

    res = {"status": "ok", "download_url": signed_link}
    return res
    signed_link = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': "zip/" + zip_file}, ExpiresIn=3600)

    res = {"status": "ok", "download_url": signed_link}
    return res
    signed_link = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': "zip/" + zip_file},
                                                ExpiresIn=3600)

    res = {"status": "ok", "download_url": signed_link}
    return res
