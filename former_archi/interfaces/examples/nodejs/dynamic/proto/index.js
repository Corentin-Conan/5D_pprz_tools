const grpc = require('grpc')
const pl = require('@grpc/proto-loader')
const proto_path = __dirname + '/../../../../grpc'

// Load the gRPC package definitions.
const packageDefinition = pl.loadSync(
    [
        'ack.proto',
        'emitter.proto',
        'identity.proto',
        'ids.proto',
        'measurements.proto',
        'report.proto',
        'sensors.proto',
        'status.proto',
        'telemetry.proto',
        'track.proto',
        'tracking.proto',
        'units.proto'
    ],
    {
        enums: String,
        keepCase: true,
        longs: String,
        oneofs: true,

        includeDirs: [
            proto_path + '/',
            proto_path + '/ids',
            proto_path + '/measurements',
            proto_path + '/system',
            proto_path + '/telemetry',
            proto_path + '/tracking',
            proto_path + '/units',
            __dirname + "/../node_modules/google-proto-files"
        ]
    })

exports.descriptors = grpc.loadPackageDefinition(packageDefinition)