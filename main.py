import os
import csv
import time
import re
import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from typing import TypeVar, Generic

generic_type = TypeVar('generic_type')

class EmptyDataStructureException(Exception):
    pass

class InvalidValueException(Exception):
    pass

class CustomNode(Generic[generic_type]):
    def __init__(self, node_value: generic_type):
        self._node_value = node_value
        self._next_node = None

    def get_node_value(self) -> generic_type:
        return self._node_value

    def set_node_value(self, new_value: generic_type):
        if new_value is None:
            raise InvalidValueException()
        self._node_value = new_value

    def get_next_node(self):
        return self._next_node

    def set_next_node(self, target_node):
        self._next_node = target_node

class CustomQueue(Generic[generic_type]):
    def __init__(self):
        self._front_node = None
        self._rear_node = None
        self._queue_size = 0

    def enqueue_item(self, item_value: generic_type):
        if item_value is None:
            raise InvalidValueException()
        new_node = CustomNode[generic_type](item_value)
        if self._rear_node is None:
            self._front_node = new_node
            self._rear_node = new_node
        else:
            self._rear_node.set_next_node(new_node)
            self._rear_node = new_node
        self._queue_size += 1

    def dequeue_item(self) -> generic_type:
        if self.is_queue_empty():
            raise EmptyDataStructureException()
        dequeued_value = self._front_node.get_node_value()
        self._front_node = self._front_node.get_next_node()
        if self._front_node is None:
            self._rear_node = None
        self._queue_size -= 1
        return dequeued_value

    def is_queue_empty(self) -> bool:
        return self._queue_size == 0

    def get_queue_size(self) -> int:
        return self._queue_size

class CustomList(Generic[generic_type]):
    def __init__(self):
        self._head_node = None
        self._list_size = 0

    def append_item(self, item_value: generic_type):
        if item_value is None:
            raise InvalidValueException()
        new_node = CustomNode[generic_type](item_value)
        if self._head_node is None:
            self._head_node = new_node
        else:
            current_iterator = self._head_node
            while current_iterator.get_next_node() is not None:
                current_iterator = current_iterator.get_next_node()
            current_iterator.set_next_node(new_node)
        self._list_size += 1

    def get_item_at(self, target_index: int) -> generic_type:
        if target_index < 0 or target_index >= self._list_size:
            raise InvalidValueException()
        current_iterator = self._head_node
        for _ in range(target_index):
            current_iterator = current_iterator.get_next_node()
        return current_iterator.get_node_value()

    def get_list_size(self) -> int:
        return self._list_size

class SurveyQuestion:
    def __init__(self, question_text: str, is_mandatory: bool, validation_regex: str = None, error_message: str = None, expected_type: str = 'text'):
        if not question_text:
            raise InvalidValueException()
        self._question_text = question_text
        self._is_mandatory = is_mandatory
        self._validation_regex = validation_regex
        self._error_message = error_message
        self._expected_type = expected_type

    def get_question_text(self) -> str:
        return self._question_text

    def get_is_mandatory(self) -> bool:
        return self._is_mandatory
        
    def get_validation_regex(self) -> str:
        return self._validation_regex
        
    def get_error_message(self) -> str:
        return self._error_message

    def get_expected_type(self) -> str:
        return self._expected_type

class SurveyAnswer:
    def __init__(self, answer_title: str, answer_value: str):
        if not answer_title or not answer_value:
            raise InvalidValueException()
        self._answer_title = answer_title
        self._answer_value = answer_value

    def get_answer_title(self) -> str:
        return self._answer_title

    def get_answer_value(self) -> str:
        return self._answer_value

class DirectoryManager:
    def __init__(self, root_directory: str):
        if not root_directory:
            raise InvalidValueException()
        self._root_directory = root_directory
        if not os.path.exists(self._root_directory):
            os.makedirs(self._root_directory)

    def prepare_user_directory(self, user_id: int, username: str) -> str:
        folder_name = f"{user_id}_{username.replace('@', '')}"
        user_path = os.path.join(self._root_directory, folder_name)
        if not os.path.exists(user_path):
            os.makedirs(user_path)
            print(f"[SYSTEM] Carpeta generada/verificada para el usuario: {folder_name}")
        return user_path

