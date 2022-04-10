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

    $data_query = "SELECT * FROM (SELECT datetime, power_consumption, status  FROM `pc_table` WHERE rpi_id LIKE '$rpi_id' ORDER BY time DESC LIMIT 1)Var1;";

    $data_R = mysqli_query($CN, $data_query);
    $data_row = mysqli_fetch_all($data_R);

    $Message = "PC Data";
    
    $Response[]=array("Message"=>$Message, "data"=> $data_row);
    echo json_encode($Response);
    

    mysqli_close($CN);
?>
