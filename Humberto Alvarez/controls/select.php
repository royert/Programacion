<?php

include "../conexion/conexion.php";

$data = array();

    $sql = "SELECT * FROM 'users'";

    $execute = mysqli_query($conn, $sql);

    while($row == mysqli_fetch_assoc($execute)){
    $data[] = $row;
    }
echo json_encode($data);
?>