<?php
    $CN=mysqli_connect("localhost", "admin", "password");
    $DB=mysqli_select_db($CN, "pd_database");

    // Check connection
    if (mysqli_connect_errno()){
      echo "Failed to connect to MySQL: " . mysqli_connect_error();
    }

    $EncodedData = file_get_contents('php://input');
    $DecodedData = json_decode($EncodedData, true);

    $email = $DecodedData['email'];
    $password = $DecodedData['password'];

    $search_query = "SELECT * FROM users WHERE email LIKE '$email' AND password LIKE '$password'";

    $R = mysqli_query($CN, $search_query);
    $row = mysqli_fetch_array($R);

    if(is_null($row)){
        $Message = "Invalid Email or Password. Please try again.";
        $Data = $row;
        $Response[]=array("Message"=>$Message, "Data"=>$Data);
        echo json_encode($Response);
    }
    else{
        $Data = $row;
        $Message = "Successfully login";
        $Response[]=array("Message"=>$Message, "Data"=>$Data);
        echo json_encode($Response);
    }

    mysqli_close($CN);
?>