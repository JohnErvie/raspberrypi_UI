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
    //$user_id = $_POST['user_id'];

    $power_consumption_query = "SELECT * FROM (SELECT power_consumption FROM `pc_table` WHERE rpi_id LIKE '$rpi_id' ORDER BY time DESC LIMIT 600)Var1;";

    $PC_R = mysqli_query($CN, $power_consumption_query);
    $PC_row = mysqli_fetch_all($PC_R);

    $time_query = "SELECT * FROM (SELECT time FROM `pc_table` WHERE rpi_id LIKE '$rpi_id' ORDER BY time DESC LIMIT 600)Var1 ORDER BY time ASC;";

    $Time_R = mysqli_query($CN, $time_query);
    $Time_row = mysqli_fetch_all($Time_R);

    $status_query = "SELECT * FROM (SELECT status FROM `pc_table` WHERE rpi_id LIKE '$rpi_id' ORDER BY time DESC LIMIT 600)Var1;";

    $status_R = mysqli_query($CN, $status_query);
    $status_row = mysqli_fetch_all($status_R);

    $Message = "PC Data Minutes";
    
    $Response[]=array("Message"=>$Message, "status"=>$status_row, "time"=> $Time_row,"power_consumption"=>$PC_row);
    echo json_encode($Response);
    
    //print_r($PC_row);
    //print_r($Time_row);

    mysqli_close($CN);
?>

