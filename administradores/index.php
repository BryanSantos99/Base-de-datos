<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administrador</title>
    <link rel="stylesheet" href="style/inde.css">
    <script src="js/jquery-3.7.1.min.js"></script>
    <script>
      function mensaje() {
        var correo = document.forma01.correo.value;
        var pass = document.forma01.pass.value;

        if (correo == "" || pass == "") {
          $('#mensaje').html('Faltan campos por llenar').show();
                setTimeout(function() {
                  $('#mensaje').html('').hide();
                }, 5000);;
        } else {
          $.ajax({
            url: 'funciones/validaEmpleado.php',
            type: 'post',
            dataType: 'text',
            data: { correo: correo, pass: pass },
            success: function(res) {
              console.log(res);
              if (res == 1) {
                window.location.href = 'bienvenido.php';
              } else {
                $('#mensaje').html('Datos incorrectos').show();
                setTimeout(function() {
                  $('#mensaje').html('').hide();
                }, 5000);
              }
            },
            error: function() {
              console.log("error");
              $('#mensaje').html('Error archivo no encontrado').show();
              setTimeout(function() {
                $('#mensaje').html('').hide();
              }, 5000);
            }
          });
        }
      }
    </script>
  </head>
  <body>
    <form name="forma01" method="post">
      <h1>Iniciar sesión</h1><br><br>
      <input type="text" name="correo" id="correo" placeholder="Escribe tu correo"/><br />
      <input type="password" name="pass" id="pass" placeholder="Escribe tu password"/><br />
      <br />
      <input onclick="mensaje(); return false;" type="submit" value="Enviar" />
      <div id="mensaje"></div>
  </body>
</html>
