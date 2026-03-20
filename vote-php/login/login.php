<?php
session_start();
try{
	$dbh= new PDO('mysql:host=localhost;dbname=voter;charset=utf8','root','');
	$dbh->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
	$stmt=$dbh->query("SELECT * FROM vote");
    $results=$stmt->fetchAll(PDO::FETCH_ASSOC);
    //$name = ($_POST["username"]);
    //$userpassword=($_POST['pass']);
      $KEYCODE=($_POST["username"]);
  $k=0;  

  foreach($results as $row)
  {
  	//$username=htmlentities($row['ID']);
  	$password=htmlentities($row['KEYCODE']);
  	// $district=htmlentities($row['district']);
  	$token=htmlentities($row['voted']);
    if($KEYCODE==$password)
    {
    // if($userpassword==$password)
    // {
        //if($username==$name)
        //{
          $k=1;
          if($token==1)
            {           $_SESSION['token']=$token;
                        $_SESSION['password']=$password;    
                        //$_SESSION['username']=$username;
                        $_SESSION['status']="active";
                        
                        $stmt2=$dbh->query("UPDATE vote set voted=0 where KEYCODE='$password'");
                        // $stmt=$dbh->query("SELECT * FROM district where districtno=$districtno");
                        // $results2=$stmt->fetchAll(PDO::FETCH_ASSOC);
                        // foreach($results2 as $row2){
                        //    $portno=htmlentities($row2['portno']);
                        // }
                        // header("Location:http://localhost:$portno");
                        header("Location:http://localhost:3000");
                        }
          else 
          {
            echo "already voted";
          }
          break;

        	}
      //}
    }
  if($k==0)
  	{
  		echo"Invalid Username or Password";	
  	}
}
catch(PDOException $e)
{
	echo "Connection failed:".$e->getMessage();
}

?>
