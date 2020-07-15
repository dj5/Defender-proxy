import re
class SQLi_Detect:
 def __init__(self):
   self.sql_sim=r"(\%27)|(\')|(\-\-)|(\%23)|(#)"
   self.sql_mod=r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))"
   self.sql_typ=r"\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))"
 def check(self,url):
    if re.search(self.sql_sim,url) or re.search(self.sql_mod,url) or re.search(self.sql_typ,url):
      return True
    else:
      return False
    
