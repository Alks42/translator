import translator


def test_translate():
    assert translator.translate('simple')
    assert translator.translate('hissy fit')
    assert translator.translate('two words')
    assert translator.translate('N0t corr@ct wrod')
    assert translator.translate('Перевод с неправильного языка')
    assert translator.translate('long sentence containing different characters if someone will use it this way')
