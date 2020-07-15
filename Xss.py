import re
class XSS_Detect:
 def __init__(self):
   self.xss_sim=r"((\%3C)|<)((\%2F)|\/)*[a-z0-9\%]+((\%3E)|>)"
   self.xss_img=r"((\%3C)|<)((\%69)|i|(\%49))((\%6D)|m|(\%4D))((\%67)|g|(\%47))[^\n]+((\%3E)|>)"
   self.xss_para=r"((\%3C)|<)[^\n]+((\%3E)|>)"
 def check(self,url):
    print(url,re.search(self.xss_sim,url))
    if re.search(self.xss_sim,url)!=None or re.search(self.xss_img,url)!=None or re.search(self.xss_para,url)!=None:
      print(url,re.search(self.xss_sim,url))
      return True
    else:
      return False
    
