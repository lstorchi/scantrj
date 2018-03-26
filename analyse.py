import glob 
import gzip
import sys
import os
import re

sys.path.append("./common")
import maesfsm
import util

os.chdir("./")

fullsetofsites = []

total_num_of_centroid = 0

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

                    total_num_of_centroid = total_num_of_centroid + 1

                    for spoint in atomdata[idx]:
                        spoint = spoint.strip()
                        spoint = re.sub(' +',' ', spoint)
                        s_spoint = spoint.split()
                        site.points.append((float(s_spoint[2]), float(s_spoint[3]), \
                                float(s_spoint[4])))

                    sitespermol.append(site)
                else:
                    print "Error in file header "

        if len(sitespermol) > 0:
            fullsetofsites.append(sitespermol)
    else:
        print "Error in parsing mae file"

    fp.close()

    cmd = "gzip -c -9 " + basename + ".mae > " + \
            basename + ".maegz"
    os.system (cmd)
    os.remove(basename + ".mae")

util.if_exist_rm("centroid.xyz")
fp = open("centroid.xyz", "w")

fp.write(str(total_num_of_centroid) + "\n")
fp.write("centroids\n")

for sites in fullsetofsites:
    print len(sites)
    for site in sites:
        print "  ", site.s_m_title
        c = util.centroid(site.points)
        if c != None:
            fp.write("H %12.6f %12.6f %12.6f\n"%(c[0], c[1], c[2]))

fp.close()
