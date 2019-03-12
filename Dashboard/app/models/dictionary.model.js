const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const sanitizerPlugin = require('mongo-sanitize');

const dictionarySchema = new Schema({
    content: { type:String, default:'help me /1e-21/\nhelp help /1e-25/\nsomeone help /1e-37/\nsomebody help /1e-30/\n'},
    createdAt: {type: Date, default: Date.now},
    updatedAt: {type: Date, default: Date.now}
});

dictionarySchema.plugin(sanitizerPlugin);

let Dictionary = mongoose.model('Dictionary', dictionarySchema);

module.exports = Dictionary;
