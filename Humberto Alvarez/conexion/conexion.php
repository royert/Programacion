<?php
$host = 'localhost';
$database = 'id21831375_diablos_bd
';
$user = 'id21831375_royert
';
$password = 'Roger26768416*';

$conn =  mysqli_connect($host, $user, $password, $database);

if(!$conn){
    die('Conexion fallida: ' . mysqli_connect_error());
}else {
    echo ('Conexion satisfactoria');
}

?>