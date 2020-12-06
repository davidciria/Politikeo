# Politikeo
Bot de Twitter que predice tu identidad política a partir de tu actividad. Se asegura el funcionamiento correcto únicamente con usuarios que tuitean en español. Actualmente el bot es capaç de situar a un usuario entre los siguientes partidos políticos:
- Unidas Podemos
- Partido Socialista Obrero Español (PSOE)
- Ciudadanos (CS)
- Partido Popular (PP)
- Vox

**Siguenos en twitter:** @PolitikeoV https://twitter.com/PolitikeoV

## Uso del bot:
- Escribe un tweet mencionando la cuenta @PolitikeoV y tu cuenta será analizada.<br>
**Ejemplo:** "¿De que partido parezco ser? @PolitikeoV"
- Escribe un tweet mencionando la cuenta @PolitikeoV junto a otros usuarios y las cuentas del resto de usuarios serán analizadas.<br>
**Ejemplo:** "¿Que ideologia pueden tener? @PolitikeoV @Ejemplo1 @Ejemplo2"

**Creadores:** Àngel Herrero, Iair Mowszet y David Ciria

## Cargar keys de la API de Twitter

Las api keys se leen desde un fichero externo llamado api_keys.txt que debe situarse en la carpeta src → data. El formato del fichero debe ser el siguiente
``
api_keys.txt
consumer_key,aqui_el_valor_de_la_consumer_key
consumer_secret,aqui_el_valor_de_la_consumer_secret
access_token,aqui_el_valor_de_la_access_token
access_token_secret,aqui_el_valor_de_la_access_token_secret
``


