<?php
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);

    require "conecta.php";
    $con = conecta();

    $id = $_GET['id'];
    $nombre = $_POST['nombre'];
    $apellidos = $_POST['apellido'];
    $pasw = $_POST['pasw'];
    $correo = $_POST['correo'];
    $rol = $_POST['rol'];
    
    $file_name = $_FILES['archivo']['name'];
    $file_tmp = $_FILES['archivo']['tmp_name'];
    
    $sql = "SELECT * FROM empleados WHERE id = '$id'";
    $res = $con->query($sql);
    $row = $res->fetch_assoc();
    $archivo = $row['archivo'];


    if($file_name != ""){
        $arreglo = explode(".", $file_name);
        $len = count($arreglo);
        $ext = $arreglo[$len-1];
        $dir = "/Applications/XAMPP/xamppfiles/htdocs/proyecto/administradores/fotos/";
        
        $nuevo_nombre = md5_file($file_tmp) . "." . $ext;
        $ruta_destino = $dir . $nuevo_nombre;
        
        if(copy($file_tmp, $dir.$nuevo_nombre)){
            $archivo = $nuevo_nombre;
            $archivo_n = $file_name;
            $sql = "UPDATE empleados SET nombre = '$nombre', apellidos = '$apellidos', correo = '$correo', rol = '$rol', archivo_n = '$archivo_n', archivo = '$archivo' WHERE id = '$id'";
            $res = $con->query($sql);
        } else {

            echo "Error al subir el archivo.";
            exit;
        }
    } else {
        $sql = "UPDATE empleados SET nombre = '$nombre', apellidos = '$apellidos', correo = '$correo', rol = '$rol' WHERE id = '$id'";
        $res = $con->query($sql);
    }

    mysqli_close($con);

    header("Location: ../empleados_lista.php");
   

?>
