from django.contrib import admin

from .models import Article, News, Paragraph


class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(News)
