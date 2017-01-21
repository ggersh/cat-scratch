module.exports = {
    "dbURL": "mongodb://admin:admin@catscratchdb-shard-00-00-pvqvd.mongodb.net:27017,catscratchdb-shard-00-01-pvqvd.mongodb.net:27017,catscratchdb-shard-00-02-pvqvd.mongodb.net:27017/admin?ssl=true&replicaSet=CatScratchDB-shard-0&authSource=admin",
    "port": process.env.PORT || 3000
}