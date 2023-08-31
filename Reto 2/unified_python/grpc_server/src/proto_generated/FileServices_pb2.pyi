from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileInfo(_message.Message):
    __slots__ = ["name", "size", "timestamp"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    timestamp: str
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ..., timestamp: _Optional[str] = ...) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ["file_info"]
    FILE_INFO_FIELD_NUMBER: _ClassVar[int]
    file_info: _containers.RepeatedCompositeFieldContainer[FileInfo]
    def __init__(self, file_info: _Optional[_Iterable[_Union[FileInfo, _Mapping]]] = ...) -> None: ...

class FindFileRequest(_message.Message):
    __slots__ = ["file_name"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...

class FindFileResponse(_message.Message):
    __slots__ = ["files_info"]
    FILES_INFO_FIELD_NUMBER: _ClassVar[int]
    files_info: _containers.RepeatedCompositeFieldContainer[FileInfo]
    def __init__(self, files_info: _Optional[_Iterable[_Union[FileInfo, _Mapping]]] = ...) -> None: ...
