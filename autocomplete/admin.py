import string, operator
from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.text import get_text_list, truncate_words
from django.utils.translation import ugettext as _


js_tuple = (
    'js/jquery.js',
    'js/jquery.bgiframe.min.js',
    'js/jquery.ajaxQueue.js',
    'js/jquery.autocomplete.js'
)

css_dict = {
    'all': ('css/django-autocomplete.css',)
}

class BaseAutocompleteWidget(ForeignKeyRawIdWidget):
    widget_template = None
    search_path = '../foreignkey_autocomplete/'
    
    class Media:
        css             = css_dict
        js              = js_tuple
        abstract        = True
    
    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        obj = self.rel.to._default_manager.get(**{key: value})
        return truncate_words(obj, 14)
    

class ForeignKeySearchWidget(BaseAutocompleteWidget):    
    def __init__(self, rel, search_fields, attrs=None):
        self.search_fields = search_fields
        super(ForeignKeySearchWidget, self).__init__(rel, attrs)
    
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        opts = self.rel.to._meta
        app_label = opts.app_label
        model_name = opts.object_name.lower()
        related_url = '../../../%s/%s/' % (app_label, model_name)
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        output = [forms.TextInput.render(self, name, value, attrs)]
        if value:
            label = self.label_for_value(value)
        else:
            label = u''
        context = {
            'url': url,
            'related_url': related_url,
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
            'search_path': self.search_path,
            'search_fields': ','.join(self.search_fields),
            'model_name': model_name,
            'app_label': app_label,
            'label': label,
            'name': name,
        }
        output.append(render_to_string(self.widget_template or (
            '%s/%s/%s' % (app_label, model_name, 'fk_widget.html'),
            '%s/%s' % (app_label, 'fk_widget.html'),
            'admin/autocomplete/%s' % 'fk_widget.html',
        ), context))
        output.reverse()
        return mark_safe(u''.join(output))

class NoLookupsForeignKeySearchWidget(BaseAutocompleteWidget):    
    def __init__(self, rel, search_fields, attrs=None):
        self.search_fields = search_fields
        super(NoLookupsForeignKeySearchWidget, self).__init__(rel, attrs)
        
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        opts = self.rel.to._meta
        app_label = opts.app_label
        model_name = opts.object_name.lower()
        related_url = '../../../%s/%s/' % (app_label, model_name)
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        output = [forms.TextInput.render(self, name, value, attrs)]
        if value:
            label = self.label_for_value(value)
        else:
            label = u''
        context = {
            'url': url,
            'related_url': related_url,
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
            'search_path': self.search_path,
            'search_fields': ','.join(self.search_fields),
            'model_name': model_name,
            'app_label': app_label,
            'label': label,
            'name': name,
        }
        output.append(render_to_string(self.widget_template or (
            '%s/%s/%s' % (app_label, model_name, 'nolookups_fk_widget.html'),
            '%s/%s' % (app_label, 'nolookups_fk_widget.html'),
            'admin/autocomplete/%s' % 'nolookups_fk_widget.html',
        ), context))
        output.reverse()
        return mark_safe(u''.join(output))

class InlineForeignKeySearchWidget(BaseAutocompleteWidget):    
    def __init__(self, rel, search_fields, attrs=None):
        self.search_fields = search_fields
        super(InlineForeignKeySearchWidget, self).__init__(rel, attrs)
        
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        opts = self.rel.to._meta
        app_label = opts.app_label
        model_name = opts.object_name.lower()
        related_url = '../../../%s/%s/' % (app_label, model_name)
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        output = [forms.TextInput.render(self, name, value, attrs)]
        if value:
            label = self.label_for_value(value)
        else:
            label = u''
        context = {
            'url': url,
            'related_url': related_url,
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
            'search_path': self.search_path,
            'search_fields': ','.join(self.search_fields),
            'model_name': model_name,
            'app_label': app_label,
            'label': label,
            'name': name,
        }
        output.append(render_to_string(self.widget_template or (
            '%s/%s/%s' % (app_label, model_name, 'inline_widget.html'),
            '%s/%s' % (app_label, 'inline_widget.html'),
            'admin/autocomplete/%s' % 'inline_widget.html',
        ), context))
        output.reverse()
        return mark_safe(u''.join(output))

