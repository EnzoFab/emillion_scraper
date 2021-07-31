const { countBy, sampleSize, flatten, toPairs, sortBy, chunk } = require("lodash")
const { parse } = require("./parser")

/*
    Idea behind batching:
    the array of number is sorted by number of occurence of each number
    we will create several batchs to have the number which appear the least
    in one group and the one which appear the most in another group.
    Then we will randomly pick some numbers in the first group and some other in the second group
        (if we have more than 2 groups the idea will remain the same but on every groups)
*/

function getUniqueValueCount(twoDeepArray){
    const flatArray = flatten(twoDeepArray)
    const counts = countBy(flatArray)

    const asPairs = toPairs(counts).map(pair => {
        const [key, count] = pair

        return [parseInt(key), count]
    })


    return sortBy(asPairs, ([,count]) => count)
}

/**
 * 
 * @param {Array} numbers : Chuncked array of number
 * @param {number} batchSize 
 */
function pickNumber(numbers, batchSize){
    let propositionSize = 5

    const pickSize = Math.ceil(5 / batchSize)

    let pick = 0
    const picks = []

    while(propositionSize > 0){
        pick = pickSize >= propositionSize ? pickSize : propositionSize
        picks.push(pick)

        propositionSize -= pick
    }

    const numberPick = picks.map((val, index) => {
        return sampleSize(numbers[index], val)
    })


    return sortBy(flatten(numberPick))
}

async function getCounts(){
    const result = await parse()

    const numbers = getUniqueValueCount(result.map(row => row.numbers))
    const stars = getUniqueValueCount(result.map(row => row.stars))

    return { numbers, stars }
}



async function generate(quantity=1, batch=1){
    const batchSize = Math.abs(batch) < 5 ? Math.abs(batch) : 5

    const { numbers, stars: s} = await getCounts()

    const stars = s.map(([key]) => key)

    const chunkSize = Math.round(numbers.length / batchSize)

    const chunkedNumber = chunk(numbers.map(([key,]) => key), chunkSize)

    const result = []

    for(let i = 0; i < quantity; i++){
        result.push({
            numbers: pickNumber(chunkedNumber),
            stars: sortBy(sampleSize(stars, 2))
        })
    }

    return result
}

module.exports = { generate }