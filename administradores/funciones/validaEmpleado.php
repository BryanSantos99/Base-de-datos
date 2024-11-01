<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require "conecta.php";
$con = conecta();

$ban = 0;
$correo = $_REQUEST['correo'];
$pass = $_REQUEST['pass'];
$pass_enc = md5($pass);

$sql = "SELECT * FROM empleados WHERE correo = '$correo' AND pass='$pass_enc'";
$res = $con->query($sql);
$num = $res->num_rows;

if ($num > 0) {
    session_start();
    $usuario = $res->fetch_array();

    $_SESSION['correo'] = $usuario['correo'];
    $_SESSION['nombre_usuario'] = $usuario['nombre'];

    $ban = 1;
    echo "$ban";
} else {
    echo "$ban";
}

mysqli_close($con);
?>
