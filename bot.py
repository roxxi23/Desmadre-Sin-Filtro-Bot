import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

PREGUNTAS = [
    "¿Cuál es tu apodo más vergonzoso?",
    "¿Cuál fue tu peor papelón?",
    "¿Qué comida podrías comer todos los días?",
    "¿Cuál es tu hábito más raro?",
    "¿Qué canción te da vergüenza admitir que te gusta?",
    "¿Qué harías si fueras invisible por un día?",
    "¿Cuál es tu emoji más usado?",
    "¿Cuál fue tu peor compra?",
    "¿Qué harías si ganaras la lotería?",
    "¿Cuál es el meme que más te representa?",
    "¿Qué famoso te cae demasiado bien?",
    "¿Cuál fue tu peor foto?",
    "¿Qué cosa te da vergüenza hacer delante de otros?",
    "¿Cuál es tu frase más repetida?",
    "¿Qué fue lo último que buscaste en Google?",
    "¿Quién del grupo te hace reír más?",
    "¿Cuál es un secreto que casi nadie sabe?",
    "¿Alguna vez stalkeaste a alguien?",
    "¿Alguna vez fingiste estar ocupado para evitar a alguien?",
    "¿Cuál fue tu mayor arrepentimiento?",
    "¿Alguna vez mandaste un mensaje y quisiste borrarlo inmediatamente?",
    "¿Qué cosa te cuesta admitir?",
    "¿Alguna vez te hiciste el/la indiferente estando celoso/a?",
    "¿Cuál fue tu peor decisión por impulso?",
    "¿Alguna vez revisaste el perfil de tu ex?",
    "¿Qué persona te gustaría volver a ver?",
    "¿Alguna vez ocultaste que alguien te gustaba?",
    "¿Qué cosa te pone de mal humor rápidamente?",
    "¿Alguna vez dijiste «estoy llegando» sin haber salido?",
    "¿Qué es lo primero que mirás en alguien?",
    "¿Cuál es tu mayor debilidad?",
    "¿Alguna vez te arrepentiste de conocer a alguien?",
    "¿Quién del grupo creés que tiene más secretos?",
    "¿Creés en el amor a primera vista?",
    "¿Qué es lo más romántico que hiciste?",
    "¿Qué detalle te conquista?",
    "¿Qué cosa jamás perdonarías en una relación?",
    "¿Sos celoso/a?",
    "¿Preferís mensajes románticos o regalos?",
    "¿Cuál sería tu cita perfecta?",
    "¿Volverías con un ex?",
    "¿Qué canción dedicarías a alguien especial?",
    "¿Qué te enamora de una persona?",
    "¿Qué te hace perder el interés?",
    "¿Preferís una relación tranquila o intensa?",
    "¿Alguna vez te enamoraste de alguien inesperado?",
    "¿Qué significa para vos la fidelidad?",
    "¿Perdonarías una mentira importante?",
    "¿Qué gesto pequeño te derrite?",
    "¿Amor o química?",
    "¿Qué parte de una persona te atrae primero?",
    "¿Qué tipo de mirada te vuelve loco/a?",
    "¿Cuál sería tu cita más atrevida?",
    "¿Qué preferís: besos lentos o intensos?",
    "¿Te gusta tomar la iniciativa?",
    "¿Qué outfit te parece más irresistible?",
    "¿Cuál es tu mayor debilidad cuando alguien te gusta?",
    "¿Alguna vez sentiste química instantánea con alguien?",
    "¿Qué gesto te parece más seductor?",
    "¿Te animarías a confesarle a alguien del grupo que te atrae?",
    "¿Qué apodo coqueto te gustaría que te pusieran?",
    "¿Qué te conquista más: una mirada, una sonrisa o la voz?",
    "¿Alguna vez mandaste un mensaje demasiado atrevido?",
    "¿Qué cualidad hace que alguien sea irresistible para vos?",
    "¿Preferís una noche planeada o una aventura improvisada?",
    "¿Cuál fue el piropo más atrevido que recibiste?",
    "¿Quién del grupo tiene más pinta de romper corazones?",
    "Si tuvieras que elegir a alguien del grupo para una cita, ¿a quién elegirías?",
    "¿Quién del grupo tiene la mejor personalidad?",
]

