class FooInline(InlineAutocompleteAdmin):
    model = Foo
    related_search_fields = {
        'team': ('school__school', '#sport__sport=Football', '#season__season_start_date__year=2010'),
        'player1': ('player__first_name', 'player__last_name', '#team__sport__sport=Football', '#team__season__season_start_date__year=2010'),
        'player2': ('player__first_name', 'player__last_name', '#team__sport__sport=Football', '#team__season__season_start_date__year=2010'),
        'pat_by': ('player__first_name', 'player__last_name', '#team__sport__sport=Football', '#team__season__season_start_date__year=2010'),
        'pat_to': ('player__first_name', 'player__last_name', '#team__sport__sport=Football', '#team__season__season_start_date__year=2010'),
    }
