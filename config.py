import yaml

class config():
    def __init__(self,path):
        try:
            with open('config.yaml') as f:
                data=yaml.load(f,Loader=yaml.SafeLoader)
                self.posturl=data['posturl']
                self.verifyKey= data['verifyKey']
                self.hookurl=data['hookur']
                self.robotQQ=data['robotQQ']


        except:
            raise('ErrorConfig')


