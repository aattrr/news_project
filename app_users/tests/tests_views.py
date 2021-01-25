from _csv import reader
from django.test import TestCase
from django.urls import reverse
from app_users.models import News, Profile, Picture
from django.contrib.auth.models import User, Permission
from django.core.files.uploadedfile import SimpleUploadedFile


NUMBER_OF_ITEMS = 20
WORD_OF_ITEMS = ['Квас', 'Жук', 'Камень', 'Круглый остров', 'Весёлый дрон', 'Дерево', 'Буксировщик', 'Сало', 'Ар', 'Хор']


class NewsListPageTest(TestCase):
    ''' Тестируем страницу со списком новостей '''
    @classmethod
    def setUpTestData(cls):
        # Создаем и заполняем базу для тестирования
        user_for_test = User.objects.create_user(username='testuser', email='fifa@fa.ru', password='testqqqq')
        for word in WORD_OF_ITEMS:
            News.objects.create(
                user=user_for_test,
                title=word,
                description='The time of sunset is defined in astronomy as the moment when the upper limb of',
                status=True
            )

    def test_news_list_page(self):
        ''' Тестируем Доступ страницы и наличие правильного шаблона '''
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/news_list.html')

    def test_items_in_template(self):
        ''' Тестируем Наличие списка на странице '''
        response = self.client.get(reverse('news_list'))
        self.assertTrue(len(response.context['object_list']) == len(WORD_OF_ITEMS))


