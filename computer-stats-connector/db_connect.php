<?php
 
/**
 * A class file to connect to database
 */
class DB_CONNECT {
 
    // constructor
    function __construct() {
        // connecting to database
        $this->connect();
    }
 
    // destructor
    function __destruct() {
        // closing db connection
        $this->close();
    }
 
    /**
     * Function to connect with database
     */
    function connect() {
        // import database connection variables
        require_once __DIR__ . '/db_config.php';
 
        // Connecting to mysql database
        $conn = mysqli_connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_PORT) or die(mysql_error());
 
        // returing connection cursor
        return $conn;
    }
 
    /**
     * Function to close db connection
     */
    function close() {
        // closing db connection
        mysql_close();
    }
 
}
?>