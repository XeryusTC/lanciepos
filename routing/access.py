import Pyro4
import subprocess

class GrantAccess:	
	def add_to_whitelist(self, ipaddress):
		ipaddress = self._valid_ip_address(ipaddress)
		
		filter_command = "iptables -I whitelist 1 -i eth1 -s {ip} -j RETURN".format(ip=ipaddress)
		nat_command = "iptables -I whitelist-nat 1 -t nat -i eth1 -s {ip} -j RETURN".format(ip=ipaddress)

		print("Adding {ip} to the whitelist".format(ip=ipaddress))
		print("\t", filter_command)
		filter_output = subprocess.check_output(filter_command, shell=True, universal_newlines=True)
		print("\t", nat_command)		
		nat_output = subprocess.check_output(nat_command, shell=True, universal_newlines=True)
		
		if len(nat_output) > 0 or len(filter_output) > 0:
			print(filter_output, "\n", nat_output)
			raise Exception("iptables_fail", filter_output, nat_output)
		
		return None
	
	def _valid_ip_address(self, ipaddress):
		"""
		Checks whether a given IP address is valid or not and removes whitespace if necessary
		"""
		bytes = ipaddress.split('.')

		if len(bytes) is not 4:
			raise Exception("ipaddressinvalid")

		bytes = [int(byte.strip()) for byte in bytes]
		for byte in bytes:
			if not (0 <= byte < 255):
				raise Exception("ipaddressinvalid")

		return ".".join([str(byte) for byte in bytes])


def main():
	iptables_manager = GrantAccess()

	# Start Pyro daemon and register with name server
	netd = Pyro4.Daemon()
	access_iptables_uri = netd.register(iptables_manager)
	ns = Pyro4.locateNS()
	ns.register("access.manager", access_iptables_uri)
	
	print("iptables manager running")
	netd.requestLoop()

if __name__ == '__main__':
	try:
		subprocess.check_output("iptables-save > ~/iptables.backup", shell=True, universal_newlines=True)
	except subprocess.CalledProcessError as ex:
		print("Backing up the current iptables configuration failed. Exit code {0}".format(ex.returncode))
	
	main()
