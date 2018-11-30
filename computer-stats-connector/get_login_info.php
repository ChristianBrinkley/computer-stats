<?php
 
/*
 * Following code will get single computer_id details
 * A computer_id is identified by computer_id computer_name and verified by computer_id password
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
if (isset($_POST["computer_name"]) && isset($_POST["password"])) {
    $computer_name = mysqli_real_escape_string($conn, $_POST['computer_name']);
	$password = $_POST['password'];
	
    // get a computer_id from computer_id table
    $result = mysqli_query($conn, "SELECT id, computer_name, password FROM computer_id WHERE computer_name = ('$computer_name')"); 	
	
    if (!empty($result)) {
        // check for empty result
        if (mysqli_num_rows($result) > 0) {
			$row = mysqli_fetch_assoc($result);
			$hashed_password = $row['password'];
			// verifying password
			if(hash_equals($hashed_password, crypt($password, $hashed_password))) {				
				// success
				$response["success"] = 1;
				$response['cid'] = $row['id'];
	 
				// echoing JSON response
				echo json_encode($response);
			} else {
				// password doesn't match
				$response["success"] = 0;
				$response["message"] = "Username or Password is incorrect";
 
				// echo no users JSON
				echo json_encode($response);
			}
        } else {
            // username doesn't match
            $response["success"] = 0;
            $response["message"] = "Username or Password is incorrect";
 
            // echo no users JSON
            echo json_encode($response);
        }
    } else {
        // no computer_id found
        $response["success"] = 0;
        $response["message"] = "Database error";
 
        // echo no users JSON
        echo json_encode($response);
    }
} else {
    // required field is missing
    $response["success"] = 0;
    $response["message"] = "Required field(s) are missing";
 
    // echoing JSON response
    echo json_encode($response);
}
?>