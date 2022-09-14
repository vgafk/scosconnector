class ClassNotExists(Exception):
    def __str__(self):
        return 'Такого класса не существует'
