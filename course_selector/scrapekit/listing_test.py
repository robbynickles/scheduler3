from type_match import valid_types
import traceback

def test_suite( LT ):
    try:
        assert set( LT.keys() ) == set( ['Name', 'Section', 'Title', 'Important Notes', \
                                             'Instructor', 'Units', 'Location', 'Type', \
                                             'Times', 'Days', 'Max/', 'Avail' ] )
        #assert all( map( bool, LT.values() ) )
        assert LT['Section'][0].isdigit()
        assert not LT['Units'][0].isalpha()
        assert all( map( lambda x: x in valid_types, LT['Type'] ) )
        assert '/' in LT['Max/'][0]
        assert '/' in LT['Title'][1]
        assert all(map( lambda x: isinstance(x, list), LT.values()))
    except AssertionError:
        print LT
        print traceback.format_exc()#more informative error log