RETOS = [
    "📸 Sube una foto de tus piernas.",
    "💋 Manda un GIF o video tirando un beso.",
    "😛 Manda una foto sacando la lengua.",
    "✍️ Escribe «Somos un Desmadre» en tu mano y manda una foto.",
    "😉 Manda una selfie guiñando un ojo.",
    "😂 Manda una foto haciendo tu cara más ridícula.",
    "🕺 Sube un video de 10 segundos bailando.",
    "😏 Manda una selfie haciendo tu mejor mirada.",
    "💄 Manda una selfie recién arreglado/a.",
    "❤️ Elige a alguien del grupo y dile algo lindo.",
    "🔥 Elige a alguien del grupo y dile qué es lo primero que te atrae de esa persona.",
    "🎤 Manda un audio cantando el estribillo de una canción.",
    "😈 Manda una selfie haciendo tu mejor pose.",
    "👀 Confiesa quién del grupo te parece más atractivo/a.",
    "💋 Manda una selfie tirando un beso.",
    "🤣 Manda un GIF que represente tu estado de ánimo.",
    "🎥 Graba un video diciendo «Yo soy parte del desmadre».",
    "😉 Manda un video guiñando un ojo.",
    "💃 Haz un pequeño baile y manda un GIF.",
    "🫣 Manda una selfie haciendo cara de inocente.",
    "🔥 Elige a alguien y descríbelo con tres palabras.",
    "😏 Dile a alguien del grupo un cumplido inesperado.",
    "🎲 Elige a alguien para que te haga una pregunta.",
    "💬 Escribe una confesión sin decir nombres.",
    "😂 Manda una foto con tu peor cara.",
    "❤️ Etiqueta a alguien que siempre te hace reír.",
    "😈 Etiqueta a alguien que consideres muy atrevido/a.",
    "💋 Manda un audio diciendo un cumplido coqueto.",
    "📸 Sube una foto de tu outfit actual.",
    "😉 Manda una selfie con tu mejor sonrisa.",
    "🎥 Graba un video saludando de una manera divertida.",
    "😛 Manda un GIF sacando la lengua.",
    "💃 Baila durante 15 segundos con la primera canción que aparezca.",
    "😂 Cambia tu foto de perfil durante 10 minutos.",
    "❤️ Escribe tres cosas que te gustan de alguien del grupo.",
    "🔥 Di quién tiene la mirada más peligrosa del grupo.",
    "😏 Di quién tiene más pinta de romper corazones.",
    "🎤 Manda un audio diciendo una frase usando una voz graciosa.",
    "📸 Manda una foto de tus manos.",
    "👀 Manda una foto de tus ojos.",
    "💋 Manda una foto de tus labios.",
    "😉 Haz una selfie con cara de «yo no fui».",
    "🎥 Graba un video haciendo tu mejor pose de modelo.",
    "🤣 Manda el último meme que guardaste.",
    "❤️ Dedícale una canción a alguien del grupo.",
    "😈 Elige a alguien y dile qué apodo le pondrías.",
    "🎲 Tira un dado virtual y haz un reto según el número.",
    "📸 Manda una foto usando algo rojo.",
    "🔥 Haz tu mejor pose y manda una selfie.",
    "💬 Escribe una frase coqueta sin mencionar a nadie.",
]

def teclado():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("❓ PREGUNTA", callback_data="pregunta"),
            InlineKeyboardButton("🔥 HOT", callback_data="hot"),
        ],
        [
            InlineKeyboardButton("🎲 RETO", callback_data="reto"),
            InlineKeyboardButton("🎲 DADO", callback_data="dado")
        ],
    ])

async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🔥😈 *DESMADRE SIN FILTRO* 😈🔥\n\n"
        "Bienvenido al bot oficial del desmadre.\n\n"
        "❓ Preguntas\n"
        "🔥 Preguntas HOT\n"
        "🎲 Retos\n\n"
        "¿Qué querés hacer?"
    )
    await update.message.reply_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado()
    )

async def pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = f"❓ *PREGUNTA*\n\n{random.choice(PREGUNTAS)}"
    await update.message.reply_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado()
    )

async def reto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🎲 *RETO DEL DESMADRE* 🎲\n\n"
        f"{random.choice(RETOS)}\n\n"
        "🚫 Si no querés hacerlo, simplemente PASÁ."
    )
    await update.message.reply_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado()
    )

async def hot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = f"🔥 *PREGUNTA HOT* 🔥\n\n{random.choice(PREGUNTAS[49:])}"
    await update.message.reply_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado()
    )

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pregunta":
        texto = f"❓ *PREGUNTA*\n\n{random.choice(PREGUNTAS)}"
    elif query.data == "dado":
        numero = random.randint(1, 6)
        texto = f"🎲 *DADO DEL DESMADRE* 🎲\n\nSalió el número: {numero}"
    elif query.data == "reto":
        texto = (
            "🎲 *RETO DEL DESMADRE* 🎲\n\n"
            f"{random.choice(RETOS)}\n\n"
            "🚫 Si no querés hacerlo, simplemente PASÁ."
        )
    else:
        texto = f"🔥 *PREGUNTA HOT* 🔥\n\n{random.choice(PREGUNTAS[49:])}"

    await query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado()
    )

def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError("Falta configurar BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", inicio))
    app.add_handler(CommandHandler("pregunta", pregunta))
    app.add_handler(CommandHandler("reto", reto))
    app.add_handler(CommandHandler("hot", hot))
    app.add_handler(CallbackQueryHandler(botones))

    print("🔥 Desmadre Sin Filtro está funcionando...")
    app.run_polling()

if __name__ == "__main__":
    main()
