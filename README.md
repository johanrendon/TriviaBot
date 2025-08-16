# 🤖 Bot de Discord - Trivia y Comandos Divertidos

Este proyecto es un bot de Discord que incluye:

- 🎮 Un sistema completo de **Trivia** usando la API de OpenTDB.
- 🏓 Un comando **ping** para comprobar la latencia del bot.
- 🏆 Una tabla de posiciones de trivia en tiempo real.
- ⚙️ Una arquitectura modular con **cogs** para organizar los comandos.

## 🚀 Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>

Instalar las dependencias

```bash
    pip install -r requirements.txt
```

🔑 Configuración del Token

Este bot utiliza variables de entorno para mayor seguridad.
Debes crear un archivo .env en la raíz del proyecto con el siguiente contenido:

    TOKEN=TU_TOKEN_DE_DISCORD_AQUI

👉 Reemplaza TU_TOKEN_DE_DISCORD_AQUI con el token de tu bot generado en el  [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).
▶️ Ejecución

Para iniciar el bot:

```bash
    python main.py
```

Si todo está configurado correctamente, en la consola deberías ver:

🤖 Bot conectado como NOMBRE_DEL_BOT

📦 Dependencias principales

Algunas de las librerías incluidas en requirements.txt:

    discord.py → Para la interacción con la API de Discord.

    aiohttp → Para hacer solicitudes HTTP a la API de Trivia.

    python-dotenv → Para manejar variables de entorno de forma sencilla.

📝 Notas

    Solo el usuario que ejecuta el comando !trivia puede responder.

    Las puntuaciones se guardan en memoria mientras el bot esté en ejecución (no en base de datos).

    El prefijo del bot se configura en config.py.

📜 Licencia

Este proyecto es de uso libre para fines educativos y personales.
