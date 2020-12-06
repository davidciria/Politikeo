# Politikeo
Bot de Twitter que predice tu identidad política a partir de tu actividad. Se asegura el funcionamiento correcto únicamente con usuarios que tuitean en español. Actualmente el bot es capaz de situar a un usuario entre los siguientes partidos políticos:
- Unidas Podemos
- Partido Socialista Obrero Español (PSOE)
- Ciudadanos (CS)
- Partido Popular (PP)
- Vox

**Siguenos en twitter:** @PolitikeoV https://twitter.com/PolitikeoV

## Uso del bot
- Escribe un tweet mencionando la cuenta @PolitikeoV y tu cuenta será analizada.<br>
**Ejemplo:** "¿De que partido parezco ser? @PolitikeoV"
- Escribe un tweet mencionando la cuenta @PolitikeoV junto a otros usuarios y las cuentas del resto de usuarios serán analizadas.<br>
**Ejemplo:** "¿Que ideologia pueden tener? @PolitikeoV @Ejemplo1 @Ejemplo2"

## Cargar keys de la API de Twitter

Las api keys se leen desde un fichero externo llamado api_keys.txt que debe situarse en la carpeta src → data. El formato del fichero debe ser el siguiente
~~~
api_keys.txt
consumer_key,aqui_el_valor_de_la_consumer_key
consumer_secret,aqui_el_valor_de_la_consumer_secret
access_token,aqui_el_valor_de_la_access_token
access_token_secret,aqui_el_valor_de_la_access_token_secret
~~~

## Organización del código

**db_utils:** Código relacionado con el crawling y la creación de los modelos.
  - **Crawling.ipynb:** Código relacionado con el crawling de los tweets de los distintos partidos.
  - **Emojis.ipynb:** Código relacionado con la obtención de los emojis más significantes de cada partido.
  - **Keywords.ipynb:** Código relacionado con la obtención de las keywords más significantes de cada partido.
  - **fastTextModel.ipynb:** Código relacionado con la creación del modelo de fastText.
  
**src:** Código final del bot. Para que el bot funcione, es necesario rellenar las api keys de twitter en el fichero api_keys.txt (src → data).
  - **politikeo_main.py:** Se encuentra el main. Archivo a ejecutar para poner en marcha el bot. Se encuentra la logica general.
  - **config.py:** Código relacionado con la configuración de la api.
  - **decisionModel.py:** Código relacionado con el procesamiento del modelo de decisión.
  - **fastTextModel.py:** Código relacionado con el procesamiento del modelo de fastText.

**Creadores:** Àngel Herrero, Iair Mowszet y David Ciria
