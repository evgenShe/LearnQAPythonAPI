class TestCheckLenPhrase:
    def test_check_phrase_len(self):
        phrase = input("Set a phrase: ")
        print(phrase)
        assert len(phrase) < 15, "Phrase with wrong length"
