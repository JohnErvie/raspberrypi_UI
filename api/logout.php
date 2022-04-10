<?php
    $CN=mysqli_connect("localhost", "admin", "password");
    $DB=mysqli_select_db($CN, "pd_database");

    // Check connection
    if (mysqli_connect_errno()){
      echo "Failed to connect to MySQL: " . mysqli_connect_error();
    }

    $EncodedData = file_get_contents('php://input');
    $DecodedData = json_decode($EncodedData, true);

    $rpi_id = $DecodedData['rpi_id'];

    $update_query = "UPDATE raspberrypi SET status='not_connected' WHERE rpi_id LIKE '$rpi_id'";
    $R = mysqli_query($CN, $update_query);

    if($R){
        //$update_query = "UPDATE raspberrypi SET status='not active' WHERE ip_address LIKE '$ip_address'";
        //mysqli_query($CN, $update_query);

        $Message = "User Logout";

        $search_query = "SELECT * FROM raspberrypi WHERE rpi_id LIKE '$rpi_id'";
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
