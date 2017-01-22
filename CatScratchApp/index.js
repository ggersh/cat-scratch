var express = require('express'),
    bodyParser = require('body-parser'),
    mongoose = require('mongoose'),
    path = require('path'),
    pug = require('pug');

var app = express();

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'), { maxAge: 31557600000 }));
app.set('view engine', 'pug');

mongoose.connect('mongodb://admin:admin@catscratchdb-shard-00-00-pvqvd.mongodb.net:27017/catscratch?ssl=true&replicaSet=CatScratchDB-shard-0&authSource=admin');
var Tweet = mongoose.model('tweets', {
    old_tweet: String,
    profile_picture: String,
    tweet_text: String,
    screen_name: String
});

app.get('/', function(req, res) {
    Tweet.find({}, function(err, data) {
      var tweeties = data;
      tweeties[0].tweet_text.replace("}}cat{{", "🐱");
      res.render('index', {
        tweets: data
      });
    });
});

app.listen(2356, function(err) {
    console.log('Starting up NodeJS server!');
});
