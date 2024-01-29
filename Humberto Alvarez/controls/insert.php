<?php

include "../conexion/conexion.php";

if(isset($_POST['insert'])){
    $nombre = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $ci = $_POST['ci'];

    $sql = "INSERT INTO 'users'('nombre_users', 'apellido_users', 'ci_users') VALUES ('$nombre','$apellido','ci')";

    $execute = mysqli_query($conn, $sql);

    if($execute){
        echo "Registro realizado con exito";
    }else{
        echo "Error" . $sql . "<br>" . mysqli_error($conn);
    }
}

?>