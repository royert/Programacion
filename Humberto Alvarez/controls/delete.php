<?php

include "../conexion/conexion.php";

if(isset($_POST['delete'])){
    $id = $_GET['id'];

    $sql = "DELETE FROM 'users' WHERE 'id_users' = $id";

    $execute = mysqli_query($conn, $sql);

    if($execute){
        echo "Registro eliminado con exito";
    }else{
        echo "Error" . $sql . "<br>" . mysqli_error($conn);
    }
}

?>