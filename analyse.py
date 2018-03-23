import glob 
import gzip
import sys
import os

sys.path.append("./common")
import maesfsm

os.chdir("./")

fullsetofsites = []

for file in glob.glob("*.maegz"):
    print(file)
    basename = file[:-6]
    newfile = basename + ".mae.gz"
    os.rename(file, newfile)
    cmd = "gunzip " + newfile
    os.system (cmd)

    fp = open(basename + ".mae")

    sitedata = []
    atomdata = []

    maesfsm.import_mae_file(fp.readlines(), sitedata, atomdata)

    if len(sitedata) == len(atomdata):
        sitespermol = []

        for idx in range(0,len(sitedata)):
            if (sitedata[idx][0].find("_site_") > 0):
                if (len(sitedata[idx]) == 14):
                    print len(atomdata[idx])
                    site = maesfsm.site_data()

                    site.s_m_title = sitedata[idx][0]
                    site.s_m_entry_name = sitedata[idx][1]
                    site.r_sitemap_SiteScore = float(sitedata[idx][2])
                    site.i_sitemap_size = int(sitedata[idx][3])
                    site.r_sitemap_Dscore = float(sitedata[idx][4])
                    site.r_sitemap_volume = float(sitedata[idx][5])
                    site.r_sitemap_exposure = float(sitedata[idx][6])
                    site.r_sitemap_enclosure = float(sitedata[idx][7])
                    site.r_sitemap_contact = float(sitedata[idx][8])
                    site.r_sitemap_phobic = float(sitedata[idx][9])
                    site.r_sitemap_philic = float(sitedata[idx][10])
                    site.r_sitemap_balance = float(sitedata[idx][11])
                    site.r_sitemap_don_d_acc = float(sitedata[idx][12])
                    site.i_m_ct_format= float(sitedata[idx][13])

                    sitespermol.append(site)
                else:
                    print "Error in file header "

        if len(sitespermol) > 0:
            fullsetofsites.append(sitespermol)
    else:
        print "Error in parsing mae file"

    fp.close()

    exit()

