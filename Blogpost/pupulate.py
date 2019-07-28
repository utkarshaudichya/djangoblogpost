import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Blogpost.settings")
django.setup()

from faker import Faker
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
import random

def create_post(n):
    try:
        faker = Faker()
        for _ in range(n):
            id = random.randint(1, 4)
            _title = faker.name()
            _slug = '-'.join(_title.lower().split())
            _author = User.objects.get(id__exact=id)
            _body = faker.text()
            _publish = timezone.now()
            _created = timezone.now()
            _updated = timezone.now()
            _status = random.choice(['published', 'draft'])
            Post.objects.create(title=_title, slug=_slug, author=_author, body=_body, publish=_publish, created=_created, updated=_updated, status=_status)
    except Exception as e:
        print(e)
    finally:
        total_post = Post.objects.count()
        if(total_post < total_post+n+1):
            create_post(20)

create_post(20)
print("------------------------------\nPopulate Data Sucessfully\n---------------------------------")
