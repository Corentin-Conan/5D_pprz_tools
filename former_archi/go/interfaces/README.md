# AirMap Interfaces
This repository contains the [Protocol Buffers](https://github.com/google/protobuf) (version 3) definitions for all public AirMap services that support gRPC.

For more details on all AirMap APIs (including REST) and developer tools, see the [AirMap Developers](https://developers.airmap.com) site.

## Protocol Buffers

Protocol buffers are a language-agnostic and platform-agnostic format for defining, serializing, and exchanging structured data. An interface is defined once via a proto file and then a compiler is used to generate all client source code.

## Generating API client libraries
To generate gRPC source code for AirMap APIs in this repository, you first need to install both Protocol Buffers and gRPC on your local machine. 

See the following tutorials that document how to generate client code specific to your language:

| Language | Tutorial |
|:--|:--|
| C/C++ | https://grpc.io/docs/tutorials/basic/c.html |
| Go | https://grpc.io/docs/tutorials/basic/go.html |
| Java | https://grpc.io/docs/tutorials/basic/java.html |
| Node.js | https://grpc.io/docs/tutorials/basic/node.html |
| PHP | https://grpc.io/docs/tutorials/basic/php.html |
| Python | https://grpc.io/docs/tutorials/basic/python/ |
