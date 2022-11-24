# -*- coding: utf-8 -*-
# info:不基于腾讯云的SDK来调用腾讯云的API
# author: Theon 
# Version: 0.1.0
# 2022-11-24
import hashlib, hmac, json, os, sys, time
from datetime import datetime
from APIConfig import config,params
from urllib import request,parse

algorithm = "TC3-HMAC-SHA256"
timestamp = int(time.time())
date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

# ************* 步骤 1：拼接规范请求串 *************
http_request_method = "POST"
canonical_uri = "/"
canonical_querystring = ""
ct = "application/json; charset=utf-8"
canonical_headers = "content-type:%s\nhost:%s\n" % (ct, config.host)
signed_headers = "content-type;host"
hashed_request_payload = hashlib.sha256(json.dumps(params.avgs).encode("utf-8")).hexdigest()
canonical_request = (http_request_method + "\n" +
                     canonical_uri + "\n" +
                     canonical_querystring + "\n" +
                     canonical_headers + "\n" +
                     signed_headers + "\n" +
                     hashed_request_payload)
#print(canonical_request)

# ************* 步骤 2：拼接待签名字符串 *************
credential_scope = date + "/" + config.service + "/" + "tc3_request"
hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
string_to_sign = (algorithm + "\n" +
                  str(timestamp) + "\n" +
                  credential_scope + "\n" +
                  hashed_canonical_request)
#print(string_to_sign)


# ************* 步骤 3：计算签名 *************
# 计算签名摘要函数
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
secret_date = sign(("TC3" + config.secret_key).encode("utf-8"), date)
secret_service = sign(secret_date, config.service)
secret_signing = sign(secret_service, "tc3_request")
signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
#print(signature)

# ************* 步骤 4：拼接 Authorization *************
authorization = (algorithm + " " +
                 "Credential=" + config.secret_id + "/" + credential_scope + ", " +
                 "SignedHeaders=" + signed_headers + ", " +
                 "Signature=" + signature)
#print(authorization)

#调用接口
def call_api(authorization,timestamp):
    headers={
         "Host":config.host,
         "Content-Type": "application/json; charset=utf-8",
         "User-Agent":"Tencent Wangyong SDK By Theon",
         "Authorization":authorization,
         "X-TC-Action":config.action,
         "X-TC-Timestamp":str(timestamp),
         "X-TC-Version":config.version,
         "X-TC-Region":config.region      
         }
    try:
        add_url= request.Request(url=config.endpoint,data=bytes(json.dumps(params.avgs),'utf-8'),headers=headers,method='POST')
        res=request.urlopen(add_url)
        resaut=res.read().decode("utf-8")
        print(resaut)
        
    except Exception as err:
        print(err)
        with open("error.log","a+") as r:
            r.write("%s\n" % err )
   
call_api(authorization,timestamp)