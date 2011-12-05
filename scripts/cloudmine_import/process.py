#!/usr/bin/python

import sys
import os
import json
import msgpack

if len(sys.argv) != 4:
    print "usage: %s <pre> <tmin> <tmax>" % (sys.argv[0])
    sys.exit(1)

pre = sys.argv[1]
tmin = sys.argv[2]
tmax = sys.argv[3]

output_format = "json"
# output_format = "msgpack"


def parsedate(path):
    fname = os.path.basename(path)

    date = fname.split('.')[1]
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])

    return (year, month, day)

year, month, day = parsedate(pre)

def save_output(start, limit, outname):
    pre_f = open(pre)
    tmin_f = open(tmin)
    tmax_f = open(tmax)
    
    try:
        row = -1
        seq = -1
        data = {}
    
        for pline in pre_f:
            row = row + 1
            col = -1

            minline = tmin_f.readline().strip()
            maxline = tmax_f.readline().strip()
            
            pvalues = pline.split()
            minvalues = minline.split()
            maxvalues = maxline.split()
    
            index = -1
            for pvalue in pvalues:
                index = index + 1
                col = col + 1
                seq = seq + 1
    
                if seq < start:
                    continue
                if limit > 0 and seq > limit:
                    break
    
                pvalue = float(pvalue)
                minvalue = float(minvalues[index])
                maxvalue = float(maxvalues[index])
    
    
                if pvalue != -999 or minvalue != -999 or maxvalue != -999:
                    #print "%s [%s, %s] %s" % (seq, row, col, value)
                    entry = {
                        "row": row,
                        "col": col,
                        "precip": pvalue,
                        "mint": minvalue,
                        "maxt": maxvalue,
                        "seq": seq,
                        "year": year,
                        "month": month,
                        "day": day,
                        }
                    data["%s%s%s_%s" % (year, month, day, seq)] = entry
                    # if seq != 252684:
                    #     comma = ','
                    # else:
                    #     comma = ''
                    # print '"%s%s%s_%s": %s%s' % (year, month, day, seq, json.dumps(entry), comma)
        
        if output_format == "msgpack":
            packer = msgpack.Packer()
            data = msgpack.packb(data)
        else:
            data = json.dumps(data)
        
        fout = open(outname, "w")
        fout.write(data)
        fout.close()
    
    except Exception, e:
        pre_f.close()
        tmin_f.close()
        tmax_f.close()
        print e
    

tpd = 259200 # total per day: 720*360
slices = 20

for slice in range(slices):
    per_slice = tpd/slices
    start = slice * per_slice
    limit = (slice+1) * per_slice

    d = "%s%02i%02i" % (year, month, day)
    outname = "output.%s.%s.%s" % (d, slice, output_format)

    sys.stderr.write("slice: %s, start: %s, limit: %s, fname: %s\n" % (slice, start, limit, outname))

    save_output(start, limit, outname)

