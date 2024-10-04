from controllers.base_controller import BaseController
from configs.storage import commandList

class SupportController(BaseController):

    def __init__(self, bot):
        super().__init__(bot)

    def support_message(self, message):
        if self.check_ignore("support_message_" + str(message.chat.id)):
            self.append_ignore("support_message_" + str(message.chat.id))
            text = (f"Բարև սիրելի {message.from_user.first_name}: \n"
                    "նկարագրեք ձեր խնդիրը. Եթե սա բողոք է մեկ այլ օգտատիրոջից, ապա նախ գրեք"
                    " օգտատիրոջ անունը, հետո խնդիրը։ \n\n"
                    "օրինակ «@find_way_arm_bot. ուշացել է ուղևորությունից և հրաժարվել է վճարել»")
            self.bot.send_message(message.chat.id, text)
            self.bot.register_next_step_handler(message, self.handler_support_message)

    def handler_support_message(self, message):
        if self.check_ignore("handler_support_message_" + str(message.chat.id)):
            self.append_ignore("handler_support_message_" + str(message.chat.id))
            command = message.text[1:]
            if command in commandList:
                return self.bot.send_message(message.chat.id, 'Դուք դադարեցրել եք գործողությունը,'
                                                              f' խնդրում ենք կրկին ուղարկել /{command} հրամանը մեկ'
                                                              f' այլ գործողություն սկսելու համար')
            self.support.user_message = message.text
            self.support.user_id = message.from_user.id
            self.support.user_name = message.from_user.username
            self.support.save_to_db()
            self.trash_ignore(message.chat.id)
            text = ("Շնորհակալություն համագործակցության համար,"
                    " դուք օգնեցիք մեզ ավելի պրոֆեսիոնալ դարձնել բոտը. "
                    "Ձեր հայտը անպայման կուսումնասիրվի մեր աջակցման թիմի կողմից, "
                    "և անհրաժեշտության դեպքում մենք կկապվենք ձեզ հետ։")
            self.bot.send_message(message.chat.id, text)
