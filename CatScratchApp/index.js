var express = require('express'),
    bodyParser = require('body-parser'),
    mongoose = require('mongoose'),
    pug = require('pug');

var app = express();

app.use(bodyParser.json());
app.set('view engine', 'pug');

mongoose.connect('mongodb://admin:admin@catscratchdb-shard-00-00-pvqvd.mongodb.net:27017/catscratch?ssl=true&replicaSet=CatScratchDB-shard-0&authSource=admin');
var Tweet = mongoose.model('tweets', {
    text: String
});

app.get('/', function(req, res) {
    Tweet.find({}).select('text').exec(function(err, data) {
        console.log(data);
    });
    res.render('index', {
        tweets: data[0].text
    });
});

app.listen(2356, function(err) {
    console.log('Starting up NodeJS server!');
});