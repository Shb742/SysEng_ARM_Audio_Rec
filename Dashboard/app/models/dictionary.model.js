const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const sanitizerPlugin = require('mongo-sanitize');

const dictionarySchema = new Schema({
    content: String,
    createdAt: {type: Date, default: Date.now},
    updatedAt: {type: Date, default: Date.now}
});

dictionarySchema.plugin(sanitizerPlugin);

let Dictionary = mongoose.model('Dictionary', dictionarySchema);

module.exports = Dictionary;
