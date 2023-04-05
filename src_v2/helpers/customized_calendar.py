import datetime
import calendar

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
from telebot_calendar import Calendar, CallbackData, Language, RUSSIAN_LANGUAGE, ENGLISH_LANGUAGE


class CustomizedCalendar(Calendar):

    __lang: Language

    def __init__(self, language: Language = ENGLISH_LANGUAGE):
        super().__init__(language)
        self.__lang = language

    def create_calendar(self, **kwargs) -> InlineKeyboardMarkup:
        """
        Create a built in inline keyboard with calendar

        :param name:
        :param year: Year to use in the calendar if you are not using the current year.
        :param month: Month to use in the calendar if you are not using the current month.
        :return: Returns an InlineKeyboardMarkup object with a calendar.
        """
        name = kwargs['name']
        year = kwargs['year']
        month = kwargs['month']

        now_day = datetime.datetime.now()

        if year is None:
            year = now_day.year
        if month is None:
            month = now_day.month

        calendar_callback = CallbackData(name, "action", "year", "month", "day")
        data_ignore = calendar_callback.new("IGNORE", year, month, "!")
        data_months = calendar_callback.new("MONTHS", year, month, "!")

        keyboard = InlineKeyboardMarkup(row_width=7)

        keyboard.add(
            InlineKeyboardButton(
                self.__lang.months[month - 1] + " " + str(year),
                callback_data=data_months,
            )
        )

        keyboard.add(
            *[
                InlineKeyboardButton(day, callback_data=data_ignore)
                for day in self.__lang.days
            ]
        )

        for week in calendar.monthcalendar(year, month):
            row = list()
            for day in week:
                if day == 0:
                    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
                elif (
                        f"{now_day.day}.{now_day.month}.{now_day.year}"
                        == f"{day}.{month}.{year}"
                ):
                    row.append(
                        InlineKeyboardButton(
                            f"({day})",
                            callback_data=calendar_callback.new(
                                "DAY", year, month, day
                            ),
                        )
                    )
                else:
                    row.append(
                        InlineKeyboardButton(
                            str(day),
                            callback_data=calendar_callback.new(
                                "DAY", year, month, day
                            ),
                        )
                    )
            keyboard.add(*row)

        keyboard.add(
            InlineKeyboardButton(
                "<",
                callback_data=calendar_callback.new("PREVIOUS-MONTH", year, month, "!"),
            ),
            InlineKeyboardButton(
                "Назад  ↩️",
                callback_data=calendar_callback.new("BACK", year, month, "!"),
            ),
            InlineKeyboardButton(
                "В меню 🏠",
                callback_data=calendar_callback.new("MENU", year, month, "!"),
            ),
            InlineKeyboardButton(
                ">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, "!")
            ),
        )

        return keyboard

    def calendar_query_handler(
        self,
        bot: TeleBot,
        call: CallbackQuery,
        name: str,
        action: str,
        year: int,
        month: int,
        day: int,
    ) -> None or datetime.datetime:
        """
        The method creates a new calendar if the forward or backward button is pressed
        This method should be called inside CallbackQueryHandler.


        :param bot: The object of the bot CallbackQueryHandler
        :param call: CallbackQueryHandler data
        :param day:
        :param month:
        :param year:
        :param action:
        :param name:
        :return: Returns a tuple
        """

        current = datetime.datetime(int(year), int(month), 1)
        if action == "IGNORE":
            bot.answer_callback_query(callback_query_id=call.id)
            return False, None
        elif action == "DAY":
            return datetime.datetime(int(year), int(month), int(day))
        elif action == "PREVIOUS-MONTH":
            preview_month = current - datetime.timedelta(days=1)

            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_calendar(
                    name=name,
                    year=int(preview_month.year),
                    month=int(preview_month.month),
                ),
                media=InputMediaPhoto(
                    media=open('helpers/static/images/media_message_picture.png', 'rb'),
                    caption=call.message.caption,
                    parse_mode='HTML'
                )
            )

            return None
        elif action == "NEXT-MONTH":
            next_month = current + datetime.timedelta(days=31)

            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_calendar(
                    name=name,
                    year=int(next_month.year),
                    month=int(next_month.month)
                ),
                media=InputMediaPhoto(
                    media=open('helpers/static/images/media_message_picture.png', 'rb'),
                    caption=call.message.caption,
                    parse_mode='HTML'
                )
            )

            return None
        elif action == "MONTHS":
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_months_calendar(
                    name=name,
                    year=current.year
                ),
                media=InputMediaPhoto(
                    media=open('helpers/static/images/media_message_picture.png', 'rb'),
                    caption=call.message.caption,
                    parse_mode='HTML'
                )
            )

            return None
        elif action == "MONTH":
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_calendar(
                    name=name,
                    year=int(year),
                    month=int(month)
                ),
                media=InputMediaPhoto(
                    media=open('helpers/static/images/media_message_picture.png', 'rb'),
                    caption=call.message.caption,
                    parse_mode='HTML'
                )
            )

            return None
        elif action == "MENU":
            return "MENU", None
        elif action == "BACK":
            return "BACK", None
        else:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text="ERROR!"
            )

            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )

            return None
