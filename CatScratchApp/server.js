var express = require('express');
var bodyParser = require('body-parser');
var morgan = require('morgan');
var config = require('./js/app/config');
var mongoose = require('mongoose');
var app = express();
var Schema = mongoose.Schema;
var tweetSchema = new Schema({
    username: String,
    profileLink: String,
    profilePicture: String,
    originalTweet: String,
    newTweet: String
})

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(morgan('dev'));

app.get('*', function(req, res) {
    // get <datalist>
    // render template
    res.sendFile(__dirname + 'index.html');
});

mongoose.connect(config.dbURL);

app.listen(config.port, function(err) {
    if (err) {
        console.log(err);
    } else {
        console.log("It's happening!!!");
    }
});