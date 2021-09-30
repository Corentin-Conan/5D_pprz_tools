const request = require('request-promise')

const AUTH_ENDPOINT = process.env.AUTH_ENDPOINT || 'auth.airmap.com'

async function authenticateServiceAccount(client_id, client_secret) {
    const options = {
        uri: `https://${AUTH_ENDPOINT}/realms/airmap/protocol/openid-connect/token`,
        method: 'POST',
        form: {
            grant_type: "client_credentials",
            client_id: client_id,
            client_secret: client_secret
        }
    }
    try {
        const response = await request(options)
        const body = JSON.parse(response)
        return body.access_token
    } catch (error) {
        throw error
    }
}

exports.authenticateServiceAccount = authenticateServiceAccount