class FileStorageManager:
    def __init__(self, bot_client: telebot.TeleBot):
        if bot_client is None:
            raise InvalidValueException()
        self._bot_client = bot_client

    def process_and_save_telegram_file(self, file_id: str, target_directory: str) -> str:
        if not file_id or not target_directory:
            raise InvalidValueException()
        telegram_file_info = self._bot_client.get_file(file_id)
        downloaded_bytes = self._bot_client.download_file(telegram_file_info.file_path)
        extracted_extension = telegram_file_info.file_path.split('.')[-1]
        time_stamp = str(int(time.time() * 1000))
        random_suffix = str(random.randint(1000, 9999))
        generated_file_name = f"media_{time_stamp}_{random_suffix}.{extracted_extension}"
        absolute_file_path = os.path.join(target_directory, generated_file_name)
        with open(absolute_file_path, 'wb') as local_file_descriptor:
            local_file_descriptor.write(downloaded_bytes)
        print(f"[FILE] Archivo guardado correctamente en: {absolute_file_path}")
        return absolute_file_path

class CsvRepository:
    def __init__(self, target_file_path: str):
        if not target_file_path:
            raise InvalidValueException()
        self._target_file_path = target_file_path

    def create_data_record(self, record_data: CustomList[str], headers_data: CustomList[str]):
        file_exists = os.path.isfile(self._target_file_path)
        
        row_container = []
        for index_pos in range(record_data.get_list_size()):
            row_container.append(record_data.get_item_at(index_pos))
            
        headers_container = []
        for index_pos in range(headers_data.get_list_size()):
            headers_container.append(headers_data.get_item_at(index_pos))
        
        with open(self._target_file_path, mode='a', newline='', encoding='utf-8') as target_file:
            csv_writer = csv.writer(target_file)
            if not file_exists:
                csv_writer.writerow(headers_container)
            csv_writer.writerow(row_container)

class UserSessionState:
    def __init__(self, session_user_id: int, session_username: str, user_directory_path: str):
        if session_user_id <= 0:
            raise InvalidValueException()
        self._session_user_id = session_user_id
        self._session_username = session_username
        self._user_directory_path = user_directory_path
        self._pending_questions = CustomQueue[SurveyQuestion]()
        self._collected_answers = CustomList[SurveyAnswer]()
        self._current_active_question = None

    def get_session_user_id(self) -> int:
        return self._session_user_id

    def get_session_username(self) -> str:
        return self._session_username

    def get_user_directory_path(self) -> str:
        return self._user_directory_path

    def load_survey_questions(self, questions_queue: CustomQueue[SurveyQuestion]):
        while not questions_queue.is_queue_empty():
            self._pending_questions.enqueue_item(questions_queue.dequeue_item())

    def pull_next_question(self) -> SurveyQuestion:
        if self._pending_questions.is_queue_empty():
            self._current_active_question = None
            return None
        self._current_active_question = self._pending_questions.dequeue_item()
        return self._current_active_question

    def get_current_active_question(self) -> SurveyQuestion:
        return self._current_active_question

    def push_question_back(self, question: SurveyQuestion):
        temp_queue = CustomQueue[SurveyQuestion]()
        temp_queue.enqueue_item(question)
        while not self._pending_questions.is_queue_empty():
            temp_queue.enqueue_item(self._pending_questions.dequeue_item())
        self._pending_questions = temp_queue

    def store_user_answer(self, user_answer_value: str):
        if self._current_active_question is None:
            raise InvalidValueException()
        new_answer_entry = SurveyAnswer(self._current_active_question.get_question_text(), user_answer_value)
        self._collected_answers.append_item(new_answer_entry)

    def export_answers_to_list(self) -> CustomList[str]:
        exported_list = CustomList[str]()
        for index_pos in range(self._collected_answers.get_list_size()):
            exported_list.append_item(self._collected_answers.get_item_at(index_pos).get_answer_value())
        return exported_list

    def export_headers_to_list(self) -> CustomList[str]:
        exported_list = CustomList[str]()
        for index_pos in range(self._collected_answers.get_list_size()):
            exported_list.append_item(self._collected_answers.get_item_at(index_pos).get_answer_title())
        return exported_list

    def format_short_admin_notification(self) -> str:
        return f"🚨 ЗАРЕГИСТРИРОВАН НОВЫЙ ОТЧЕТ 🚨\n\n👤 Пользователь: {self._session_username}\n🆔 ID: {self._session_user_id}\n📁 Данные успешно сохранены в персональную папку."

