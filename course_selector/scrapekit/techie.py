def clean(raw_listing):
    listing = []
    for td_tag in raw_listing.find_all('td'):
        tag_strings = [str(s).strip() for s in td_tag.strings]
        print td_tag
        if td_tag.attrs.has_key('style') and \
                '500px;' in td_tag.attrs['style']: #This is the more-info tag
            listing += [[" ".join(tag_strings)]]
        else:
            listing += [tag_strings]
    listing = listing[1:]
    #compress location data
    listing[6] = [ listing[6][i] + listing[6][i+1] for i in range(0,len(listing[6])-1,2)]    
    return listing
    
