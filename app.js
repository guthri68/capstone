const express = require('express');
const mysql = require('Mysql');
const http = require('http');
const request = require('request');
const { title } = require('process');

let url ="https://api.nasa.gov/planetary/apod?api_key=VpSPFEEvHKaceHZ1BHE1wp0gEFbeDAp0ggrUKu0R";


request(url, function (err, response, body) {
    if(err){
      console.log('error:', error);
    } else {
const apod = JSON.parse(body);
const copyright = apod.copyright;
const explanation = apod.explanation;
const date = apod.date;
const title = apod.title;
const url = apod.url;
  let sql = `INSERT INTO astronomy_app.nasa(copyright, download_date, title, url, explanation) VALUES ('${copyright}', '${date}', '${title}', '${url}', "${explanation}");`;
db.query(sql, function (err, result) {
  if (err) throw err;
  console.log(`INSERTED>> \n ${sql}`);
  db.end(function(err) {
    if (err) {
      return console.log('error:' + err.message);
    }
    console.log('Closed the database connection.');
  });
});
    

//log parts of the parsed json body returned for testing
let message = `Copyright: ${apod.copyright} \n url: ${apod.url} explanation: ${apod.explanation}`;
console.log(message);
    }
});


//connection info
const db = mysql.createConnection({
    host     : 'localhost',
    user     : 'node',
    password : 'node',
    database : 'astronomy_app'
});

const app = express();
db.connect((err) =>{
    if(err){
        console.log(err);
    }
    console.log('MySQL Connected...')
});

app.listen('4000', () => {
    console.log('Server started on port 4000');
})


