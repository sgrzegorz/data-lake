from websocket import create_connection
import time
import threading
from minio import Minio
from minio.error import S3Error
from io import BytesIO
import os
import re

# Time to feed single file in seconds
timeout = 5

def find_env_variable_by_regex(regex):
    for k, v in os.environ.items():
        if re.match(regex, k):
            return v
    return None

minio_service_host_reqex = r'MINIO_\d+_SERVICE_HOST'
minio_service_port_reqex = r'MINIO_\d+_SERVICE_PORT'

minio_service_host = find_env_variable_by_regex(minio_service_host_reqex)
minio_service_port = find_env_variable_by_regex(minio_service_port_reqex)

ws = create_connection("wss://ws-feed.exchange.coinbase.com")
ws.send(
    """{
    "type": "subscribe",
    "product_ids": [
        "ETH-USD"],
    "channels": [
        "level2",
        "heartbeat",
        {
            "name": "ticker",
            "product_ids": [
                "ETH-USD"]
        }
    ]
}
"""
)

def upload_to_minio(filename):
    host = f"{minio_service_host}:{minio_service_port}"
    access_key = "rootuser"
    secret_key = "rootpass123"
    minioClient = Minio(host, access_key=access_key, secret_key=secret_key,
                        secure=False)

    try:
        with open(filename, 'r') as file:
            text = file.read()
    except IOError:
        print(f"{filename} Could not read file")
        return
    print(type(text))
    bucket = "coinbase-bucket"
    content = BytesIO(bytes(text, 'utf-8'))
    key = filename
    size = content.getbuffer().nbytes

    try:
        print(f'{filename} Starting file sending')
        minioClient.put_object(bucket, key, content, size)
        print(f'{filename} File was sent')
    except S3Error as err:
        print(f'{filename} Could not send to minio', err)

    os.remove(filename)
    print(f'{filename} Local version removed')



filename = f"data_{time.time()}.txt"
f = open(filename, "a")
print ("Sent")
print ("Receiving...")
start = time.time()
while True:
    result = ws.recv()
    f.write(result + '\n')
    if (time.time() - start > timeout):
        print(f"Creating new file {filename}")
        f.close()
        upload_thread = threading.Thread(target=upload_to_minio, args=(filename,))
        upload_thread.start()

        filename = f"data_{time.time()}.txt"
        f = open(filename, "a")
        start = time.time()
ws.close()
