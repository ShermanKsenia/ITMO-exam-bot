import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from mistralai import Mistral
from PyPDF2 import PdfReader
import textwrap



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your actual bot token from @BotFather
TOKEN = os.environ['BOT_KEY']
MISTRAL_TOKEN = os.environ['MISTRAL_KEY']
MODEL = 'mistral-small'  
PDF_FOLDER = './downloaded_plans/'

PROMPT = """You are a helpful assistant that answers to questions of applicants to ITMO University. 
You should answer only to those questions which are connected to master programs 'Искусственный интеллект' and 'Управление ИИ продуктами'.
If a person asks you a question in a different field you should say that you answers only to a questions about the maste programs.
Applicants can ask questions about the curriculum, which elective courses are best for an applicant to take during their studies, taking into account the applicant's information about his background, etc.
Answer on Russian
"""

client = Mistral(api_key=MISTRAL_TOKEN)

def extract_text_from_pdfs():
    """Extract text from all PDFs in the folder"""
    all_text = ""
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith('.pdf'):
            try:
                reader = PdfReader(os.path.join(PDF_FOLDER, filename))
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                all_text += f"\n\n[Из файла {filename}]:\n{text}"
            except Exception as e:
                logger.error(f"Error reading {filename}: {e}")
    return all_text

curriculums = extract_text_from_pdfs()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I will greet you whenever you send me a message.')

async def hello_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Customized response"""
    user = update.message.from_user
    await update.message.reply_text(f'Hello {user.first_name}! Nice to meet you!')

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Customized response"""
    pdf_context = textwrap.dedent(f"""
            Here is relevant information from available PDF documents:
            {curriculums[:15000]}  # Limit context size
            """)
    user_message = update.message.text
    chat_response = client.chat.complete(
        model= MODEL,
        messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": pdf_context + "\n\Вопрос: " + user_message}
            ],
            temperature=0.7
        )
    response = chat_response.choices[0].message.content
    
    await update.message.reply_text(response)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    # curriculums = extract_text_from_pdfs()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello_response))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question))


    # Run the bot until you press Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()