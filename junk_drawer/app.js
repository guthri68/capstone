const express = require('express');
const mysql = require('Mysql');

//connection info
const db = mysql.createConnection({
    host     : 'localhost',
    user     : 'node',
    password : 'node',
    database : 'nodemysql'
});

//connect to DB
db.connect((err) =>{
    if(err){
        console.log(err);
    }
    console.log('MySQL Connected...')
});

const app = express();

//Route for DB
app.get('/createdb', (req, res) =>{
    let sql = 'CREATE DATABASE nodemysql';
    db.query(sql, (err, result) =>{
        if (err) console.log(err);
        console.log(result, err);
        res.send('<p>Database created...</p>');
    });
});

app.get('/createpoststable', (req, res) =>{
    let sql = 'CREATE TABLE posts(id int AUTO_INCREMENT, title VARCHAR(255), body VARCHAR(255), PRIMARY KEY (id))';
    db.query(sql, (err, result) =>{
        if(err) throw err;
        console.log(result);
        res.send('Posts table created...');
    });
});

app.get('/addpostFinal', (req, res) =>{
    let post = {title:'Post Final', body: 'this is the final post'};
    let sql = 'INSERT INTO posts SET ?';
    let query = db.query(sql, post, (err, result) =>{
        if(err) throw err;
        console.log(result);
        res.send('Post final added...');
    });
});

app.get('/addpost2', (req, res) =>{
    let post = {title:'Post two', body: 'this is post number two'};
    let sql = 'INSERT INTO posts SET ?';
    let query = db.query(sql, post, (err, result) =>{
        if(err) throw err;
        console.log(result);
        res.send('Post two added...');

    });
});

//select post from db
app.get('/getposts', (req, res) =>{
    let sql = 'SELECT * FROM posts';
    let query = db.query(sql, (err, results) =>{
        if(err) throw err;
        console.log(results);
        res.send('Posts fetched...');

    });
});

//select single post from db
app.get('/getpost/:id', (req, res) =>{
    let sql = `SELECT * FROM posts WHERE id = ${req.params.id}`;
    let query = db.query(sql, (err, result) =>{
        if(err) throw err;
        console.log(result);
        res.send('Post fetched...');

    });
});

// update post
app.get('/updatepost/:id', (req, res) =>{
    let newTitle = '"Updated Title"';
    let sql = `UPDATE posts SET title = ${newTitle} WHERE id = ${req.params.id}`;
    let query = db.query(sql, (err, result) =>{
        if(err) throw err;
        console.log(result);
        res.send('Post updated...');

    });
});

// Delete post
app.get('/deletepost/:id', (req, res) =>{
    //let newTitle = '"Updated Title"';
    let sql = `DELETE FROM posts WHERE id = ${req.params.id}`;
    let query = db.query(sql, (err, result) =>{
        if(err) throw err;
        console.log(result);
        res.send('Post deleted...');

    });
});

app.listen('4000', () => {
    console.log('Server started on port 4000');  
})