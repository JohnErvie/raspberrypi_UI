<?php
    $CN=mysqli_connect("localhost", "admin", "password");
    $DB=mysqli_select_db($CN, "pd_database");

    $EncodedData = file_get_contents('php://input');
    $DecodedData = json_decode($EncodedData, true);

    $email = $DecodedData['email'];
    $name = $DecodedData['name'];
    $password = $DecodedData['password'];

    $insert_query = "insert into users(email,name,password, status, ip_address, rpi_status) values('$email', '$name', '$password', 'login', '', '')";

    $R = mysqli_query($CN, $insert_query);

    if($R){
        $Message = "User has been registered successfully";

        $search_query = "SELECT * FROM users WHERE email LIKE '$email' AND password LIKE '$password'";
        $R = mysqli_query($CN, $search_query);
        $row = mysqli_fetch_array($R);

        $Data = $row;
        $Response[]=array("Data"=>$Data, "Message"=> $Message);
        echo json_encode($Response);

    }
    else{
        $Message = "Server Error... Please try later";
        $Response[]=array("Message"=>$Message);
        echo json_encode($Response);
    }

    mysqli_close($CN);

?>
