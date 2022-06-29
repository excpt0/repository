from app.foobar.views import BarView, FooView

urls = [
    ('/api/bar', BarView),
    ('/api/foo', FooView),
]