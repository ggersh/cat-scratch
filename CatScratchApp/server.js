var express = require('express');
var bodyParser = require('body-parser');
var morgan = require('morgan');
var config = require('./js/config');
var mongoose = require('mongoose');
const pug = require('pug');
var app = express();
var Schema = mongoose.Schema;
var tweetSchema = new Schema({
    _id: Schema.Types.ObjectId,
    tweet_text1: String
})
var example = mongoose.model("example", tweetSchema);

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(morgan('dev'));
app.set('view engine', 'pug');

app.get('/', function(req, res) {
    example.find({}, 'username', function(err, data) {
        if (err) {
            console.log(err);
        } else {
            console.log(data);
        }
    });
    res.render('index', {

    });
});

mongoose.connect(config.dbURL);

app.listen(config.port, function(err) {
    if (err) {
        console.log(err);
    } else {
        console.log("It's happening!!!");
    }
});