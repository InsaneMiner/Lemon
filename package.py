class Package():
    def __init__(self,package_location):
        self.package_location = package_location
        self.needed_files = ["info.json","setup.conf.json","setup.list.json"]
        self.valid = self.check_valid()
    def check_valid(self):
        valid = 1
        for file in self.needed_files:
            try:
                open(f"{self.package_location}/{file}","r").close()
            except:
                valid = 0
                break
        return valid == 1

package = Package("lemon/TempPackage/WAF")