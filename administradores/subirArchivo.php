<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=<device-width>, initial-scale=1.0">
    <title>Subir archivo</title>
</head>
<body>
    <form enctype="multipart/form-data" action="funciones/salvaArchivo.php" method="post">
        <input type="file" id="archivo" name="archivo"><br><br>
        <input type="submit" value="Subir archivo" name="submit">
    </form>
</body>
</html>