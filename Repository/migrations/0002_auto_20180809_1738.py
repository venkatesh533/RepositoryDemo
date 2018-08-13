# Generated by Django 2.0 on 2018-08-09 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryFiles',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Repository.BaseContent')),
                ('repo_image', models.ImageField(blank=True, null=True, upload_to='Images/%Y/%m/%d')),
                ('repo_audio', models.FileField(blank=True, null=True, upload_to='Audios/%Y/%m/%d')),
                ('repo_video', models.FileField(blank=True, null=True, upload_to='Videos/%Y/%m/%d')),
            ],
            bases=('Repository.basecontent',),
        ),
        migrations.RenameField(
            model_name='repository',
            old_name='rep_id',
            new_name='repo_id',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='rep_audio',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='rep_image',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='rep_video',
        ),
        migrations.AddField(
            model_name='repositoryfiles',
            name='repo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Repository.Repository'),
        ),
    ]
