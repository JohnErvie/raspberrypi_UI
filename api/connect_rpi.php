<?php
    $CN=mysqli_connect("localhost", "admin", "password");
    $DB=mysqli_select_db($CN, "pd_database");

    // Check connection
    if (mysqli_connect_errno()){
      echo "Failed to connect to MySQL: " . mysqli_connect_error();
    }

    $EncodedData = file_get_contents('php://input');
    $DecodedData = json_decode($EncodedData, true);

    $ip_address = $DecodedData['ip_address'];
    $password = $DecodedData['password'];

    $search_query = "SELECT * FROM raspberrypi WHERE ip_address LIKE '$ip_address' AND password LIKE '$password'";

    $R = mysqli_query($CN, $search_query);
    $row = mysqli_fetch_array($R);

    if(is_null($row)){
        $Message = "Invalid Ip Address of the Raspberry Pi.";
        $Data = $row;
        $Response[]=array("Message"=>$Message, "Data"=>$Data);
        echo json_encode($Response);
    }
    else{
        $update_query = "UPDATE raspberrypi SET status='connected' WHERE ip_address LIKE '$ip_address'";
        mysqli_query($CN, $update_query);

        $search_query = "SELECT * FROM raspberrypi WHERE ip_address LIKE '$ip_address'";
        $R = mysqli_query($CN, $search_query);
        $row = mysqli_fetch_array($R);

        $Data = $row;
        $Message = "Successfully connected";
        $Response[]=array("Message"=>$Message, "Data"=>$Data);
        echo json_encode($Response);
    }

    mysqli_close($CN);
?>
