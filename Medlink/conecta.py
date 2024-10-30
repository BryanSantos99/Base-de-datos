import psycopg2 as db

def conectar():
    
    try:
        conn = db.connect(
            
            host="localhost",
            database="nucleo",
            user="postgres",
            password="12345"
        )
        print("Conexión exitosa")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    return conn
