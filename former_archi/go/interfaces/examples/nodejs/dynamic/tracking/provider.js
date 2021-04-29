// Bootstrap our dependencies.
const grpc = require('grpc')
const auth = require('../auth')
const proto = require('../proto')

// Configure your env with your client id and client secret
const API_ENDPOINT = process.env.API_ENDPOINT || 'api.airmap.com:443'
const CLIENT_ID = process.env.CLIENT_ID
const CLIENT_SECRET = process.env.CLIENT_SECRET
const PROVIDER_ID = process.env.PROVIDER_ID || 'demo'

// The starting coordinate for the simulation. Defaults to Baja California
const COORDINATE_LATITUDE = process.env.COORDINATE_LATITUDE | 23.3575
const COORDINATE_LONGITUDE = process.env.COORDINATE_LONGITUDE || -109.823

function connectProvider(token) {

  const tracking = proto.descriptors.tracking
  const collector = new tracking.Collector(API_ENDPOINT, grpc.credentials.createSsl())

  const metadata = new grpc.Metadata()
  metadata.add("authorization", "Bearer " + token)

  const client = collector.ConnectProvider(metadata)

  client.on('data', function (response) {
    if (response.ack) {
      console.log('received ack from collector: ', response.ack.count)
    } else {
      console.log('received status from collector: ', response.status.level)
    }
  })

  client.on('end', function () {
    console.log('client connection to collector ended')
  })

  client.on('error', function (error) {
    throw error
  })

  return client
}

function runSimulation(client) {

  var lat = COORDINATE_LATITUDE
  var lng = COORDINATE_LONGITUDE

  setInterval(function () {
    // Advance the coordinate position at each tick
    lng += 0.001
    lat += 0.001

    console.log(lat)
    console.log(lng)

    const update = buildUpdate(lat, lng)
    client.write(update)

  }, 1000)
}

function buildUpdate(lat, lng) {

  // the current time in milliseconds
  const now = new Date()
  const seconds = now / 1000
  const nanos = (now % 1000) * 1e6

  const observed = {
    seconds: seconds,
    nanos: nanos
  }

  const position = {
    absolute: {
      coordinate: {
        latitude: {
          value: lat
        },
        longitude: {
          value: lng
        }
      },
      altitude: {
        height: {
          value: 50
        },
        reference: "REFERENCE_ELLIPSOID"
      }
    }
  }

  const update = {
    batch: {
      tracks: [
        {
          observed: observed,
          position: position,
          sensor: {
            primary_radar: {}
          },
          identities: [
            {
              provider_id: {
                as_string: PROVIDER_ID
              }
            },
            {
              track_id: {
                as_string: "001"
              }
            }
          ]
        }
      ]
    }
  }

  return update
}

// Login using the client credentials,
// connect to the collector with a token,
// and run the simulation
auth.authenticateServiceAccount(CLIENT_ID, CLIENT_SECRET)
  .then(connectProvider)
  .then(runSimulation)
  .catch(console.log)
