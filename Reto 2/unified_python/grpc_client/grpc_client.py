import grpc
from FileServices_pb2_grpc import FileServicesStub
from dotenv import load_dotenv
import os

load_dotenv()

GRPC_HOST = os.getenv('GRPC_HOST')

channel = grpc.insecure_channel(GRPC_HOST)
stub = FileServicesStub(channel=channel)