from django.db import models

class Book(models.Model):
    local_path = models.CharField(max_length=4096, blank=True)#4096 is the linux file path limit
    remote_url = models.CharField(max_length=32000, blank=True)#32000 is the firefox url char limit
    viewer_path = models.CharField(max_length=4096, blank=True)

    class Meta:
        ordering = ['local_path']
    
    def __str__(self):
        return self.local_path

class AvailableBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True)
    author = models.CharField(max_length=1000, blank=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class SingletonModel(models.Model):
    '''
    base class to use for table with one row to store app settings
    '''
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class bookapiUserSettings(SingletonModel):
    source_ip = models.CharField(max_length=255, blank=True)
    source_script_path = models.CharField(max_length=4096, blank=True)
    source_viewer_base_url = models.CharField(max_length=32000, blank=True)

    def __str__(self):
        return "bookapiUserSettings"

    class Meta:
        verbose_name = "Book API User Setting"

class bookapiSourceFiles(SingletonModel):
    source_json = models.TextField(blank=True)

    def __str__(self):
        return "bookapiSourceFiles"

    class Meta:
        verbose_name = "Book API Source File"
