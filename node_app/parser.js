const fs = require('fs');
const csv = require('csv-parser')

/**
 * Pars
 * @returns {Promise<Array<Object>>}
 */
async function parse(){
    const parser = new Promise((resolve, reject) => {
        const results = []
        const file = fs.createReadStream("../notebook/euro_million_history.csv")

        try {
            file.pipe(csv())
            .on('data', (data) => results.push(data))
            .on('end', () => resolve(results))
        } catch (error) {
            reject(error)
        }

        
    })

    const csvParsed = await parser
    
    return csvParsed.map(row => {
        const date = row.date
        const numbers = JSON.parse(row.numbers)
        const stars = JSON.parse(row.stars)

        return {date, numbers, stars}
    })
}

module.exports = { parse }