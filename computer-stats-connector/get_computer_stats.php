<?php
 
/*
 * Following code will get all stats
 * stats are identified by user cid (cid)
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
	$cid = $_GET['cid'];
	
	$response['cid'] = $cid;
	
    // get all from stats table
    $userResult = mysqli_query($conn, "SELECT * FROM user WHERE cid = ('$cid')");
	$statsResult = mysqli_query($conn, "SELECT * FROM stats WHERE cid =('$cid')");
	$disksResult = mysqli_query($conn, "SELECT * FROM disks WHERE cid =('$cid')");
 
    if (!empty($userResult)) {
        // check for empty result
        if (mysqli_num_rows($userResult) > 0) {
			// fetch data
			$userRow = mysqli_fetch_assoc($userResult);
			$statsRow = mysqli_fetch_assoc($statsResult);
			
            // start building response
			$response["tracking_all_stats"] = $userRow["tracking_all_stats"];
			$response["tracking_cpu"] = $userRow["tracking_cpu"];
			$response["tracking_memory"] = $userRow["tracking_memory"];
			$response["tracking_disk"] = $userRow["tracking_disk"];
			
			// check if tracker is running
			if ($userRow["tracking_all_stats"] == 1) {
				// add boot time and computer user to response
				$response["system_boot_time"] = $statsRow["system_boot_time"];
				$response["computer_user"] = $statsRow["computer_user"];
					
				// check if tracking cpu
				if ($userRow["tracking_cpu"] == 1) {
					$response["cpu_percent"] = $statsRow["cpu_percent"];
					$response["cpu_max_percent"] = $statsRow["cpu_max_percent"];
					$response["cpu_count_physical"] = $statsRow["cpu_count_physical"];
					$response["cpu_count_logical"] = $statsRow["cpu_count_logical"];
					$response["cpu_frequency"] = $statsRow["cpu_frequency"];
				}
				
				// check if tracking memory
				if ($userRow["tracking_memory"] == 1) {
					$response["memory_total"] = $statsRow["memory_total"];
					$response["memory_available"] = $statsRow["memory_available"];
					$response["memory_used"] = $statsRow["memory_used"];
					$response["memory_percent"] = $statsRow["memory_percent"];
				}
				
				// check if tracking disk
				if ($usrRow["tracking_disk"] == 1) {
					
				}
				//stats have been tracked
				$response["success"] = 1;
				// echo JSON response
				echo json_encode($response);
			} else { 
				// stats tracker is not currently running
				$response["success"] = 1;
				// echo JSON response
				echo json_encode($response);
			}
        } else {
            // no stats found
            $response["success"] = 0;
            $response["message"] = "No stats found";
 
            // echo no users JSON
            echo json_encode($response);
        }
    } else {
        // no stats found
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