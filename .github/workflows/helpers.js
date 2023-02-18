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
            res.on('data', chunk => data.push(chunk))
            res.on('end', () => {
                const response = JSON.parse(Buffer.concat(data).toString())
                resolve(Object.keys(response.releases))
            })
        })
        req.on('error', reject)
        req.end()
    })
}

async function getLatestVersion(package) {
    const versions = await getReleaseVersions(package)
    return sortVersions(versions).pop()
}

function isVersionGreater(version, other) {
    const latest = sortVersions([version, other]).pop()
    return latest !== other
}

function getStableVersion(version) {
    return version.split('.').slice(0, 3).join('.')
}

function isStableVersionGreater(version, other) {
    return isVersionGreater(getStableVersion(version), getStableVersion(other))
}

async function getLatestStubsVersion(stubsPackage, version) {
    const versions = await getReleaseVersions(stubsPackage)
    const stableVersion = getStableVersion(version)
    const stubsVersions = versions.filter(x => x.startsWith(stableVersion))
    if (!stubsVersions.length) return null
    return sortVersions(stubsVersions).pop()
}

function getNextVersion(version) {
    if (!version.includes('.post')) return `${version}.post1`
    const [stableVersion, post] = version.split('.post', 2)
    return `${stableVersion}.post${parseInt(post, 10) + 1}`
}

module.exports = {
    getLatestVersion,
    isVersionGreater,
    getStableVersion,
    isStableVersionGreater,
    getLatestStubsVersion,
    getNextVersion
}
