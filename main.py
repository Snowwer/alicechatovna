import openai
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

# Initialize OpenAI API
openai.api_key = "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"


# Initialize Telegram Bot and Dispatcher
bot = Bot(token="6025503505:AAGWxnicCk0BD1NXu7cKOVLEUGNYmjRJYhg")
dp = Dispatcher(bot, storage=MemoryStorage())

# Define States
class Question(StatesGroup):
    waiting_for_question = State()

# Define Command Handlers
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hi, ask me any question and I will try to answer it!")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = "Ask me any question and I will try to answer it using OpenAI's API."
    await message.reply(help_text)

# Define Question Handler
@dp.message_handler(commands=['q'])
async def question_command(message: types.Message):
    await message.reply("Чё?")
    await Question.waiting_for_question.set()

@dp.message_handler(state=Question.waiting_for_question)
async def answer_question(message: types.Message, state: FSMContext):
    # Get user question from state
    user_question = message.text

    # Call OpenAI API to answer the question
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=user_question,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Get OpenAI API response
    answer = response.choices[0].text.strip()

    # Send answer to user
    await message.reply(md.text(md.bold("Answer: "), answer))

    # Reset state
    await state.finish()

# Define Error Handler
@dp.errors_handler()
async def errors_handler(update, error):
    await bot.send_message(chat_id='-812589943', text=f'An error occurred: {error}')

# Start the Bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
