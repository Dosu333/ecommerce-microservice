# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: product.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'product.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\x12\x07product\".\n\x0eProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"\x1e\n\x10ProductIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"3\n\x0fProductResponse\x12\x11\n\tavailable\x18\x01 \x01(\x08\x12\r\n\x05price\x18\x02 \x01(\x01\"N\n\x15ProductDetailResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04slug\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x01\x32\x9a\x01\n\x0eProductService\x12?\n\nCheckStock\x12\x17.product.ProductRequest\x1a\x18.product.ProductResponse\x12G\n\nGetProduct\x12\x19.product.ProductIdRequest\x1a\x1e.product.ProductDetailResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCTREQUEST']._serialized_start=26
  _globals['_PRODUCTREQUEST']._serialized_end=72
  _globals['_PRODUCTIDREQUEST']._serialized_start=74
  _globals['_PRODUCTIDREQUEST']._serialized_end=104
  _globals['_PRODUCTRESPONSE']._serialized_start=106
  _globals['_PRODUCTRESPONSE']._serialized_end=157
  _globals['_PRODUCTDETAILRESPONSE']._serialized_start=159
  _globals['_PRODUCTDETAILRESPONSE']._serialized_end=237
  _globals['_PRODUCTSERVICE']._serialized_start=240
  _globals['_PRODUCTSERVICE']._serialized_end=394
# @@protoc_insertion_point(module_scope)
