from transitions import Machine


class PythonMeetupBot(object):
    states = ['initial', 'say_hello', 'enter_name', 'go_to_main_menu', 'go_to_programs',
              'go_to_questions']

    def __init__(self, name):
        self.machine = Machine(model=self, states=PythonMeetupBot.states, initial='say_hello')
        self.name = name
        # self.machine.add_transition('get_started', 'initial', 'say_hello')  # Переводим бота в стартовое состояние
        self.machine.add_transition('new_name', 'say_hello', 'enter_name')  # Если имя новое, переходим в состояние ожидания нового имени
        self.machine.add_transition('old_name', 'say_hello', 'go_to_main_menu')  # Если имя старое, переходим в состояние отображения меню
        self.machine.add_transition('name_entered', 'enter_name', 'go_to_main_menu')  # Если имя введено, переходим в состояние отображения меню