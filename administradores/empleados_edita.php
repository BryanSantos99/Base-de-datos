<!DOCTYPE html>
<html lang="es">
<?php

    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);

    require "funciones/conecta.php";
    $con = conecta();

    $id = $_GET['id']; 

    $sql = "SELECT * FROM empleados WHERE id = '$id'";
    $res = $con->query($sql);
    $row = $res->fetch_array();

    $nombre = $row['nombre'];
    $apellidos = $row['apellidos'];
    $correo = $row['correo'];
    $rol = $row['rol'];
    $archivo = $row['archivo'] ?? '';
    $pasw = md5($row['pass']);

    mysqli_close($con);

?>
<head>
    <meta charset="UTF-8">
    <title>Empleado_Edita</title>
    <link rel="stylesheet" href="style/empleados_alta.css">
    <script src="js/jquery-3.7.1.min.js"></script>
    <link rel="stylesheet" href="style/menu.css">
   
    <script>
        function recibe() {
            var nombre = $('#nombre').val();
            var apellidos = $('#apellido').val();
            var correo = $('#correo').val();
            var pasw = $('#pasw').val();
            var rol = $('#rol').val();
            var archivo = $('#archivo').val();


            $('#mensaje').show();
            if (nombre === "" || apellidos === "" || correo === "" || rol === "0") {
                console.log("Faltan campos");
                $('#mensaje').html('Faltan Campos Por Llenar');
                setTimeout(function () {
                    $('#mensaje').html('');
                    $('#mensaje').hide();
                }, 5000);
            } else {
                console.log("Enviando formulario");
                document.getElementById('form01').submit();
            }
        }

        function correoAjax() {
            var correoA = $('#correo').val();

            $.ajax({
                url: 'funciones/correoAjax.php',
                type: 'post',
                dataType: 'text',
                data: 'correo=' + correoA,
                success: function (res) {
                    console.log(res);
                    $('#mensajeCorreo').show();
                    if (res == 1) {
                        $('#mensajeCorreo').html('Correo ' + correoA + ' Ya Registrado ');
                        setTimeout(function () {
                            $('#mensajeCorreo').html('');
                            $('#mensajeCorreo').hide();
                        }, 5000);
                        $('#correo').val('');
                    } else {
                        $('#mensajeCorreo').hide();
                    }
                },
                error: function (res) {
                    console.log("Error en el sistema");
                    $('#mensajeCorreo').html('Error en el sistema');
                    setTimeout(function () {
                        $('#mensajeCorreo').html('');
                        $('#mensajeCorreo').hide();
                    }, 5000);
                }
            });
        }
    </script>
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
    
    <div id="contenedorPrincipal">
        <h1>Formulario Editar Empleado</h1>
        <div id="formulario">
            <form id="form01" method="POST" action="funciones/emplados_update.php?id=<?php echo $id; ?>" enctype="multipart/form-data">
                <label for="nombre">Nombres:</label><br>
                <input type="text" id="nombre" name="nombre" class="campos" placeholder="Ingresa tu Nombre" value="<?php echo $nombre; ?>"><br>

                <label for="apellido">Apellidos:</label><br>
                <input type="text" id="apellido" name="apellido" class="campos" placeholder="Ingresa tus Apellidos" value="<?php echo $apellidos; ?>"><br>

                <label for="correo">Correo:</label><br>
                <input type="email" id="correo" name="correo" class="campos" placeholder="Escribe tu correo"
                    onblur="correoAjax()" value="<?php echo $correo; ?>"><br>

                <div id="mensajeCorreo"></div>

                <label for="pasw">Contraseña:</label><br>
                <input type="password" id="pasw" name="pasw" class="campos" placeholder="Ingresa la contraseña" value="<?php echo $pasw; ?>"><br>

                <label for="archivo">Archivo actual:</label><br>
            
                <img src="fotos/<?php echo $archivo; ?>" alt="Imagen actual" style="max-width: 200px;"><br>
        
                
                <label for="archivo">Cambiar archivo:</label><br>
                <input type="file" id="archivo" name="archivo" accept="image/*"><br><br>

                <label for="rol">Rol:</label><br>
                    <select name="rol" id="rol" class="campos">
                    <option value="<?php echo $rol; ?>" selected><?php  if($rol == 0) echo "Selecciona"; if($rol == 1) echo "Gerente"; if($rol == 2) echo "Ejecutivo";?></option>
                    <option value="1">Gerente</option>
                    <option value="2">Ejecutivo</option>
                </select><br>

                <input type="button" id="enviarBoton" value="Enviar" onclick="recibe();">
                <div id="mensaje"></div>
            </form>
        </div>
        <button id="regresarBoton" onClick="window.location.href='empleados_lista.php'">Regresar</button>
        <a id="botonInicio" href="bienvenido.php">Volver al inicio</a>
    </div>
</body>

</html>
