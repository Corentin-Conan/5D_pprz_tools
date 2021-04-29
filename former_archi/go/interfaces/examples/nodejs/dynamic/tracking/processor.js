// Bootstrap our dependencies.
const grpc = require('grpc')
const auth = require('../auth')
const proto = require('../proto')

// Configure your env with your client id and client secret
const API_ENDPOINT = process.env.API_ENDPOINT || 'api.airmap.com:443'
const CLIENT_ID = process.env.CLIENT_ID
const CLIENT_SECRET = process.env.CLIENT_SECRET

function connectProcessor(token) {

  const tracking = proto.descriptors.tracking
  const collector = new tracking.Collector(API_ENDPOINT, grpc.credentials.createSsl())

  const metadata = new grpc.Metadata()
  metadata.add("authorization", "Bearer " + token)

  const client = collector.ConnectProcessor(metadata)

  client.on('data', function (response) {
    switch (response.details) {
      case "batch":
        for (let i in response.batch.tracks) {
          let track = response.batch.tracks[i]
          console.log(track.identities)
          console.log(track.position.absolute)
        }
        break
      case "status":
        console.log('received status from collector: ', response.status.level, response.status.message)
        break
    }
  })

  client.on('end', function () {
    console.log('client connection to collector ended')
  })

  client.on('error', function (error) {
    throw error
  })
}

// Login using the client credentials,
// and connect to the collector with a token
auth.authenticateServiceAccount(CLIENT_ID, CLIENT_SECRET)
  .then(connectProcessor)
  .catch(console.log)
