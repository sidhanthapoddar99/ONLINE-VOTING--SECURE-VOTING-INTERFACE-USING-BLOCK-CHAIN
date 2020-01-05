<?php
try{
 
	$dbh= new PDO('mysql:host=localhost;dbname=voter;charset=utf8','root','');
	$dbh->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
	$hashedpassword=password_hash('poddar',PASSWORD_DEFAULT);

$q= "INSERT into voters (username,token,password,age,district,cardnumber,districtno) VALUES ('Saumya Gupta', '1', '$hashedpassword', '20','Tamil Nadu','8963217789','3')";

if($dbh->exec($q)){
   
}
else{
  echo "ERROR: Couldn't Execute";
	}
}
catch(PDOException $e)
{
	echo "Connection failed:".$e->getMessage();

}


?>