import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)
                               
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def fix_marks(schoolkid_full_name: str):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    except MultipleObjectsReturned:
        if not schoolkid_full_name:
            print('Кажется ты забыл указать имя')
        else:   
            print('Нашлось больше одного человека с такими данными. Попробуй уточнить запрос')
        return None
    except ObjectDoesNotExist:
        print(f'{schoolkid_full_name} нет в списке учеников. Может опечатка?')
        return None
    child_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    child_marks.update(points=random.randint(4, 5))


def remove_chastisements(schoolkid_full_name: str):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    except MultipleObjectsReturned:
        if not schoolkid_full_name:
            print('Кажется ты забыл указать имя')
        else:   
            print('Нашлось больше одного человека с такими данными. Попробуй уточнить запрос')
        return None
    except ObjectDoesNotExist:
        print(f'{schoolkid_full_name} нет в списке учеников. Может опечатка?')
        return None
    child_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisement.delete()


def create_commendation(schoolkid_full_name: str, subject_title: str):
    commendation_variants = ['хвалю', 'восхваляю', 'красавчик', 
                             'молодец', 'просто гений']
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
        subject = Subject.objects.get(title__contains=subject_title,
                                      year_of_study=schoolkid.year_of_study)
    except MultipleObjectsReturned:
        if not schoolkid_full_name:
            print('Кажется ты забыл указать имя')
        elif not subject_title:
            print('Кажется ты забыл указать предмет')
        else:
            print('Нашлось больше одного человека с такими данными. Попробуй уточнить запрос')
        return None
    except ObjectDoesNotExist:
        if not Subject.objects.filter(title__contains=subject_title).exists():
            print(f'{subject_title} в списке предметов нет. Может опечатка?')
        else:
            print(f'{schoolkid_full_name} нет в списке учеников. Может опечтака?')
        return None
    lesson = Lesson.objects.filter(subject=subject,
                                   subject__year_of_study=schoolkid.year_of_study).last()
    Commendation.objects.create(schoolkid=schoolkid, subject=subject,
                                teacher=lesson.teacher, created=lesson.date,
                                text=random.choice(commendation_variants))
