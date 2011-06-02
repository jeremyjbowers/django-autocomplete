wapo-django-autocomplete
========================
Autocomplete is an installable app which overrides the raw ID widget with an autocomplete search box.

Warning: wapo-django-autocomplete is probably broken
-----------------------------------------------------
I won't know for sure if this is working for a little while. If you're installing this, you're probably either me or crazy.

Code
-----
Here's an example of how you would use wapo-django-autocomplete to create an autocomplete field on a a foreign key field on an inline.

    class FooInline(InlineAutocompleteAdmin):
        model = Foo
        related_search_fields = {
            'bar': ('field__field_2', '#field__field2=baz', '#field3__field4__field5=bat'),
        }