import pytest

from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    @pytest.mark.parametrize("name,delta", [
    ("", 0),
    ("A", 1),
    ("X" * 40, 1),
    ("Y" * 41, 0),
    ])
    def test_add_new_book_length_rules(self, name, delta):
        collector = BooksCollector()
        initial_count = len(collector.books_genre)
        collector.add_new_book(name)
        assert len(collector.books_genre) == initial_count + delta



    def test_set_book_genre_success(self):
        # 1. Создаём объект
        collector = BooksCollector()
        
        # 2. Готовим данные: добавляем книгу и ставим ей ПРАВИЛЬНЫЙ жанр
        book_name = "Дюна"
        valid_genre = "Фантастика"  # Этот жанр точно есть в списке self.genre
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, valid_genre)
        
        # 3. ОДИН assert: проверяем, что жанр установился верно
        assert collector.get_book_genre(book_name) == valid_genre


    def test_get_book_genre_returns_correct_value(self):
        collector = BooksCollector()
        book_name = "Властелин колец"
        valid_genre = "Фантастика"
        
        # Подготовка данных: книга должна существовать и иметь жанр
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, valid_genre)
        
        # ОДИН assert: проверяем, что вернули то, что ожидали
        assert collector.get_book_genre(book_name) == valid_genre

    
    @pytest.mark.parametrize("genre, expected_books", [
    ("Фантастика", ["Дюна", "Основание"]),
    ("Мультфильмы", []),
    ])
    def test_get_books_with_specific_genre_filtering(self, genre, expected_books):
        collector = BooksCollector()

        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")

        collector.add_new_book("Основание")
        collector.set_book_genre("Основание", "Фантастика")

        # Один assert: сравниваем списки целиком
        assert collector.get_books_with_specific_genre(genre) == expected_books



    
    def test_get_books_genre_returns_full_dict(self):
        collector = BooksCollector()
        
        # 1. Добавляем несколько книг и ставим им жанры
        collector.add_new_book("Книга А")
        collector.set_book_genre("Книга А", "Фантастика")
        
        collector.add_new_book("Книга Б")
        collector.set_book_genre("Книга Б", "Комедии")
        
        # 2. Получаем словарь целиком
        result = collector.get_books_genre()
        
        # 3. ОДИН assert: сравниваем полученный словарь с ожидаемым
        expected = {
            "Книга А": "Фантастика",
            "Книга Б": "Комедии"
        }
        
        assert result == expected


    def test_get_books_for_children_excludes_adult_genre(self):
        collector = BooksCollector()  # Не забудь создать объект!
        
        # 1. Добавляем книгу для детей
        collector.add_new_book("KidsBook")
        collector.set_book_genre("KidsBook", "Мультфильмы")

        # 2. Добавляем «взрослую» книгу (Ужасы есть в genre_age_rating)
        collector.add_new_book("AdultBook")
        collector.set_book_genre("AdultBook", "Ужасы")

        # 3. Получаем список книг для детей
        children_books = collector.get_books_for_children()
        
        # 4. ОДИН assert: проверяем, что взрослая книга НЕ попала в список
        assert "AdultBook" not in children_books
    
    
    def test_add_book_in_favorites_works(self):
        collector = BooksCollector()
        book_name = "Гарри Поттер"
        
        # Книга должна быть в словаре, чтобы попасть в избранное
        collector.add_new_book(book_name)
        
        # Добавляем в избранное
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что она там
        assert book_name in collector.get_list_of_favorites_books()


    def test_delete_book_from_favorites_works(self):
        collector = BooksCollector()
        book_name = "Хоббит"
        
        # Подготовка: книга должна быть в словаре и в избранном
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Удаляем из избранного
        collector.delete_book_from_favorites(book_name)
        
        # Проверяем, что её больше нет в списке
        assert book_name not in collector.get_list_of_favorites_books()


    def test_get_list_of_favorites_books_not_empty(self):
        # 1. Создаём чистый объект для этого теста
        collector = BooksCollector()
        
        # 2. Готовим данные: книга должна быть в словаре, чтобы попасть в избранное
        collector.add_new_book("F1")
        
        # 3. Добавляем в избранное
        collector.add_book_in_favorites("F1")
        
        # 4. Получаем список избранного
        favorites = collector.get_list_of_favorites_books()
        
        # 5. ОДИН assert: проверяем, что книга там есть
        assert "F1" in favorites
