  <?php   
    
    require 'html_practica.php';

    $nombre = $_POST['nombre'];
    $edad = $_POST['edad'];

    if ($isset($_POST['edad'])) {
        echo 'su edad es', $edad; 
    }  
    ?>