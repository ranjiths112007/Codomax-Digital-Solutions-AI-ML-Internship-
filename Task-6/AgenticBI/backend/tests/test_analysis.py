from app.analysis import analyze_csv

def test_shape_missing_and_duplicates():
    result = analyze_csv(b'region,sales,units\nSouth,100,2\nNorth,200,3\nSouth,100,2\n,300,4\n','test.csv')
    assert result['shape'] == {'rows':4,'columns':3}
    assert result['data_quality']['duplicate_rows'] == 1
    assert result['data_quality']['missing_cells'] == 1
    assert 'sales' in result['numeric_summary']

def test_empty_csv_fails():
    try: analyze_csv(b'')
    except ValueError: return
    raise AssertionError('Expected empty CSV to fail')
