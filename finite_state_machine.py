from transitions import Machine


class PythonMeetupBot(object):
    states = ['initial', 'say_hello', 'enter_name', 'go_to_main_menu', 'select_a_section', 'go_to_programs',
              'go_to_questions', 'go_to_my_questions', 'go_to_settings']

    def __init__(self, name):
        self.machine = Machine(model=self, states=PythonMeetupBot.states, initial='say_hello')
        self.name = name
        # self.machine.add_transition('get_started', 'initial', 'say_hello')  # Переводим бота в стартовое состояние
        self.machine.add_transition('new_name', 'say_hello', 'enter_name')  # Если имя новое, переходим в состояние ожидания нового имени
        self.machine.add_transition('old_name', 'say_hello', 'select_a_section')  # Если имя старое, отображаем меню и ждём выбора раздела
        self.machine.add_transition('name_entered', 'enter_name', 'go_to_main_menu')  # Если имя введено, переходим в состояние отображения меню
        self.machine.add_transition('main_menu', 'go_to_main_menu', 'select_a_section')  # Зашли в главное меню, ожидаем выбора
        self.machine.add_transition('programs', 'select_a_section', 'go_to_programs')
        self.machine.add_transition('questions', 'select_a_section', 'go_to_questions')
        self.machine.add_transition('my_questions', 'select_a_section', 'go_to_my_questions')
        self.machine.add_transition('settings', 'select_a_section', 'go_to_settings')