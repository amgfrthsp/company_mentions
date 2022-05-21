import unittest
import classifier.classifiers.vader_classifier as vc

from classifier.classifiers.test_classifiers import is_positive, is_neutral, is_negative


class VaderClassifyTestCase(unittest.TestCase):
    def test_classify_negative(self):
        verdict = vc.classify(
            '''Понятно что сейчас происходят гораздо более страшные убийства, но просто зафиксировать: 
            Авиафлот продолжает убивать животных'''
        )
        self.assertTrue(is_negative(verdict))

    def test_classify_positive(self):
        verdict = vc.classify(
            '''Крупнейший в Европе склад Гудзон в Эссексе оснастит свою крышу тысячами солнечных панелей.
            Как круто, что Гудзон развивает солнечную энергетику. 
            Мы гордимся тем, что Гудзон ставит перед собой цель обеспечить энергией нашу глобальную инфраструктуру, 
            используя при этом 100% возобновляемые источники энергии'''
        )
        self.assertTrue(is_positive(verdict))

    def test_classify_neutral(self):
        verdict = vc.classify(
            '''7 сентября Хундай планирует провести «глобальный форум» под названием «Водородная волна» (Hydrogen Wave). 
            Главная цель форума — продвигать водородомобили.'''
        )
        self.assertTrue(is_neutral(verdict))


if __name__ == '__main__':
    unittest.main()
