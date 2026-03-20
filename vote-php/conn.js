const MongoClient = require('mongodb').MongoClient;
const uri ="mongodb+srv://Saumya:atmvote@cluster0-z7nfn.mongodb.net/test?retryWrites=true";
MongoClient.connect(uri, function(err, client) {
   if(err) {
        console.log('Error occurred while connecting to MongoDB Atlas...\n',err);
   }
   console.log('Connected...');
   var CryptoJS = require("crypto-js");
   cryptPassword = CryptoJS.AES.encrypt('sidhanta', '292708');
   cryptPassword2 = CryptoJS.AES.encrypt('saumya', '292708');
   cryptPassword3 = CryptoJS.AES.encrypt('vivek', '292708');
   cryptPassword4 = CryptoJS.AES.encrypt('rakshita', '292708');
   const collection = client.db("voters").collection("users");
   collection.insertOne({
   username:"Sidhanta Poddar",
   cardno:"123456789",
   age:"20",
   district:"Bengal",
   credit:"1",
   password:cryptPassword
});
   /*collection.insertOne({
   username:"Saumya Gupta",
   cardno:"589745614789",
   age:"19",
   district:"Delhi",
   credit:1,
   password:cryptPassword2
});
   collection.insertOne({
   username:"Rakshita Srivastava",
   cardno:"4789654123",
   age:"21",
   district:"Delhi",
   credit:1,
   password:cryptPassword4
});
   collection.insertOne({
   username:"Vivek",
   cardno:"127896542",
   age:"20",
   district:"Bengal",
   credit:1,
   password:cryptPassword3
});
*/
   client.close();
});

/*connection.connect(function(err) {
if(err) throw(err);
else {
console.log("connected");
var path = require ('path');
var http=require("http");
var sanitizer = require('sanitize')();
var express = require('express');
var bodyParser = require('body-parser');
var CryptoJS = require("crypto-js");
const expressValidator = require('express-validator');
var session = require('express-session');
var cookieParser = require('cookie-parser');
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(expressValidator());
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('trust proxy', 1);
app.use(cookieParser());
app.use(session({secret: '_secret_', cookie: { maxAge: 60 * 60 * 1000 }, saveUninitialized: false, resave: false})); 
app.get('/signup',function(req,res){
res.render('register.html');
}); 
var name,email,gender,phone,city,country,address,pin,password,cryptPassword;
app.post('/signup', function(req, res){
name=req.body.name;
phone=req.body.phone;
email=req.body.email;
gender=req.body.sex;
city=req.body.city;
country=req.body.country;
address=req.body.address,'array';
pin=req.body.pin;
password=req.body.password;
cryptPassword = CryptoJS.AES.encrypt(password, '292708');
req.checkBody('name').isLength({ min: 3 }).trim().escape();
req.checkBody('email').isEmail().normalizeEmail();
req.checkBody('pin').isNumeric().isLength({ min: 6, max:6}).trim().escape();
req.checkBody('phone').isNumeric().isLength({ min: 10, max:10 }).trim().escape();
req.checkBody('password').isLength({ min:8 })
    .matches('[0-9]')
    .matches('[a-z]')
    .matches('[A-Z]');
   var errors = req.validationErrors();
   if(errors){
    console.log(errors);
   }
   else{
   	var sql = "INSERT INTO users (name,email,phone,address,city,country,pin,gender,password) VALUES ('"+name+"','"+email+"','"+phone+"','"+address+"','"+city+"','"+country+"','"+pin+"','"+gender+"','"+cryptPassword+"')";
  connection.query(sql, function (err, result) {
    if (err) throw err;
    console.log("1 record inserted");
    res.redirect('/login');
   });
      
   }
});
app.get('/login',function(req,res){
res.render('login.html');
}); 
app.post('/login', function(req, res){
var matchpass,matchname,match;
matchname=req.body.name;
matchpass=req.body.password;
var sql = "select * from users where name='"+matchname+"'";
  connection.query(sql, function (err, result, fields) {
    if (err) throw (err);
    if(Object.keys(result).length === 0)
      console.log("Incorrect username or password");
    else{
      match=CryptoJS.AES.decrypt(result[0]['password'].toString(), '292708');
      match=match.toString(CryptoJS.enc.Utf8);
        if (match==matchpass){
        console.log("Signed in");
        var newUser = {name:result[0]['name'],password:match,city:result[0]['city'],country:result[0]['country'],pin:result[0]['pin'],address:result[0]['address'],email:result[0]['email'],gender:result[0]['gender']};
         req.session.user=newUser;
         }
      else
        console.log("Incorrect username or password");
    }
    
});
  
});

app.listen(3000);
}
});*/
 
