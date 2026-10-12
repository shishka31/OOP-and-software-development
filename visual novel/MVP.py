
class Character:

    def __init__(self, name):
        self.name = name

    def say(self, text):
        print(f"\n{self.name}: {text}")


class VisualNovel:

    print("Введите имя: ")

    mc_name = input().strip()

    def __init__(self):
        self.hero_name = self.mc_name
        self.doctor = Character("Доктор Кобсон")

    def show_scene(self, title, description):
        print("\n" + "=" * 40)
        print(title.upper())
        print("=" * 40)
        print(description)

    def start(self):
        self.show_scene(
            "Сцена 1",
            "Поздний вечер. На тускло освещённой улице никого нет.\n"
            "Дождь стучит по карнизам крыш, а на часах 23:55.\n"
            "Поодаль от жилых домов особняком расположено неприметное здание с заколоченными окнами.\n\n"
            f"{self.hero_name} стоит перед ним со скомканным объявлением в руке, не решаясь зайти внутрь через массивную металлическую дверь."
        )

        input("\nНажми Enter, чтобы продолжить...")

        self.show_scene(
            "Сцена 2",
            f"Вдруг дверь распахивается, и в тусклом свете {self.hero_name} замечает фигуру мужчины.\n"
            "Лабораторный халат, надетый поверх затасканной футболки, выдаёт в нём врача."
        )

        self.doctor.say(
            f"Приветствую, юноша. Меня зовут {self.doctor.name}. Вы, должно быть, мистер {self.hero_name}?"
        )

        self.doctor.say(
            "Я очень рад, что вы откликнулись на моё объявление. Новых сотрудников в нашу клинику сейчас найти непросто..."
        )

        self.doctor.say(
            "Прошу, проходите."
        )

        print(
            f"\n{self.doctor.name} зловеще улыбается. {self.hero_name} чуствует, как по его спине пробегает холодок."
        )

        input("\nНажми Enter, чтобы продолжить...")

        self.show_scene(
            "Сцена 3",
            "Жуткий вид доктора, стоящего в дверном проёме казалось бы заброшенного здания, не вызывает ничего, кроме тревоги.\n"
            "Однако стоит ли из-за этого отказаться от столь удачно подвернувшейся работы? "
            f"{self.hero_name} смотрит на объявление в своей руке, а затем на доктора.\n\n"
            "1. Зайти внутрь.\n"
            "2. Отказаться и уйти."
        )

        choice = self.get_choice()

        if choice == "1":
            self.main_route()
        else:
            self.alt_route()

    def get_choice(self):
        while True:
            choice = input("\nТвой выбор (1 или 2): ").strip()

            if choice in ("1", "2"):
                return choice

            print("Пожалуйста, введи 1 или 2.")

    def main_route(self):

        self.show_scene(
            "Концовка 1",
            f"{self.hero_name} колеблется, но всё же заходит в 'клинику'.\n"
            f"{self.doctor.name} закрывает за ним дверь."
        )

        self.doctor.say(
            "Очень хорошо. Что ж, пора мне познакомить вас с нашими пациенами."
        )

        print(
            f"\nВ помещении резко включается свет, и {self.hero_name} видит перед собой пробирающую до дрожи картину..."
        )

        self.doctor.say(
            "Надеюсь, вы поладите."
        )

        print(
            "\nС лица доктора не сходит зловещая улыбка.\n"
            f"\n{self.hero_name} понимает, что найденная им работа была явно не тем, чем казалась."
        )

        print("\nКОНЕЦ")

    def alt_route(self):
        self.show_scene(
            "Концовка 2",
            f"{self.hero_name} крепко сжимает объявление."
        )

        print(
            f"\n{self.hero_name}: Простите, но я передумал."
        )

        self.doctor.say(
            "Что ж... Работать ты здесь не будешь, но это не значит, что ты сможешь отсюда сбежать."
        )

        print(
            f"\n{self.hero_name} замечает, как {self.doctor.name} выхватывает что-то из кармана своего халата, но не успевает среагировать.\n"
            f"Раздаётся хлопок. {self.hero_name} чувствует, как земля уходит у него из-под ног, а в глазах темнеет."
        )

        print(
            "\nПоследнее, что он успевает разглядеть перед полным погружением в темноту -- "
            f"{self.doctor.name} затаскивает его за ноги вглубь помещения..."
        )

        print("\nКОНЕЦ")


game = VisualNovel()
game.start()
