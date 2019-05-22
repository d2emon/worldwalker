from .screen import Screen


class UserScreen(Screen):
    @classmethod
    def input_field(cls, **kwargs):
        try:
            value = kwargs.get('value')
            new_value = input("{}(Currently {} ):".format(kwargs.get('label'), kwargs.get('value')))[:128]
            if not new_value:
                return value
            if new_value[0] == ".":
                return value
            if "." in new_value:
                raise ValueError("\nInvalid Data Field\n")
            return new_value
        except ValueError as e:
            cls.show_message(e)
            return cls.input_field(**kwargs)

    @classmethod
    def input_username(cls):
        cls.before_data()
        return input("\nUser Name:")[:79]

    @classmethod
    def before_data(cls, **kwargs):
        cls.show(**kwargs)

    @classmethod
    def show_data(cls, **kwargs):
        """
        for show user and edit user

        :return:
        """
        user = kwargs.get('user')
        if user is None:
            print()
            print("No user registered in that name")
            print()
            print()
            return
        print()
        print()
        print("User Data For {}".format(user.username))
        print()
        print("Name:{}".format(user.username))
        print("Password:{}".format(user.password))

    @classmethod
    def show_edit(cls, **kwargs):
        user = kwargs.get('user')
        print()
        print("Editing : {}".format(user.username))
        print()


class MainScreen(UserScreen):
    @classmethod
    def show(cls, **kwargs):
        super().show(**kwargs)
        print("Welcome To AberMUD II [Unix]")
        print()
        print()
        print("Options")
        print()
        print("1]  Enter The Game")
        print("2]  Change Password")
        print()
        print()
        print("0] Exit AberMUD")
        print()
        print()
        if kwargs.get('admin'):
            print("4] Run TEST game")
            print("A] Show persona")
            print("B] Edit persona")
            print("C] Delete persona")
        print()
        print()
        print("Select > ")

    @classmethod
    def input_option(cls):
        return input()[:2].lower()

    @classmethod
    def input_old_password(cls):
        print()
        return input("Old Password")

    @classmethod
    def input_new_password(cls):
        value = input("*")
        print()
        return value

    @classmethod
    def input_verify_password(cls):
        print()
        print("Verify Password")
        value = input("*")
        print()
        return value

    @classmethod
    def input_wait(cls):
        print()
        input("Hit Return...\n")

    @classmethod
    def request_new_password(cls):
        print()
        print("New Password")

    @classmethod
    def before_data(cls, **kwargs):
        pass

    @classmethod
    def show_data(cls, **kwargs):
        pass
