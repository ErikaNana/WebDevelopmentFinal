from time import gmtime, strftime

class Entry_Class:
    def __init__(self,content,current, version = "0"):
        self.entry_content = content
        self.entry_created = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        self.if_current = current
        self.version_created = version
