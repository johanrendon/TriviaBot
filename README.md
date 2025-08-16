# 🤖 Bot de Discord - Trivia y Comandos Divertidos

Este proyecto es un bot de Discord que incluye:

- 🎮 Un sistema completo de **Trivia** usando la API de OpenTDB.
- 🏓 Un comando **ping** para comprobar la latencia del bot.
- 🏆 Una tabla de clasificación de trivia en tiempo real.
- ⚙️ Una arquitectura modular con **cogs** para organizar los comandos.

## 🚀 Instalación

1. **Clona el repositorio**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_PROYECTO>
    ```

2. **Instala las dependencias**

    ```bash
    pip install -r requirements.txt
    ```

### 🔑 Configuración del Token

Este bot utiliza variables de entorno para una mayor seguridad.
Debes crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

    TOKEN=TU_TOKEN_DE_BOT_DE_DISCORD_AQUI

👉 Reemplaza `TU_TOKEN_DE_BOT_DE_DISCORD_AQUI` con el token de tu bot generado en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).

### 🔧 Configuración en el Portal de Desarrolladores de Discord

Antes de ejecutar el bot, necesitas configurar algunos ajustes en el Portal de Desarrolladores de Discord para asegurarte de que tenga los permisos necesarios para funcionar.

#### Habilitar Intents Privilegiados

Para que el bot pueda leer mensajes (como las respuestas de la trivia) y reconocer a los miembros del servidor, debes habilitar dos "Intents Privilegiados".

1. Ve al [Portal de Desarrolladores de Discord](https://discord.com/developers/applications) y selecciona tu aplicación.
2. En el menú de la izquierda, haz clic en la pestaña **"Bot"**.
3. Desplázate hacia abajo hasta la sección **"Privileged Gateway Intents"**.
4. Activa las siguientes opciones:
    - **SERVER MEMBERS INTENT**: Permite que el bot reciba eventos relacionados con los miembros del servidor (por ejemplo, cuando alguien se une).
    - **MESSAGE CONTENT INTENT**: Permite que el bot lea el contenido de los mensajes. Esto es crucial para los comandos y las respuestas de la trivia.
5. ¡No olvides guardar los cambios!

#### 🔗 Invitar el Bot a tu Servidor

Una vez configurado, puedes generar un enlace de invitación para añadir el bot a cualquier servidor en el que tengas permisos de administrador.

1. Dentro de tu aplicación en el portal, ve a la pestaña **"OAuth2"** y luego a **"URL Generator"**.
2. En la sección **"SCOPES"**, marca las casillas `bot` y `applications.commands`.
3. Aparecerá una nueva sección llamada **"BOT PERMISSIONS"**. Aquí debes seleccionar los permisos que el bot necesita para funcionar correctamente:
    - `Send Messages` (Enviar Mensajes)
    - `Read Message History` (Leer el historial de mensajes)
    - `Add Reactions` (Añadir Reacciones)
4. Copia la URL generada en la parte inferior y pégala en tu navegador.
5. Selecciona el servidor al que quieres invitar al bot y autoriza los permisos.

## ▶️ Ejecutar el Bot

Para iniciar el bot:

```bash
python main.py
```

Si todo está configurado correctamente, deberías ver en la consola:

🤖 Bot conectado como NOMBRE_DEL_BOT

## 📦 Dependencias Principales

Algunas de las librerías incluidas en requirements.txt:

    discord.py → Para interactuar con la API de Discord.

    aiohttp → Para realizar peticiones HTTP a la API de Trivia.

    python-dotenv → Para gestionar variables de entorno fácilmente.

## 🎮 Comandos

Aquí están los comandos disponibles para interactuar con el bot.

### 🧠 !trivia

Inicia una nueva partida de trivia. El bot enviará una pregunta de opción múltiple. Si el usuario que ejecutó el comando responde correctamente, ganará un punto que se registrará en la tabla de clasificación.

### 🏆 !leaderboard

Muestra la tabla de clasificación actual del servidor. Puedes ver quién va ganando y cuántos puntos tiene cada jugador. Los puntajes se reinician si el bot se apaga.

### 🏓 !ping

Comprueba la latencia del bot. Este comando responderá con el tiempo de respuesta actual en milisegundos (ms), permitiéndote saber si el bot está funcionando de manera rápida y eficiente.

## 📝 Notas

    Solo el usuario que ejecuta el comando !trivia puede responder.

    Los puntajes se almacenan en memoria mientras el bot está en ejecución (no en una base de datos).

    El prefijo del bot se configura en config.py.

## 📜 Licencia

Este proyecto es de uso libre para fines educativos y personales.
