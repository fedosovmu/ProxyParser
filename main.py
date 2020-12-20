from proxy_list_updater import ProxyListUpdater

ProxyListUpdater.update_proxy_list()
proxy_list = ProxyListUpdater.load_proxy_list()

print('===========')
for proxy in proxy_list:
    print(proxy)



