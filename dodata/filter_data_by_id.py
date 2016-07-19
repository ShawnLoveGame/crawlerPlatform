#!/usr/bin/env python2.7
#coding=utf-8
#author@alingse
#2014.11.08

from __future__ import print_function
import argparse
#import rapidjson as json
import json
import sys

log = print


def get_id_from_id_line(id_line):
    return id_line.strip()
    #return id_line.strip().decode('utf-8')
    #return id_line.strip()[-32:]
    #return id_line.split('\t',1)[0]
    #return id_line.split('\t',1)[1]
    #return id_line.strip().split('\t', 1)[1]
    #return id_line.split(' ',1)[0]
    #return json.loads(id_line).get('item_id')
    #return json.loads(id_line).get('unique')
    #return json.loads(id_line).get('name').decode('utf-8')
    #return json.loads(id_line).get('weibo')
    #result = json.loads(id_line)
    #return result['feed_id']+'ID'+result['datenow']
    #return json.loads(id_line).get('shop_id')


    #import re
    #weibofinder=re.compile('"weibo": "([^"]+)"').findall
def get_id_from_data_line(data_line):
    """
    try:
        data=json.loads(data_line)
        return data.get("data").get("itemInfoModel").get("itemId")         
    except:
        return None
    """
    #result = json.loads(data_line)
    #return result['feed_id']+'ID'+result['datenow']
    #return result['start']+result['end']+result['key']
    return data_line.strip()
    #return data_line.strip()[-32:]
    #return data_line.split('\t',1)[0]
    #return data_line.split('\t',2)[1]
    #return data_line.split('\t')[1]
    #return data_line.split('\t')[0]
    #return data_line.strip().split('\t')[2]
    #return data_line.strip().split('\t')[1]
    #return data_line.split(' ')[1]
    #return data_line.split(' ',1)[0]
    #return data_line.split(',',1)[0]
    #return data_line.split('\t')[1].strip()
    #return weibofinder(data_line[:300])[0]
    #return str(json.loads(data_line).get('uin'))
    #return str(json.loads(data_line).get('cat_id'))
    #return json.loads(data_line).get('shop_id')
    #return json.loads(data_line).get('id')[-32:]
    #return json.loads(data_line).get('unique')
    #return json.loads(data_line).get('company_id')[-32:]
    #return json.loads(data_line).get('KeyNo')
    #return json.loads(data_line).get('category')
    #return json.loads(data_line).get('name').decode('utf-8')
    #return json.loads(data_line).get('ent_name').decode('utf-8')
    #return json.loads(data_line).get('id')
    #return json.loads(data_line).get('wb')
    #return json.loads(data_line).get('weibo')
    #return str(json.loads(data_line).get('item_id'))
    #return json.loads(data_line).get('seller_id')
    #return json.loads(data_line).get('item_id')
    #return json.loads(data_line).get('nid')
    #return json.loads(data_line).get('feed_id')
    #return json.loads(data_line).get('item_info',{}).get('item_id')
    #return json.loads(data_line).get('item_info',{}).get('category_id')
    #return json.loads(data_line).get('guid')
    #return json.loads(data_line).get('uid')
    #return str(json.loads(data_line).get('brandId'))


def load_id_dict(idfd):
    id_dict = {}
    for id_line in idfd:
        if id_line == "\n":
            continue
        _id = get_id_from_id_line(id_line)
        if _id != None:
            id_dict[_id] = 0
    return id_dict


def filter_data(id_dict, id_ct, datafd, outfd, multi=False):
    hit = 0
    ct = 0
    for data_line in datafd:
        ct += 1
        if data_line == '\n':
            continue
        _id = get_id_from_data_line(data_line)
        if _id == None:
            continue
        if _id not in id_dict:
            continue
        #multi data share one id
        if multi == False:
            if id_dict[_id] == 1:
                continue
        if id_dict[_id] == 0:
            id_dict[_id] = 1
            hit += 1
        outfd.write(data_line)
        if hit == id_ct:
            break

        #for log
        if ct % 1000 == 0:
            log('id:{},visit data:{} hit:{}'.format(id_ct, data_ct, hit))
    log('id:{} hit:{} notin:{}'.format(id_ct, hit, (id_ct - hit)))
    return hit


def dump_notin(idfd, id_dict, notinfd):
    for id_line in idfd:
        if id_line == "\n":
            continue
        _id = get_id_from_id_line(id_line)
        if _id != None:
            if id_dict[_id] == 0:
                notinfd.write(id_line)


def main(idf, dataf, outf, notinf, multi=False):
    idfd = open(idf, 'r')

    id_dict = load_id_dict(idfd)

    idfd.close()

    id_ct = len(id_dict)
    log("got id count: {}".format(id_ct))

    datafd = open(dataf, 'r')
    outfd = open(outf, 'w')

    hit = filter_data(id_dict, id_ct, datafd, outfd, multi=multi)

    datafd.close()
    outfd.close()

    if hit == id_ct:
        return True
    if notinf == None:
        return None

    log('dump the notin id file')

    idfd = open(idf, 'r')
    notinfd = open(notinf, 'w')
    dump_notin(idfd, id_dict, notinfd)
    idfd.close()
    notinfd.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('idf', help='id file')
    parser.add_argument('dataf', help='data file')
    parser.add_argument('outf', help='filter data file')
    parser.add_argument('notinf', nargs='?', help='notin id file')
    parser.add_argument('-m',
                        '--multi',
                        action='store_true',
                        help='multi data share one id')
    args = parser.parse_args()
    log(args)

    idf = args.idf
    dataf = args.dataf
    outf = args.outf
    notinf = args.notinf
    multi = args.multi
    main(idf, dataf, outf, notinf, multi=multi)
