<?php

include "../conexion/conexion.php";

if(isset($_POST['update'])){
    $nombre = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $ci = $_POST['ci'];
    $id = $_POST['id'];

    $sql = "UPDATE 'users' SET ,'nombre_users'='$nombre','apellido_users'='$apellido','ci_users'='ci' WHERE 'id_users'='$id'";

    $execute = mysqli_query($conn, $sql);

    if($execute){
        echo "Registro modificado con exito";
    }else{
        echo "Error" . $sql . "<br>" . mysqli_error($conn);
    }
}

?>