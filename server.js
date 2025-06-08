const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
app.use(bodyParser.json(), bodyParser.urlencoded({ extended: true }));

const rawData = fs.readFileSync('data.json');
const jsonData = JSON.parse(rawData);
const Map = Object.assign({}, ...jsonData);

app.get('/', (req, res) => {
    let { from, to, amount } = req.query;
    from = from.toUpperCase();
    to = to.toUpperCase();
    amount = parseFloat(amount);

    if (!Map[from] || !Map[to]) {
        return res.status(400).send('Invalid currency code');
    }

    let fromVal = Map[from];
    let toVal = Map[to];

    let temp = amount * fromVal;
    let convertedAmount = temp / toVal;

    res.status(200).json({ val: convertedAmount });
});

app.post('/update-json', (req, res) => {
    const jsonData = req.body;
    const filePath = 'data.json';
    fs.writeFile(filePath, JSON.stringify(jsonData, null, 2), (err) => {
        if (err) {
            console.error('Error writing to file:', err);
            return res.status(500).send('Error writing to file');
        }
        console.log('JSON data updated successfully');
        res.send('JSON data updated successfully');
    });
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
