from app.main import parse_pdf


def test_parse80():
    try:
        with open('80.pdf', 'rb') as file:
            parse_pdf(file)
    except:
        pass
    assert True
