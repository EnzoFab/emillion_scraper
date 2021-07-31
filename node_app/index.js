const inquirer = require("inquirer")
const { generate } = require("./generator")

const questions = {
    QUANTITY: {
        name: "quantity",
        type: "number",
        message: "How many euromillion propositions do you wan to generate ?"
    },
    BATCH_SIZE: {
        name: "batch",
        type: "number",
        message: "What is the batch size (default 1 - max 5)?",
        default: 1
    }
}


inquirer
    .prompt([questions.QUANTITY, questions.BATCH_SIZE])
    .then(async (answer) => {
        const { quantity, batch } = answer

        const result = await generate(quantity, batch)

        console.log("Proposition:\n")

        result.forEach(prop => {
            console.log(`N° [${prop.numbers.join(', ')}] ★ [${prop.stars.join(', ')}]`)
        })
    })