bot_access_token = "8117819271:AAGcvNgV8oh7jogS_eu5QtBmiA4myYoCglw"
admin_chat_id = 250309338
root_data_path = r"C:\BOT\User_Data"

telegram_bot_client = telebot.TeleBot(bot_access_token, threaded=False)
directory_manager = DirectoryManager(root_data_path)
file_manager = FileStorageManager(telegram_bot_client)
active_user_sessions = {}
pending_admin_notifications = CustomQueue[str]()

def resolve_user_display_name(telegram_user) -> str:
    if telegram_user.username is not None:
        return f"@{telegram_user.username}"
    if telegram_user.first_name is not None:
        return str(telegram_user.first_name).replace(" ", "_")
    return "Unknown_User"

def build_questions_catalog() -> CustomQueue[SurveyQuestion]:
    catalog_queue = CustomQueue[SurveyQuestion]()
    catalog_queue.enqueue_item(SurveyQuestion("👤 Укажите фамилию пропавшего", True))
    catalog_queue.enqueue_item(SurveyQuestion("👤 Имя", True))
    catalog_queue.enqueue_item(SurveyQuestion("👤 Отчество", False))
    catalog_queue.enqueue_item(SurveyQuestion("📅 Дата рождения (в формате: ДД/ММ/ГГГГ)", False, r"^\d{2}/\d{2}/\d{4}$", "⚠️ Неверный формат. Используйте ДД/ММ/ГГГГ (например, 15/05/1990)."))
    catalog_queue.enqueue_item(SurveyQuestion("🪖 Номер воинской части (Номер состоит из 5 цифр. Введите только их. Например: 78567)", False, r"^\d{5}$", "⚠️ Введите ровно 5 цифр."))
    catalog_queue.enqueue_item(SurveyQuestion("🏢 Подразделение (Например: 155 бригада морской пехоты)", False))
    catalog_queue.enqueue_item(SurveyQuestion("🎖 Звание пропавшего без вести (Например: младший сержант)", False))
    catalog_queue.enqueue_item(SurveyQuestion("🗣 Позывной", False))
    catalog_queue.enqueue_item(SurveyQuestion("🏷 Номер жетона (например, АВ 434381)", False))
    catalog_queue.enqueue_item(SurveyQuestion("🇷🇺 Национальная принадлежность (Например: бурят)", False))
    catalog_queue.enqueue_item(SurveyQuestion("🛡 Служба в ВС РФ (Например: Мобилизован/контрактник/ЧВК/пошел из тюрьмы)", False))
    catalog_queue.enqueue_item(SurveyQuestion("📞 Номер моб. телефона пропавшего без вести (в формате: +х ххх ххх хххх)", False, r"^\+[0-9\s]{10,20}$", "⚠️ Неверный формат. Начните с '+' и введите правильный номер."))
    catalog_queue.enqueue_item(SurveyQuestion("📅 Примерная дата, когда пропал без вести (в формате: ДД/ММ/ГГГГ)", False, r"^\d{2}/\d{2}/\d{4}$", "⚠️ Неверный формат. Используйте ДД/ММ/ГГГГ."))
    catalog_queue.enqueue_item(SurveyQuestion("📍 Примерное место, где пропал без вести (Например: село Веселое. Или координаты: 48.1850, 37.7443)", False))
    catalog_queue.enqueue_item(SurveyQuestion("📸 Фотография пропавшего без вести (1/3). Пожалуйста, отправьте только 1 фото.", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("📸 Фотография пропавшего без вести (2/3). Пожалуйста, отправьте еще 1 фото. Если больше нет, нажмите 'Пропустить'.", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("📸 Фотография пропавшего без вести (3/3). Пожалуйста, отправьте еще 1 фото. Если больше нет, нажмите 'Пропустить'.", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("👞 Размер обуви", False))
    catalog_queue.enqueue_item(SurveyQuestion("👁 Особые приметы (Опишите особенности: татуировки, шрамы, переломы, родинки, протезы и т.д)", False))
    catalog_queue.enqueue_item(SurveyQuestion("📸 Фотография особых примет (1/3). Пожалуйста, отправьте только 1 фото.", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("📸 Фотография особых примет (2/3). Пожалуйста, отправьте еще 1 фото. Если больше нет, нажмите 'Пропустить'.", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("📸 Фотография особых примет (3/3). Пожалуйста, отправьте еще 1 фото. Если больше нет, нажмите 'Пропустить'.", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("🧬 ДНК-профиль биологического родственника (фотография или картинка jpg, png).", False, None, None, 'photo'))
    catalog_queue.enqueue_item(SurveyQuestion("📝 Дополнительная информация (Все то, что может помочь в поиске)", False))
    catalog_queue.enqueue_item(SurveyQuestion("🤝 Кем вы приходитесь пропавшему без вести (родитель, супруг, брат/сестра, и т.д)", False))
    catalog_queue.enqueue_item(SurveyQuestion("👤 Ваша фамилия", False))
    catalog_queue.enqueue_item(SurveyQuestion("👤 Ваше имя", False))
    catalog_queue.enqueue_item(SurveyQuestion("👤 Ваше отчество", False))
    catalog_queue.enqueue_item(SurveyQuestion("📞 Ваш контактный номер телефона для обратной связи (в формате: +х ххх ххх хххх)", True, r"^\+[0-9\s]{10,20}$", "⚠️ Неверный формат. Начните с '+' и введите правильный номер."))
    catalog_queue.enqueue_item(SurveyQuestion("🌍 Укажите из какого вы региона РФ", False))
    catalog_queue.enqueue_item(SurveyQuestion("💼 Укажите ваше место работы", False))
    return catalog_queue

def create_skip_keyboard() -> ReplyKeyboardMarkup:
    keyboard_layout = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    skip_button = KeyboardButton("Не знаете? Нажмите, чтобы пропустить")
    keyboard_layout.add(skip_button)
    return keyboard_layout

def create_final_action_keyboard(include_operator_button: bool) -> InlineKeyboardMarkup:
    action_keyboard = InlineKeyboardMarkup(row_width=1)
    restart_button = InlineKeyboardButton(text="➕ Новая заявка", callback_data="trigger_restart")
    if include_operator_button:
        operator_button = InlineKeyboardButton(text="📞 Связь с оператором", url=f"tg://user?id={admin_chat_id}")
        action_keyboard.add(operator_button, restart_button)
    else:
        action_keyboard.add(restart_button)
    return action_keyboard

def flush_admin_notifications():
    temp_queue = CustomQueue[str]()
    while not pending_admin_notifications.is_queue_empty():
        target_message = pending_admin_notifications.dequeue_item()
        try:
            telegram_bot_client.send_message(admin_chat_id, target_message)
            print(f"[SYSTEM] Notificación despachada correctamente desde la cola hacia el admin {admin_chat_id}.")
        except Exception as dispatch_error:
            temp_queue.enqueue_item(target_message)
            print(f"[WARNING] Fallo al enviar notificación en cola. Se reintentará luego. Motivo: {dispatch_error}")
            
    while not temp_queue.is_queue_empty():
        pending_admin_notifications.enqueue_item(temp_queue.dequeue_item())

def prompt_next_survey_question(chat_id_value: int, user_session: UserSessionState):
    next_question = user_session.pull_next_question()
    if next_question is not None:
        try:
            telegram_bot_client.send_message(
                chat_id_value, 
                next_question.get_question_text(), 
                reply_markup=create_skip_keyboard()
            )
        except Exception:
            pass
    else:
        conclude_survey_process(chat_id_value, user_session)

def conclude_survey_process(chat_id_value: int, user_session: UserSessionState):
    cleanup_message = "⏳ Сохранение данных..."
    remove_keyboard_markup = ReplyKeyboardRemove()
    
    try:
        telegram_bot_client.send_message(
            chat_id_value, 
            cleanup_message, 
            reply_markup=remove_keyboard_markup
        )
    except Exception:
        pass
        
    try:
        user_specific_csv = os.path.join(user_session.get_user_directory_path(), "user_data.csv")
        user_csv_repository = CsvRepository(user_specific_csv)
        extracted_data_list = user_session.export_answers_to_list()
        extracted_headers_list = user_session.export_headers_to_list()
        user_csv_repository.create_data_record(extracted_data_list, extracted_headers_list)
        print(f"[SUCCESS] CSV guardado exitosamente para el usuario: {user_session.get_session_username()}")
    except Exception as data_error:
        print(f"[ERROR CRÍTICO] Falló la exportación CSV para el usuario {user_session.get_session_username()}: {data_error}")
        
    final_message_text = "✅ Ваша заявка на поиск принята. Срок предоставления ответа может быть больше 14 дней. ❗️ Не подавайте заявку на поиск одного и того же человека несколько раз."
    try:
        telegram_bot_client.send_message(
            chat_id_value, 
            final_message_text, 
            reply_markup=create_final_action_keyboard(True)
        )
    except Exception:
        try:
            telegram_bot_client.send_message(
                chat_id_value, 
                final_message_text, 
                reply_markup=create_final_action_keyboard(False)
            )
        except Exception:
            pass
        
    admin_notification_text = user_session.format_short_admin_notification()
    pending_admin_notifications.enqueue_item(admin_notification_text)
    flush_admin_notifications()
    
    if chat_id_value in active_user_sessions:
        del active_user_sessions[chat_id_value]

def initiate_survey_for_user(chat_id_value: int, session_username: str):
    user_directory_path = directory_manager.prepare_user_directory(chat_id_value, session_username)
    new_user_session = UserSessionState(chat_id_value, session_username, user_directory_path)
    questions_queue = build_questions_catalog()
    new_user_session.load_survey_questions(questions_queue)
    active_user_sessions[chat_id_value] = new_user_session
    prompt_next_survey_question(chat_id_value, new_user_session)

@telegram_bot_client.message_handler(commands=['start'])
def handle_bot_start(incoming_message):
    flush_admin_notifications()
    user_chat_id = incoming_message.chat.id
    session_username = resolve_user_display_name(incoming_message.from_user)
    print(f"[NEW USER] Inicio de interacción: {session_username} (ID: {user_chat_id})")
    welcome_text = "Здравствуйте. Пожалуйста, представьтесь и подробно заполните анкету, после с вами свяжется оператор."
    try:
        telegram_bot_client.send_message(user_chat_id, welcome_text)
    except Exception:
        return
    initiate_survey_for_user(user_chat_id, session_username)

@telegram_bot_client.callback_query_handler(func=lambda call_event: call_event.data == "trigger_restart")
def handle_survey_restart(call_event):
    flush_admin_notifications()
    user_chat_id = call_event.message.chat.id
    session_username = resolve_user_display_name(call_event.from_user)
    print(f"[RESTART] Petición de nuevo formulario desde: {session_username} (ID: {user_chat_id})")
    try:
        telegram_bot_client.answer_callback_query(call_event.id)
        restart_message = "Новая анкета. Пожалуйста, заполните данные внимательно."
        telegram_bot_client.send_message(user_chat_id, restart_message)
    except Exception:
        pass
    initiate_survey_for_user(user_chat_id, session_username)

@telegram_bot_client.message_handler(content_types=['text', 'photo', 'document'])
def handle_user_survey_input(incoming_message):
    flush_admin_notifications()
    user_chat_id = incoming_message.chat.id
    if user_chat_id not in active_user_sessions:
        try:
            expire_msg = "⚠️ Сессия истекла или бот был перезагружен. Пожалуйста, отправьте /start, чтобы начать заново."
            telegram_bot_client.send_message(user_chat_id, expire_msg)
            print(f"[WARNING] Usuario sin sesión ({user_chat_id}) intentó interactuar. Solicitando /start.")
        except Exception:
            pass
        return
        
    current_session = active_user_sessions[user_chat_id]
    active_question = current_session.get_current_active_question()
    
    if active_question is None:
        return

    extracted_value = ""
    expected_type = active_question.get_expected_type()
    
    if incoming_message.content_type == 'text':
        if incoming_message.text == "Не знаете? Нажмите, чтобы пропустить":
            if active_question.get_is_mandatory():
                error_message = "⚠️ Это поле обязательно для заполнения. Пожалуйста, предоставьте информацию."
                try:
                    telegram_bot_client.send_message(user_chat_id, error_message)
                    current_session.push_question_back(active_question)
                    prompt_next_survey_question(user_chat_id, current_session)
                except Exception:
                    pass
                return
            extracted_value = "Пропущено"
            print(f"[INFO] {current_session.get_session_username()} saltó una pregunta.")
        else:
            if expected_type == 'photo':
                photo_error_message = "📸 ⚠️ Ошибка: Пожалуйста, отправьте фотографию (или документ), либо нажмите кнопку 'Пропустить'."
                try:
                    telegram_bot_client.send_message(user_chat_id, photo_error_message)
                    current_session.push_question_back(active_question)
                    prompt_next_survey_question(user_chat_id, current_session)
                except Exception:
                    pass
                return
                
            extracted_value = incoming_message.text
            regex_pattern = active_question.get_validation_regex()
            if regex_pattern is not None:
                if not re.search(regex_pattern, extracted_value):
                    error_msg = active_question.get_error_message()
                    try:
                        telegram_bot_client.send_message(user_chat_id, error_msg)
                        current_session.push_question_back(active_question)
                        prompt_next_survey_question(user_chat_id, current_session)
                    except Exception:
                        pass
                    return
            
    elif incoming_message.content_type in ['photo', 'document']:
        if expected_type == 'text':
            text_error_message = "📝 ⚠️ Ошибка: Пожалуйста, отправьте текстовое сообщение."
            try:
                telegram_bot_client.send_message(user_chat_id, text_error_message)
                current_session.push_question_back(active_question)
                prompt_next_survey_question(user_chat_id, current_session)
            except Exception:
                pass
            return
            
        try:
            if incoming_message.content_type == 'photo':
                target_file_id = incoming_message.photo[-1].file_id
            else:
                target_file_id = incoming_message.document.file_id
                
            saved_file_path = file_manager.process_and_save_telegram_file(target_file_id, current_session.get_user_directory_path())
            extracted_value = saved_file_path
        except Exception as e:
            extracted_value = "[Error_Saving_Media]"
            print(f"[ERROR] No se pudo guardar la imagen: {str(e)}")

    try:
        current_session.store_user_answer(extracted_value)
        prompt_next_survey_question(user_chat_id, current_session)
    except InvalidValueException:
        pass

if __name__ == "__main__":
    print("[SYSTEM] Servidor del bot iniciado...")
    print("[SYSTEM] Estructura de carpetas configurada en C:\\BOT\\User_Data")
    print("[SYSTEM] Callbacks iniciados. Esperando usuarios de Telegram...\n")
    while True:
        try:
            telegram_bot_client.polling(none_stop=True)
        except Exception as system_error:
            print(f"[ERROR CRÍTICO] Conflicto de API o corte de red detectado. Reconectando en 5 segundos... Error: {system_error}")
            time.sleep(5)