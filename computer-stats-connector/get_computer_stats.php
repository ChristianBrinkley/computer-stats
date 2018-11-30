<?php
 
/*
 * Following code will get cpu_percent
 * cpu_percent is identified by computer_id id (id)
 */
 
// array for JSON response
$response = array();
 
// include db connect class
require_once __DIR__ . '/db_connect.php';
 
// connecting to db
$db = new DB_CONNECT();
 
// setup mysqli connector
$conn = $db->connect(); 

// check for post data
if (isset($_GET["cid"])) {
	$id = $_GET['cid'];
	
	$response['id'] = $id;
	
    // get a cpu_percent from computer_id table
    $result = mysqli_query($conn, "SELECT cpu_percent, cpu_max_percent FROM computer_id WHERE id = ('$id')");
 
    if (!empty($result)) {
        // check for empty result
        if (mysqli_num_rows($result) > 0) {
			
			$row = mysqli_fetch_assoc($result);
			
			// success
            $response["success"] = 1;
		
            // user node
			$response["cpu_percent"] = $row["cpu_percent"];
            $response["cpu_max_percent"] = $row["cpu_max_percent"];
 
            // echoing JSON response
            echo json_encode($response);
        } else {
            // no computer_id found
            $response["success"] = 0;
            $response["message"] = "No cpu_percent found";
 
            // echo no users JSON
            echo json_encode($response);
        }
    } else {
        // no computer_id found
        $response["success"] = 0;
        $response["message"] = "Empty";
 
        // echo no users JSON
        echo json_encode($response);
    }
} else {
    // required field is missing
    $response["success"] = 0;
    $response["message"] = "Required field(s) is missing";
 
    // echoing JSON response
    echo json_encode($response);
}
?>