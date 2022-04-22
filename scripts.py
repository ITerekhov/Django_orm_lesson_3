import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)


def fix_marks(schoolkid_full_name: str):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    child_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    child_marks.update(points=random.randint(4, 5))


def remove_chastisements(schoolkid_full_name: str):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    child_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisement.delete()


def create_commendation(schoolkid_full_name: str, subject_title: str):
    commendation_variants = ['хвалю', 'восхваляю', 'красавчик', 'молодец', 'просто гений']
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    lesson = Lesson.objects.filter(subject__title__contains=subject_title,
                                   subject__year_of_study=schoolkid.year_of_study).last()
    Commendation.objects.create(schoolkid=schoolkid, subject=lesson.subject,
                                teacher=lesson.teacher, created=lesson.date,
                                text=random.choice(commendation_variants))