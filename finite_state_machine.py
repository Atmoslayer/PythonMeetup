from transitions import Machine


class PythonMeetupBot(object):
    states = ['say_hello', 'enter_name', 'select_a_section', 'go_to_programs',
              'go_to_questions', 'go_to_my_questions', 'go_to_settings',
              'select_program', 'select_description', 'select_question', 'select_speaker']

    def __init__(self, name):
        self.machine = Machine(model=self, states=PythonMeetupBot.states, initial='say_hello')
        self.name = name
        self.machine.add_transition('new_name', 'say_hello', 'enter_name')  # Если имя новое, переходим в состояние ожидания нового имени
        self.machine.add_transition('old_name', 'say_hello', 'select_a_section')  # Если имя старое, отображаем меню и ждём выбора раздела
        self.machine.add_transition('name_entered', 'enter_name', 'select_a_section')  # Если имя введено, переходим в состояние отображения меню
        self.machine.add_transition('programs', 'select_a_section', 'go_to_programs')
        self.machine.add_transition('questions', 'select_a_section', 'go_to_questions')
        self.machine.add_transition('my_questions', 'select_a_section', 'go_to_my_questions')
        self.machine.add_transition('settings', 'select_a_section', 'go_to_settings')
        self.machine.add_transition('program_selected', 'go_to_programs', 'select_program')
        self.machine.add_transition('description_selected', 'select_program', 'select_description')
        self.machine.add_transition('program_selected', 'go_to_questions', 'select_question')
        self.machine.add_transition('question_selected', 'select_question', 'select_speaker')