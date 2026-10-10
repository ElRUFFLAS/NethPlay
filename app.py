import psycopg2
import bcrypt

# Configuración de la conexión para el proyecto nethplay
DB_CONFIG = {
    "host": "127.0.0.1",       # O 'localhost'
    "database": "nethplay",     # Nombre de la base de datos existente
    "user": "postgres",         # Tu usuario de PostgreSQL
    "password": "tu_contraseña", # Tu contraseña de PostgreSQL
    "port": "5432"
}

def conectar_db():
    """Establece y devuelve la conexión a la base de datos nethplay."""
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        return conexion
    except Exception as error:
        print(f"❌ Error al conectar a la base de datos: {error}")
        return None

def registrar_usuario(email, password):
    """Registra un nuevo usuario cifrando su contraseña."""
    conexion = conectar_db()
    if not conexion:
        return

    cursor = conexion.cursor()
    try:
        # 1. Generar el hash de la contraseña de forma segura con bcrypt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        # 2. Insertar en la tabla usuarios de nethplay
        query = "INSERT INTO usuarios (email, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (email, hashed.decode('utf-8')))
        conexion.commit()
        print(f"✅ ¡Usuario {email} registrado con éxito en nethplay!")
        
    except psycopg2.errors.UniqueViolation:
        print(f"⚠️ El correo {email} ya está registrado en el sistema.")
        conexion.rollback()
    except Exception as error:
        print(f"❌ Error al registrar: {error}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()

def login_usuario(email, password):
    """Valida las credenciales de un usuario existente para el login."""
    conexion = conectar_db()
    if not conexion:
        return False

    cursor = conexion.cursor()
    try:
        # 1. Buscar al usuario por correo en la base de datos
        query = "SELECT id, password_hash FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        resultado = cursor.fetchone()

        if not resultado:
            print("❌ Credenciales incorrectas (Usuario no encontrado).")
            return False

        user_id, stored_hash = resultado

        # 2. Verificar la contraseña ingresada contra el hash guardado
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            print(f"🎉 ¡Login exitoso en Nethplay! Bienvenido (ID de usuario: {user_id})")
            return True
        else:
            print("❌ Credenciales incorrectas (Contraseña errónea).")
            return False

    except Exception as error:
        print(f"❌ Error durante el login: {error}")
        return False
    finally:
        cursor.close()
        conexion.close()

# --- Bloque de pruebas ---
if __name__ == "__main__":
    print("--- PROBANDO SISTEMA DE LOGIN PARA NETHPLAY ---")
    
    # Descomenta la siguiente línea la PRIMERA vez que quieras registrar un usuario de prueba:
    # registrar_usuario("gamer@nethplay.com", "password123")
    
    # Prueba de login con las credenciales correctas
    print("\nIntentando iniciar sesión...")
    login_usuario("gamer@nethplay.com", "password123")