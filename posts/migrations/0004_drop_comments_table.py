from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0003_alter_post_cover_image_alter_post_html_cache_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS comments CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="DELETE FROM django_migrations WHERE app = 'comments';",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
