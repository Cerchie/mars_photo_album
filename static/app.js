// How do I import a key to keep it safe?
// How do I use these routes in other functions?
// How do I enter photo urls in my database? 

async function displayMissionInfoC() {
    resp = await axios.get(f `https://api.nasa.gov/mars-photos/api/v1/manifests/Curiosity?api_key=${APIKEY}`)
}

async function displayMissionInfoO() {
    resp = await axios.get(f `https://api.nasa.gov/mars-photos/api/v1/manifests/Opportunity?api_key=${APIKEY}`)
}

async function displayMissionInfoS() {
    resp = await axios.get(f `https://api.nasa.gov/mars-photos/api/v1/manifests/Spirit?api_key=${APIKEY}`)
}