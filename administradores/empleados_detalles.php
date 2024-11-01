<!DOCTYPE html>
<html>
<head>
    <title>Detalles del Empleado</title>
    <link rel="stylesheet" href="style/empleados_detalles.css">
    <script src="js/jquery-3.7.1.min.js"></script>
    <link rel="stylesheet" href="style/menu.css">
    <?php
        require "funciones/conecta.php";
        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);
        $id = $_GET['id'];
        $con = conecta();
        $sql = "SELECT * FROM empleados WHERE id = '$id'";
        $res = $con->query($sql);
        $row = $res->fetch_array();
        $nombre = $row['nombre'];
        $apellidos = $row['apellidos'];
        $correo = $row['correo'];
        $rol = $row['rol'];
        $archivo_n = $row['archivo'];
        $con->close();
        if($rol == 1){
            $rol = "Gerente";
        }else{
            $rol = "Empleado";
        }
    ?>

</head>
<body>
    <?php
        session_start();
    ?>
<nav id="menu">
    <h1 id="titulo">Bienvenido, <?php echo $_SESSION['nombre_usuario']; ?>!</h1>
        <ul id="menu-lista">
       
            <li class="menu-item"><a href="empleados_lista.php">Empleados</a></li>
            <li class="menu-item"><a href="#">Productos</a></li>
            <li class="menu-item"><a href="funciones/logout.php">Cerrar sesión</a></li>
        </ul>
    </nav>
    
    <div class="contenedor">
        <h1>Detalles del Empleado</h1>
        <div class="detalles">
            <p class="registros"><strong>Nombre:</strong> <?php echo $nombre; ?> <?php echo $apellidos; ?></p>
            <p class="registros"><strong>Correo:</strong> <?php echo $correo; ?></p>
            <p class="registros"><strong>Rol:</strong> <?php echo $rol; ?></p>
            <p class="registros"><strong>Foto:</strong> <img src="fotos/<?php echo $archivo_n; ?>" alt="Foto del Empleado"></p>
        </div>
        <a href="empleados_lista.php">Volver a la lista</a>
        <a id="botonInicio" href="bienvenido.php">Volver al inicio</a>
    </div>
</body>
</html>