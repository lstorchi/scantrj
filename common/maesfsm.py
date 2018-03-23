
def import_mae_file (lines, sitedata, atomdata): # in the final version I should use a state machine

    state = None

    local_sitedata = []
    local_atomdata = []

    for line in lines:
        line = line.rstrip()
        line = line.lstrip()

        if state == "START":
            if line.find(":::") == 0:
                state = "SITEINFO"
        
        if state == "SITEINFO":   
            if line.find("m_atom") == 0:
                state = "ATOM"
            else:
                if line.find(":::") < 0:
                    local_sitedata.append(line)
                    #print "SITEINFO ", line 

        if state == "DATATOM":
            if line.find(":::") == 0:
                state = None
                sitedata.append(local_sitedata)
                atomdata.append(local_atomdata)
                local_sitedata = []
                local_atomdata = []
            else:
                local_atomdata.append(line)
                #print "DATATOM:", line

        if state == "ATOM":
            if line.find(":::") == 0:
                state = "DATATOM"

        if state == None:
            if line.find("f_m_ct {") == 0:
                state = "START"

class site_data(object):

    def __init__(self):
        self.s_m_title = ""
        self.s_m_entry_name = ""
        self.r_sitemap_SiteScore = 0.0
        self.i_sitemap_size = 0
        self.r_sitemap_Dscore = 0.0
        self.r_sitemap_volume = 0.0
        self.r_sitemap_exposure = 0.0
        self.r_sitemap_enclosure = 0.0
        self.r_sitemap_contact = 0.0
        self.r_sitemap_phobic = 0.0
        self.r_sitemap_philic = 0.0
        self.r_sitemap_balance = 0.0
        self.r_sitemap_don_d_acc = 0.0
        self.i_m_ct_format= 0

        self.points = []
