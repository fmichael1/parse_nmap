
<h1>Network Scanner Tool</h1>
<h2>Overview</h2>

<p>This Network Scanner Tool is a Python script designed for macOS and Linux systems. It provides information about your local network, such as the SSID, subnet mask, network gateway, and the local machine's IP and hostname. Additionally, it uses <code>nmap</code> to scan the local network for other devices, listing their IP addresses, hostnames, and open ports.</p>

<h2>Features</h2>
<ul>
  <li>Retrieve SSID of the connected Wi-Fi network.</li>
  <li>Display the local machine's IP address and hostname.</li>
  <li>Get the subnet mask and network gateway.</li>
  <li>Perform a network scan using <code>nmap</code>.</li>
  <li>Resolve hostnames using DNS, mDNS (via <code>dns-sd</code> or <code>avahi-browse</code>), and NetBIOS (<code>nmblookup</code>).</li>
</ul>

<h2>Prerequisites</h2>
<ul>
  <li>Python 3.x</li>
  <li><code>nmap</code></li>
  <li><code>dns-sd</code> (pre-installed on macOS)</li>
  <li><code>avahi-browse</code> (for Linux users)</li>
  <li><code>nmblookup</code> (Samba package for Linux)</li>
</ul>

<h2>Installation</h2>
<ol>
  <li><strong>Clone the repository</strong>:
    <pre><code>git clone https://github.com/fmichael1/parse_nmap.git</code></pre>
  </li>
  <li><strong>Install Dependencies</strong>:
    <ul>
      <li><strong>nmap</strong>:
        <ul>
          <li>macOS: <code>brew install nmap</code></li>
          <li>Linux: <code>sudo apt-get install nmap</code></li>
        </ul>
      </li>
      <li><strong>Avahi (Linux only)</strong>:
        <pre><code>sudo apt-get install avahi-utils</code></pre>
      </li>
      <li><strong>Samba for nmblookup (Linux only)</strong>:
        <pre><code>sudo apt-get install samba</code></pre>
      </li>
    </ul>
  </li>
</ol>

<h2>Usage</h2>
<p>Run the script using Python:</p>
  <pre><code>python network_scanner.py</code></pre>
<p>The script will output network details and a list of detected devices on your network.</p>

<h2>Output Example</h2>
<code>Network SSID:        MyWifiNetwork
Subnet Mask:         255.255.255.0
Network Gateway:     192.168.1.1
My IP:               192.168.1.100 (MyDevice.local)

Host  IP Address       Hostname            Ports
1     192.168.1.1      Router              80/tcp (http), 443/tcp (https)
2     192.168.1.101    DeviceOne           22/tcp (ssh)
... </code>
