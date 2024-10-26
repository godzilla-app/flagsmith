const isDev = process.env.E2E_DEV;
module.exports = {
    "browsers": "firefox:headless",
    "port1": 8080,
    "port2": 8081,
    "hostname": "localhost",
    quarantineMode: false,
    skipJsErrors: true,
    selectorTimeout: 20000,
    assertionTimeout: 20000,
    cache: true,
    "videoPath": "reports/screen-captures",
    "videoOptions": {
        "singleFile": true,
        "failedOnly": true,
        "pathPattern": "./test-report-${FILE_INDEX}.mp4"
    },
    "videoEncodingOptions": {
        "r": 20,
        "aspect": "4:3"
    },
    // other settings
}
