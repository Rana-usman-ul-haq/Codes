const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const {v4: uuidv4} = require('uuid');
const Blockchain = require('./blockchain');

const nodeAddress = uuidv4().split('-').join('');


const bitcoin = new Blockchain();


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));


//this will give us a complete blockchain
app.get('/blockchain', function (req, res) {
  res.send(bitcoin);
});

//this will give us new transactions
app.post('/transaction', function (req, res) {
    const blockIndex = bitcoin.createNewTransaction(req.body.amount, req.body.sender, req.body.recipient);
    res.json({note: `This transaction will be added in block ${blockIndex}`});
  }); //calling transactions from postman body

//MINE a new block
app.get('/mine', function (req, res){

  const lastBlock = bitcoin.getLastBlock();
  const previousBlockHash = lastBlock['hash'];

  const currentBlockdata = {
  transaction: bitcoin.pendingTransactions,
  index: lastBlock['index'] + 1  //pending transaction will go in last block
}

  const nonce = bitcoin.proofOfwork(previousBlockHash, currentBlockdata);

  const blockHash = bitcoin.hashBlock(previousBlockHash,currentBlockdata, nonce);

  bitcoin.createNewTransaction(10,'000000', nodeAddress);

  const newBlock = bitcoin.createNewBlock(nonce, previousBlockHash, blockHash);
  res.json({
    note: "New Block mined Succesfully",
    block: newBlock
// what to show when block is mined
  })
})
//simple web wallet
app.get('/wallet', function (req, res) {
  res.sendFile(__dirname + "/index.html");
});

app.post('/wallet', function (req, res) {
  const blockIndex = bitcoin.createNewTransaction(req.body.amount, req.body.senderAddress, req.body.recipientAddress);
  res.json({note: `This transaction will be added in block ${blockIndex}`});
});
 

app.listen(3000, function() {
    console.log("This server is running on port 3000")
});
// res(response) data from server to client
// req(request) data from client to server
// npx nodemon file.js to use nodemon on mac
// `` used for string interpolation
// post to send data to server
// get getting data from server