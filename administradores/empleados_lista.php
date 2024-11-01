<html>
<head>
    <title>Listado de empleados</title>
    <link rel="stylesheet" href="style/style.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="style/menu.css">
    <style>
        .botonCrear,
.boton,
button.boton {
  display: inline-block;
  padding: 10px 20px;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 10px;
  border: none;
  cursor: pointer;
}

.botonCrear {
  background-color: #007bff;
}

.boton,
button.boton {
  background-color: #4CAF50;
}

.boton:hover,
.botonCrear:hover,
button.boton:hover {
  opacity: 0.9;
}

.boton-editar,
button.boton-editar { 
  background-color: #2196F3; 
}
    </style>
    <script>
        function eliminarEmpleado(idEmpleado) {
            if (confirm("¿Desea eliminar el empleado con id " + idEmpleado + "?")) {
                $.ajax({
                    url: 'funciones/empleados_elimina.php',
                    type: 'POST',
                    data: { id: idEmpleado },
                    success: function(response) {
                    if (response == 1) {
                        alert("Empleado eliminado correctamente.");
                        $("#empleado-" + idEmpleado).hide();
                    } else {
                        alert("No se pudo eliminar al empleado.");
                    }
                },
                error: function() {
                    alert("Hubo un error al intentar eliminar al empleado.");
                    console.log(error);
                }
                });
            }
        }
        function editarEmpleado(idEmpleado) {
            window.location.href = 'empleados_edita.php?id=' + idEmpleado;
        }
        function verEmpleado(idEmpleado) {
            window.location.href = 'empleados_detalles.php?id=' + idEmpleado;
        }
    </script>
</head>
<body>
    <?php
        session_start();
        if (!isset($_SESSION['correo'])) {
            header('Location: index.php');
            exit();
        }

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
        <?php
    
            require "funciones/conecta.php";
            $con = conecta();
            $sql = "SELECT * FROM empleados WHERE eliminado = 0";
            $res = $con->query($sql);
            $cantidad_empleados = $res->num_rows;
        ?>
        <h1>Listado de empleados (<?php echo $cantidad_empleados; ?>)</h1>
        
        <div class="tabla">
            <table>
                <div id="registros">
                    <tr>
                        <th>ID</th>
                        <th>Nombre completo</th>
                        <th>Correo</th>
                        <th>Rol</th>
                        <th>Ver detalle</th>
                        <th>Editar</th>
                        <th>Eliminar</th>
                    </tr>
                </div>
                <div id="tuplas">
                    <?php
                        
                        while ($row = $res->fetch_array()) {
                            $id = $row["id"];
                            $nombre = $row["nombre"];
                            $apellidos = $row["apellidos"];
                            $correo = $row["correo"];
                            $rol = $row["rol"] == 1 ? "Gerente" : "Ejecutivo";  
                            echo '<tr  id="empleado-'.$id.'">';
                            echo "<td>$id</td>";
                            echo "<td>$nombre $apellidos</td>";
                            echo "<td>$correo</td>";
                            echo "<td>$rol</td>";
                            echo '<td><button class="boton" onclick="verEmpleado(' . $id . ')">Ver Detalles</button></td>'; 
                            echo '<td><button class="boton boton-editar" onclick="editarEmpleado(' . $id . ')">Editar Registro</button></td>';
                            echo '<td><button class="boton boton-eliminar" onclick="eliminarEmpleado(' . $id . ')">Eliminar Registro</button></td>';
                            echo "</tr>";
                        }
                    ?>
                </div>
            </table>
            <div class="registro">
            <a href="empleados_alta.php" class="botonCrear">Crear nuevo registro</a>
            <a href="bienvenido.php" class="botonCrear">Volver al inicio</a>
        </div>
        </div>
    </div>
</body>
</html>
