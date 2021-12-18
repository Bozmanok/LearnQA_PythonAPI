class TestShortPhrase:
    def test_check_short_phrase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) < 15, "Фраза состоит из 15-ти или более символов"
