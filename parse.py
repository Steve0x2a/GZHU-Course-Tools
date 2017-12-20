    def get_webflow(response):
        soup = BeautifulSoup(response.text,'html.parser')
        lt = soup.find('input',{'name' : 'lt'})['value']
        execution = soup.find('input',{'name' : 'execution'})['value']
        soup.clear()
        return(lt,execution)