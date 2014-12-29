import urllib, urllib2

class GoogleStaticMapAPI(object):
    def create_marker( self, (color, label, location ) ):
        marker_template = "color:{}|label:{}|{}"
        return marker_template.format( color, label, location ) 

    def create_url( self, parameter_list ):
        url_template = "https://maps.googleapis.com/maps/api/staticmap?{}"
        return url_template.format( '&'.join( parameter_list ) )

    def get_map_picture(self, fd, markers=None, **gmap_parameters):
        parameter_list = ['{}={}'.format(k, urllib.quote( v ) ) for k,v in gmap_parameters.items()] + \
                         ['markers={}'.format( urllib.quote( self.create_marker(m) ) ) for m in markers]
        req = urllib2.Request( self.create_url( parameter_list ), None, {} )
        res = urllib2.urlopen(req).read()
        with open(fd, 'w') as f: 
            f.write( res )



if __name__ == '__main__':
    def college(building): 
        return "{}, Columbia, Ca, 95310".format( building )
    # Bug: When two markers are on the same location, the first one wins.
    markers = [ ('blue' , '', college('Maple'  ) ),
                ('green', '', college('Sequoia') ),
                ('red'  , '', college('Toyon'  ) ),
                ('green', '', college('Toyon'  ) ) ] 
    gsm = GoogleStaticMapAPI()
    gsm.get_map_picture( 'test.png', markers=markers, size='640x640' )
                       
    
