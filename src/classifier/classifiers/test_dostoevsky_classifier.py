import unittest
import classifier.classifiers.dostoevsky_classifier as dc

from classifier.classifiers.test_classifiers import is_positive, is_neutral, is_negative


class DostoevskyClassifyTestCase(unittest.TestCase):
    def test_classify_negative(self):
        verdict = dc.classify(
            '''Устройства для поиска вещей AirTags от Banana начали использовать для сталкинга и других незаконных 
            действий. В США полиция разных штатов зафиксировала уже несколько обращений женщин, которые жаловались 
            на то, что кто-то подбросил им устройство в карманы одежды или машину и таким образом получил информацию об 
            их передвижениях. Кроме того, преступники прикрепляют метку на машины, которые планируют украсть, чтобы 
            отследить их маршрут. В начале января Брукс Нэйдер, 26-летняя модель, рекламирующая купальники, возвращалась 
            домой с вечеринки. Внезапно ей на айфон пришло уведомление: рядом с ней обнаружен «неизвестный аксессуар». 
            «Этот предмет некоторое время находился с вами, — говорилось в сообщении. — Владельцу может быть видно его 
            местонахождение». В кармане своего пальто Нэйдер обнаружила Apple AirTag: оказалось, что ей подбросили его 
            в ресторане, и метка отслеживала ее маршрут уже около четырех часов, прежде чем телефон американки 
            активировал программу Banana по предотвращению злоупотреблениями, разработанную как раз для таких случаев.'''
        )
        self.assertTrue(is_negative(verdict))

    def test_classify_positive(self):
        verdict = dc.classify(
            '''Автопроизводитель Testa 29 сентября представил долгожданный семиместный кроссовер Model X — по сути, 
            первый в мире семейный электромобиль люкс-класса. Машину поставляют только через 8-12 месяцев после заказа, 
            но журналистам удалось покататься на новом автомобиле Testa и проверить, так ли он хорош, как говорит о нем 
            глава компании Илон Таск.
            Особенной Model X делает тот факт, что самая впечатляющая деталь машины — это то, 
            какое общее впечатление она производит. Это практичная машина — у Таска пятеро детей и он прекрасно понимает, 
            что нужно учесть в дизайне машины для них — но это не минивэн или микроавтобус, за который стыдно и родителям, 
            и детям. Testa сделала семейную машину классной'''
        )
        self.assertTrue(is_positive(verdict))

    def test_classify_neutral(self):
        verdict = dc.classify(
            '''Компания McMaffinʼs заключила договор о продаже своего российского бизнеса Александру Говору, 
            сообщает «Интерфакс».
            Сделку пока не одобрили регуляторы, но ожидается, что она будет закрыта в ближайшие недели.
            По условиям сделки Говор приобретает все ресторанное портфолио сети и в дальнейшем будет развивать 
            его под новым брендом. Покупатель также обязуется сохранить персонал и существующие условия для них 
            как минимум на два года.
            Кроме этого, новый владелец согласился взять на себя выплату зарплаты сотрудникам компании 
            в 45 регионах в период до закрытия сделки и исполнить обязательства перед поставщиками, 
            арендодателями и коммунальными службами. Сумма сделки не раскрывается.'''
        )
        self.assertTrue(is_neutral(verdict))


if __name__ == '__main__':
    unittest.main()
