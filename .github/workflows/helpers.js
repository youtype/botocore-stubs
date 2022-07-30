const https = require('https')

function sortVersions(versions) {
    return versions.map(
        a => a.replace(/\d+/g, n => +n + 100000)
    ).sort().map(
        a => a.replace(/\d+/g, n => +n - 100000)
    )
}

async function getReleaseVersions(packageName) {
    const options = {
        hostname: 'pypi.org',
        port: 443,
        path: `/pypi/${packageName}/json`,
        method: 'GET'
    }

    return new Promise((resolve, reject) => {
        const req = https.request(options, res => {
            if (res.statusCode < 200 || res.statusCode >= 300) {
                return reject(new Error(`Status Code: ${res.statusCode}`))
            }
            const data = []
            res.on("data", chunk => data.push(chunk))
            res.on("end", () => {
                const response = JSON.parse(Buffer.concat(data).toString())
                resolve(Object.keys(response.releases))
            })
        })
        req.on("error", reject)
        req.end()
    })
}

async function getLatestVersion(package) {
    const versions = await getReleaseVersions(package)
    return sortVersions(versions).pop()
}

function isVersionGreater(version, other) {
    const versionStable = version.split('.').slice(0, 3).join(".")
    const otherStable = other.split('.').slice(0, 3).join(".")
    const latestStable = sortVersions([versionStable, otherStable]).pop()
    return latestStable !== otherStable
}

async function extractVersions({ core, context }) {
    core.setOutput('version', '')

    const botocoreVersion = await getLatestVersion('botocore')
    core.info(`Botocore version = ${botocoreVersion}`)

    const botocoreStubsVersion = await getLatestVersion('botocore-stubs')
    core.info(`Botocore-stubs version = ${botocoreStubsVersion}`)

    if (isVersionGreater(botocoreVersion, botocoreStubsVersion)) {
        core.info(`New version found: ${botocoreVersion}`)
        core.setOutput('version', botocoreVersion)
    }
}

module.exports = {
    getLatestVersion,
    isVersionGreater,
}
