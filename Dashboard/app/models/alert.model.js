const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const sanitizerPlugin = require('mongo-sanitize');

const AlertSchema = new Schema({
    content: String,
    type: String,
    location: String,
    file: {
        type: String,
        select: false
    },
    createdAt: {
        type: Date,
        expires: '43200m',
        default: Date.now
    }
}, {
    capped: true,
    size: 1677721600,
    max: 100,
    timestamps: true
});

AlertSchema.plugin(sanitizerPlugin);

module.exports = mongoose.model('Alert', AlertSchema);
