<?php

$hashed_password = '$5$rounds=535000$v2ocuy//h2CrS2HE$TJNibh2YnkbNoNv8TXXCg0uxXFLAMcOTEJax4L8O4k1'; // let the salt be automatically generated

/* You should pass the entire results of crypt() as the salt for comparing a
   password, to avoid problems when different hashing algorithms are used. (As
   it says above, standard DES-based password hashing uses a 2-character salt,
   but MD5-based hashing uses 12.) */
$user_input = 'password';

if (hash_equals($hashed_password, crypt($user_input, $hashed_password))) {
	echo "Password verified!";
} else {
	echo "Password incorrect!";
}
?>