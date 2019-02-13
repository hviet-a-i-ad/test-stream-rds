import json
# import boto3
import os

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
  DeleteRowsEvent,
  UpdateRowsEvent,
  WriteRowsEvent,
)

def main():
  host = os.getenv('HOST')
  user = os.getenv('USER')
  password = os.getenv('PASSWORD')
  # kinesis = boto3.client("kinesis")

  stream = BinLogStreamReader(
    connection_settings= {
      "host": host,
      "port": 3306,
      "user": user,
      "passwd": passwords},
    server_id=100,
    blocking=True,
    resume_stream=True,
    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])

  for binlogevent in stream:
    for row in binlogevent.rows:
      event = {"schema": binlogevent.schema,
      "table": binlogevent.table,
      "type": type(binlogevent).__name__,
      "row": row
      }

      # kinesis.put_record(StreamName="<STREAM_NAME>", Data=json.dumps(event), PartitionKey="default")
      print(json.dumps(event))

if __name__ == "__main__":
   main()
