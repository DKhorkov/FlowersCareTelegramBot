class BotMessagesEditor:

    def __init__(self, bot):
        self.bot = bot

    def edit_message(self, user_id, template_method, markup_method, error=False, **kwargs):
        str_user_id = kwargs['str_user_id']
        message_id = kwargs['json'][str_user_id]['message_for_update']
        # if markup_method.__name__ == 'create_calendar':
        #     self.bot.edit_message_text(
        #         chat_id=user_id,
        #         message_id=message_id,
        #         text=template_method(**kwargs),
        #         reply_markup=markup_method(**kwargs),
        #         parse_mode='html'
        #     )
        #
        # elif markup_method.__name__ == 'create_waiting_thresholds_markup' and error:
        #     error_msg = '⛔  Неправильно отправлены пороговые значения для выбранных каунтеров! ' \
        #                 'Пожалуйста, проверьте, что для каждого каунтера было введено числовое пороговое значение ' \
        #                 'через пробел!\n\n'
        #     self.bot.edit_message_text(
        #         chat_id=user_id,
        #         message_id=message_id,
        #         text=error_msg + template_method(**kwargs),
        #         reply_markup=markup_method(**kwargs),
        #         parse_mode='html'
        #     )
        #
        # else:
        try:
            self.bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=template_method(**kwargs),
                reply_markup=markup_method(**kwargs),
                parse_mode='html'
            )
        except TypeError:
            self.bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=template_method(),
                reply_markup=markup_method(),
                parse_mode='html'
            )