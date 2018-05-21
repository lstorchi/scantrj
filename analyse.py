import numpy
import glob 
import gzip
import sys
import os
import re

import numpy.linalg

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
    siteheader = []

    maesfsm.import_mae_file(fp.readlines(), sitedata, atomdata, siteheader)

    if len(sitedata) == len(atomdata) and len(sitedata) == len(siteheader):
        sitespermol = []

        for idx in range(0,len(sitedata)):
            if (sitedata[idx][0].find("_site_") > 0):
                if (len(sitedata[idx]) > 0):
                    site = maesfsm.site_data()
                    
                    totfill = 0
                    for hidx in range(len(siteheader[idx])):
                        if siteheader[idx][hidx] == "s_m_title":
                            site.s_m_title = sitedata[idx][hidx]
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "s_m_entry_name":
                            site.s_m_entry_name = sitedata[idx][hidx]
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_SiteScore":
                            site.r_sitemap_SiteScore = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "i_sitemap_size":
                            site.i_sitemap_size = int(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_Dscore":
                            site.r_sitemap_Dscore = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_volume":
                            site.r_sitemap_volume = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_exposure":
                            site.r_sitemap_exposure = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_enclosure":
                            site.r_sitemap_enclosure = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_contact":
                            site.r_sitemap_contact = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_phobic":
                            site.r_sitemap_phobic = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_philic":
                            site.r_sitemap_philic = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_balance":
                            site.r_sitemap_balance = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "r_sitemap_don/acc":
                            site.r_sitemap_don_d_acc = float(sitedata[idx][hidx])
                            totfill = totfill + 1
                        elif siteheader[idx][hidx] == "i_m_ct_format":
                            site.i_m_ct_format = float(sitedata[idx][hidx])
                            totfill = totfill + 1

                    if totfill != 14:
                        print "Some data may be missed"

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

util.if_exist_rm("data.txt")
fp1 = open("data.txt", "w")

fp.write(str(total_num_of_centroid) + "\n")
fp.write("centroids\n")

fp1.write("name, sscore, ssize, dscore, volume, sexposure, senclosure, sbalance, " + \
        "linearity, planarity, sphericity, anisotropy\n")
 
for sites in fullsetofsites:
    print len(sites)
    for site in sites:
        print "  ", site.s_m_title
        c = util.centroid(site.points)

        covm = numpy.cov (site.points, rowvar=False)

        ueigs, eigvls =  numpy.linalg.eig(covm)
        eigs =  numpy.sort(ueigs)

        linearity = 0.0
        planarity = 0.0
        sphericity = 0.0
        anisotropy = 0.0

        if  eigs.size == 3:
            sum = numpy.sum(eigs)
            l1 = eigs[2]/sum
            l2 = eigs[1]/sum
            l3 = eigs[0]/sum
            linearity = (l1 - l2)/l1
            planarity = (l2 - l3) / l1
            sphericity = l3 / l1
            anisotropy = (l1 - l3)/l1
        else:
            print "Error in eigenvalues dimension"

        fp1.write( \
                "%s, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f, %12.5f\n"%( \
                site.s_m_title, 
                site.r_sitemap_SiteScore, site.i_sitemap_size, site.r_sitemap_Dscore, site.r_sitemap_volume, \
                site.r_sitemap_exposure, site.r_sitemap_enclosure, site.r_sitemap_balance, \
                linearity, planarity, sphericity, anisotropy))

        fp2 = open(site.s_m_title+".xyz", "w")

        fp2.write(site.s_m_title+"\n")
        fp2.write(str(len(site.points)+1)+ "\n")
        fp2.write("O %12.6f %12.6f %12.6f\n"%(c[0], c[1], c[2]))
        for p in site.points:
            fp2.write("H %12.6f %12.6f %12.6f\n"%(p[0], p[1], p[2]))

        if c != None:
            fp.write("H %12.6f %12.6f %12.6f\n"%(c[0], c[1], c[2]))

        fp2.close()

fp.close()
fp1.close()
