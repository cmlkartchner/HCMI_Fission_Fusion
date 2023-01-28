import random
from .Site import Site

class SiteBuilder:

    def build_sites(hexagons, num_sites, site_qualities=[]):
        site_hexes = random.sample(list(hexagons.values()), num_sites)
        sites=[]
        if site_qualities:
            for i in range(len(site_hexes)):
                sites.append(Site(site_hexes[i], site_qualities[i]))
        else:
            for i in range(len(site_hexes)):
                sites.append(Site(site_hexes[i]))