class NewsDetailPageTest(TestCase):
    ''' Тестируем страницу описания новости '''
    @classmethod
    def setUpTestData(cls):
    # Создаем и заполняем базу для тестирования
        user_for_test = User.objects.create_user(username='testuser', email='fifa@fa.ru', password='testqqqq')
        for word in WORD_OF_ITEMS:
            News.objects.create(
                user=user_for_test,
                title=word,
                description='The time of sunset is defined in astronomy as the moment when the upper limb of',
                status=True
            )

    def test_news_detail_page(self):
        first_test_news = News.objects.first()
        id_news = first_test_news.id    # Получаем id первой новости
        response = self.client.get(reverse('news_detail', kwargs={'pk': id_news}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/news_detail.html')


class AddCommentPageTest(TestCase):
    ''' Тестируем страницу добавления комментария '''
    @classmethod
    def setUpTestData(cls):
        # Создаем и заполняем базу для тестирования
        user_for_test = User.objects.create_user(username='testuser', email='fifa@fa.ru', password='testqqqq')
        for word in WORD_OF_ITEMS:
            News.objects.create(
                user=user_for_test,
                title=word,
                description='The time of sunset is defined in astronomy as the moment when the upper limb of',
                status=True
            )

    def test_add_comment_page(self):
        # Тестируем Доступ страницы и наличие правильного шаблона
        first_test_news = News.objects.first()
        id_news = first_test_news.id  # Получаем id первой новости
        response = self.client.get(reverse('add_comment', kwargs={'pk': id_news}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/add_comment.html')


class AddNewsPageTest(TestCase):
    ''' Тестируем страницу добавления новости '''
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя testuser1 без прав
        test_user1 = User.objects.create_user(username='testuser1', password='testqqqq')
        test_user1.save()
        # Создаем пользователя testuser2 c наличием прав на добавление новости
        test_user2 = User.objects.create_user(username='testuser2', password='testqqqq')
        test_user2.save()
        permission = Permission.objects.get(codename='add_news')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_add_news_page_for_has_perm_user(self):
        # Тестируем возможность добавления новости пользователем имеющим на это права
        login = self.client.login(username='testuser2', password='testqqqq')
        response = self.client.get(reverse('add_news'))
        self.assertEqual(response.status_code, 200)

    def test_add_news_page_for_has_not_perm_user(self):
        # Тестируем отсутствие возможности добавления новости пользователем не имеющим на это права
        login = self.client.login(username='testuser1', password='testqqqq')
        response = self.client.get(reverse('add_news'))
        self.assertEqual(response.status_code, 403)


class LoginPageTest(TestCase):
    '''Тестируем страницу авторизации'''
    def test_login_page(self):
        # Тестируем Доступ страницы и наличие правильного шаблона
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djfiles/login.html')


class EditNewsPageTest(TestCase):
    ''' Тестируем страницу изменения новости '''
    @classmethod
    def setUpTestData(cls):
    # Создаем и заполняем базу для тестирования
        user_for_test = User.objects.create_user(username='testuser', email='fifa@fa.ru', password='testqqqq')
        for word in WORD_OF_ITEMS:
            News.objects.create(
                user=user_for_test,
                title=word,
                description='The time of sunset is defined in astronomy as the moment when the upper limb of',
                status=True
            )

    def test_edit_news_page(self):
        first_test_news = News.objects.first()
        id_news = first_test_news.id  # Получаем id первой новости
        # Тестируем Доступ страницы и наличие правильного шаблона
        response = self.client.get(reverse('edit_news', kwargs={'pk': id_news}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/edit_news.html')


class DeletePicturePageTest(TestCase):
    ''' Тестируем страницу удаления новости '''
    @classmethod
    def setUpTestData(cls):
    # Создаем и заполняем базу для тестирования
        user_for_test = User.objects.create_user(username='testuser', password='testqqqq')
        for word in WORD_OF_ITEMS:
            News.objects.create(
                user=user_for_test,
                title=word,
                description='The time of sunset is defined in astronomy as the moment when the upper limb of',
                status=True
            )
        first_test_news = News.objects.first()
        Picture.objects.create(
            image=SimpleUploadedFile(name='01.jpg', content=open('image/image/01.jpg', 'rb').read(),
                                        content_type='image/jpg'),
            news=first_test_news,
        )

    def test_delete_picture_page(self):
        # Тестируем Доступ страницы и наличие правильного шаблона
        u = self.client.login(username='testuser', password='testqqqq')
        first_test_news = News.objects.first()  # Получаем первую новость
        id_news = first_test_news.id  # Получаем id первой новости
        test_picture = Picture.objects.first()  # Получаем единственную картинку
        id_picture = test_picture.id    # Получаем id первой картинки
        data = {
            'pk': id_news,
            'checks': id_picture
        }
        response = self.client.post(reverse('delete_picture'), data={'checks': id_picture}, kwargs={'pk': id_news})

        self.assertEqual(response.status_code, 200)


class RegisterPageTest(TestCase):
    '''Тестируем страницу регистрации пользователя'''
    def test_register_page(self):
        # Тестируем Доступ страницы и наличие правильного шаблона
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djfiles/register.html')


class LoadFilesPageTest(TestCase):
    '''Тестируем страницу загрузки файла'''
    @classmethod
    def setUpTestData(cls):
    # Создаем пользователя и файл для тестирования
        test_user1 = User.objects.create_user(username='testuser8', password='testqqqq')
        test_user1.save()

    def test_load_files_page(self):
        # Тестируем Доступ страницы и наличие правильного шаблона
        self.client.login(username='testuser8', password='testqqqq')

        # В load_file должен появиться информационный текст
        response_get_load_file = self.client.get(reverse('load_file'))
        self.assertContains(response_get_load_file, 'Чтобы загрузить новости необходимо использовать .csv файл')

        f = SimpleUploadedFile(name='news.csv', content=open('image/image/news.csv', 'rb').read(),
                               content_type='text/csv')

        response = self.client.post(reverse('load_file'),  data={'file': f})   #Тестируем загрузку файлов
        self.assertEqual(response.status_code, 200)

        response_get_news_list = self.client.get(reverse('news_list'))
        self.assertContains(response_get_news_list, 'Салют опасен для глаз')      # В news_list должны появиться новости из csv-файла


class PersonalInfPageTest(TestCase):
    ''' Тестируем страницу добавления новости '''
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя testuser3 без прав
        test_user3 = User.objects.create_user(username='testuser3', password='testqqqq')
        test_user3.save()

    def test_personal_inf_page_for_anonym_user(self):
        # Тестируем доступ к странице пользовательской информации для НЕавторизованного пользователя
        response = self.client.get(reverse('personal_inf'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вы не авторизованы, авторизуйтесь чтобы посмотреть информацию о пользователе')

    def test_personal_inf_page_for_authorize_user(self):
        # Тестируем доступ к странице пользовательской информации для авторизованного пользователя
        login = self.client.login(username='testuser3', password='testqqqq')
        response = self.client.get(reverse('personal_inf'))
        self.assertEqual(response.status_code, 200)


class EditProfilePageTest(TestCase):
    '''Тестируем страницу изменения профиля пользователя'''
    @classmethod
    def setUpTestData(cls):
    # Создаем пользователя testuser3
        user_for_test = User.objects.create_user(username='testuser3', email='fifa@fa.ru', password='testqqqq')
        Profile.objects.create(
            user=user_for_test,
            about_me='Обычный парень не лишен простоты',
            check=True
        )

    def test_edit_profile_page_for_authorize_user(self):
        # Тестируем возможность редактрования пользовательских данных авторизованным пользователем
        login = self.client.login(username='testuser3', password='testqqqq')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page_for_anonym_user(self):
        # Тестируем возможность редактрования пользовательских данных НЕавторизованным пользователем
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вы не авторизованы, авторизуйтесь чтобы посмотреть информацию о пользователе')


class MainPageTest(TestCase):
    '''Тестируем страницу регистрации пользователя'''
    def test_main_page(self):
        # Тестируем Доступ страницы и наличие правильного шаблона
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djfiles/main.html')