class BaseAutocompleteAdminMixin(object):
    related_search_fields = {}
    related_string_functions = {}
    related_search_filters = {}
    
    class Meta:
        abstract = True
    
    def foreignkey_autocomplete(self, request):
        
        def _restrict_queryset(queryset, search_fields):
            for bit in search_fields.split(','):
                if bit[0] == '#':
                    key, val = bit[1:].split('=')
                    queryset = queryset.filter(**{key: val})
            return queryset
        
        query = request.GET.get('q', None)
        app_label = request.GET.get('app_label', None)
        model_name = request.GET.get('model_name', None)
        search_fields = request.GET.get('search_fields', None)
        object_pk = request.GET.get('object_pk', None)
        try:
            to_string_function = self.related_string_functions[model_name]
        except KeyError:
            to_string_function = lambda x: x.__unicode__()
        if search_fields and app_label and model_name and (query or object_pk):
            def construct_search(field_name):
                if field_name.startswith('^'):
                    return "%s__istartswith" % field_name[1:]
                elif field_name.startswith('='):
                    return "%s__iexact" % field_name[1:]
                elif field_name.startswith('@'):
                    return "%s__search" % field_name[1:]
                else:
                    return "%s__icontains" % field_name
            
            model = models.get_model(app_label, model_name)
            queryset = model._default_manager.all()
            data = ''
            if query:
                for bit in query.split():
                    or_queries = []
                    for field_name in search_fields.split(','):
                        if field_name[0] == "#":
                            continue
                        or_queries.append(
                            models.Q(**{construct_search(smart_str(field_name)): smart_str(bit)}))
                    other_qs = QuerySet(model)
                    other_qs.dup_select_related(queryset)
                    other_qs = other_qs.filter(reduce(operator.or_, or_queries))
                    queryset = queryset & other_qs
                queryset = _restrict_queryset(queryset, search_fields)
                data = ''.join([u'%s|%s\n' % (
                    to_string_function(f), f.pk) for f in queryset])
            elif object_pk:
                try:
                    obj = queryset.get(pk=object_pk)
                except:
                    pass
                else:
                    data = to_string_function(obj)
            return HttpResponse(data)
        return HttpResponseNotFound()
    
    def get_help_text(self, field_name, model_name):
        searchable_fields = self.related_search_fields.get(field_name, None)
        if searchable_fields:
            help_kwargs = {
                'model_name': model_name,
                'field_list': get_text_list(searchable_fields, _('and')),
            }
            return _('Use the left field to do %(model_name)s lookups in the fields %(field_list)s.') % help_kwargs
        return ''
    

class ForeignKeyAutocompleteAdmin(BaseAutocompleteAdminMixin, admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if (isinstance(db_field, models.ForeignKey) and 
            db_field.name in self.related_search_fields):
            model_name = db_field.rel.to._meta.object_name
            # help_text = self.get_help_text(db_field.name, model_name)
            if kwargs.get('help_text'):
                help_text = u'%s %s' % (kwargs['help_text'], help_text)
            kwargs['widget'] = ForeignKeySearchWidget(db_field.rel, self.related_search_fields[db_field.name])
            # kwargs['help_text'] = help_text
        return super(ForeignKeyAutocompleteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    def get_urls(self):
        urls = super(ForeignKeyAutocompleteAdmin, self).get_urls()
        search_url = patterns('',
            (r'^foreignkey_autocomplete/$', self.admin_site.admin_view(self.foreignkey_autocomplete))
        )
        return search_url + urls

class NoLookupsForeignKeyAutocompleteAdmin(BaseAutocompleteAdminMixin, admin.ModelAdmin):    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if (isinstance(db_field, models.ForeignKey) and 
            db_field.name in self.related_search_fields):
            model_name = db_field.rel.to._meta.object_name
            # help_text = self.get_help_text(db_field.name, model_name)
            if kwargs.get('help_text'):
                help_text = u'%s %s' % (kwargs['help_text'], help_text)
            kwargs['widget'] = NoLookupsForeignKeySearchWidget(db_field.rel, self.related_search_fields[db_field.name])
            # kwargs['help_text'] = help_text
        return super(NoLookupsForeignKeyAutocompleteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    def get_urls(self):
        urls = super(NoLookupsForeignKeyAutocompleteAdmin, self).get_urls()
        search_url = patterns('',
            (r'^foreignkey_autocomplete/$', self.admin_site.admin_view(self.foreignkey_autocomplete))
        )
        return search_url + urls

class InlineAutocompleteAdmin(BaseAutocompleteAdminMixin, admin.TabularInline):    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if (isinstance(db_field, models.ForeignKey) and 
            db_field.name in self.related_search_fields):
            model_name = db_field.rel.to._meta.object_name
            # help_text = self.get_help_text(db_field.name, model_name)
            if kwargs.get('help_text'):
                help_text = u'%s %s' % (kwargs['help_text'], help_text)
            kwargs['widget'] = InlineForeignKeySearchWidget(db_field.rel, self.related_search_fields[db_field.name])
            # kwargs['help_text'] = help_text
        return super(InlineAutocompleteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    def get_urls(self):
        urls = super(InlineAutocompleteAdmin, self).get_urls()
        search_url = patterns('',
            (r'^foreignkey_autocomplete/$', self.admin_site.admin_view(self.foreignkey_autocomplete))
        )
        return search_url + urls
