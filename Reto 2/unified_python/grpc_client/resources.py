
from flask import render_template, make_response, request, redirect
from flask_restful import Resource
import json
import grpc
import grpc_client
from FileServices_pb2 import FileInfo, FindFileRequest
from google.protobuf.empty_pb2 import Empty
from producerQueue import RunAMQP


class FilesListResource(Resource):

    def get(self):
        headers = {'Content-Type': 'application/json'}
        response = []  # Call Client Here

        try:
            for file in grpc_client.stub.ListFiles(Empty()).file_info:
                serialized = {
                    "name": file.name,
                    "size": file.size,
                    "timestamp": file.timestamp
                }

                response.append(serialized)
        except:
            response = RunAMQP("", function="list")

        return make_response(json.dumps(response), 200, headers)


class FilesFindResource(Resource):
    def get(self, name):
        headers = {'Content-Type': 'application/json'}

        findFileReq = FindFileRequest(file_name=name)

        response = []

        try:
            files = grpc_client.stub.FindFile(findFileReq).files_info
        except grpc.RpcError as e:
            response = RunAMQP(name, function="find")
            return make_response(json.dumps(response), 200, headers)

        for file in files:
            response.append({
                "name": file.name,
                "size": file.size,
                "timestamp": file.timestamp
            })

        return make_response(json.dumps(response), 200, headers)
