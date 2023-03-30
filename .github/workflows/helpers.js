let fetch = null;
let core = null;
let context = null;

function setupGlobals(globals) {
    fetch = globals.fetch
    if (!fetch) throw new Error('fetch is not defined')

    core = globals.core
    if (!core) throw new Error('core is not defined')

    context = globals.context
    if (!context) throw new Error('context is not defined')
}

function sortVersions(versions) {
    return versions.map(
        a => a.replace(/\d+/g, n => +n + 100000)
    ).sort().map(
        a => a.replace(/\d+/g, n => +n - 100000)
    )
}

async function getReleaseVersions(packageName) {
    const response = await fetch(`https://pypi.org/pypi/${packageName}/json`)
    const data = await response.json()
    return Object.keys(data.releases)
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

async function extractVersions() {
    core.setOutput('stubs-version', '')
    const package = process.env.PACKAGE
    const stubsPackage = process.env.STUBS
    const force = context.payload.inputs ? context.payload.inputs.force !== 'false' : false

    if (force) {
        core.notice('Force release, skipping version check')
    }

    const inputVersion = context.payload.inputs?.version
    const version = inputVersion ? inputVersion : await getLatestVersion(package)
    core.notice(`${package} version = ${version}`)

    const stubsVersion = await getLatestStubsVersion(stubsPackage, version)
    core.notice(`${stubsPackage} latest version = ${stubsVersion}`)

    const buildStubsVersion = stubsVersion ? getNextVersion(stubsVersion) : version

    if (!force) {
        const isStubsVersionGreater = stubsVersion === null || isStableVersionGreater(buildStubsVersion, stubsVersion)
        if (!isStubsVersionGreater) {
            core.notice('Stubs version is not greater than the latest, skipping run')
            return
        }
    }

    core.notice(`New ${package} version found: ${version}`)
    core.notice(`${stubsPackage} build version = ${buildStubsVersion}`)
    core.setOutput('version', version)
    core.setOutput('stubs-version', buildStubsVersion)
}

module.exports = {
    setupGlobals,
    extractVersions
}
