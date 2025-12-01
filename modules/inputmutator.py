import random
import string
from core import logger


class InputMutator:

    def __init__(self):
        self.special_chars = [
            "'", "\"", ";", "<", ">", "(", ")", "{", "}", "[", "]",
            "%", "$", "#", "!", "@", "/", "\\", "|", "&", "*", "+"
        ]

        self.injection_payloads = [
            "' OR '1'='1",
            "\" OR \"1\"=\"1",
            "'; DROP TABLE users; --",
            "<script>alert(1)</script>",
            "../../etc/passwd",
            "' UNION SELECT NULL --",
            "' OR sleep(5)--"
        ]


    def random_string(self, length=12):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def mutate_special(self, text):
        if not text:
            return random.choice(self.special_chars)

        index = random.randint(0, len(text)-1)
        char = random.choice(self.special_chars)
        return text[:index] + char + text[index+1:]

    def add_injection(self, text):
        payload = random.choice(self.injection_payloads)
        return f"{text}{payload}"

    def full_mutate(self, text):
        choice = random.choice(["special", "inject", "random"])

        if choice == "special":
            return self.mutate_special(text)
        elif choice == "inject":
            return self.add_injection(text)
        else:
            return self.random_string(20)

    def mutate_list(self, inputs):
        mutated = []
        for item in inputs:
            mutated.append(self.full_mutate(item))
        return mutated

    def calistir(self, input_value):
        logger.bilgi("Input Mutator çalışıyor...")
        sonuc = self.full_mutate(input_value)
        logger.başarı(f"Mutasyona uğratılmış değer: {sonuc}")
        return sonuc