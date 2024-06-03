from app import create_app
import unittest

app = create_app('default')
print('hi')


@app.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
