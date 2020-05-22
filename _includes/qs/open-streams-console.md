Get the URL of the Streams Console for your Streams instance. 
   
- **Find the URL for the Streams add-on in IBM Cloud Pak for Data:**
     - From the navigation menu, click <strong>My instances</strong>.
     - Click the <strong>Provisioned Instances</strong> tab.
     - Find your Streams instance, and click **View details** from the context menu. Open the URL under **External console endpoint**.
       
- **Open the Streams Console in IBM Cloud:**
  - From the Dashboard, click **Resource list***.
  - Find your Streaming Analytics instance in the list of services, and click on it.
  - From the service page, click **Launch**.

- **From a local installation of Streams**:
  - Run the following command, assuming that S:

    <pre>
    $ source $STREAMS_INTSALL/bin/streamsprofile.sh
    $ streamtool geturl 
    https://streamsqse.localdomain:8443/streams/domain/console
    </pre>

    Open this URL in a browser, and you will see a log-in screen. If you are using the Streams Quick Start Edition VM, enter the following user ID and password: **streamsadmin:passw0rd**.


- **Find the URL for Streams stand-alone deployment**: [See the documentation](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_5.2.0/com.ibm.streams.dev.doc/doc/find-dns-url.html#find-dns-url). Choose *finding the internal URL*  or *finding the external URL* depending on whether or not you will be accessing the Streams Console from within the Kubernetes cluster.

