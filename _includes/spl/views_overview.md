A [**View**](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.welcome.doc/doc/ibminfospherestreams-adminconsole-applications-visualizing-terminology.html) is a connection to a particular Stream in a running application that allows you to see a sample of the data in the Stream.
Views can be defined in an SPL with the [`@view` annotation](https://github.com/IBMStreams/samples/blob/main/Examples-for-beginners/103_view_annotation_at_work/com.acme.test/ViewAnnotationAtWork.spl#L38),  or in Python with the [`Stream.view` function](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.View).

Once the application is running, you can use the View to observe the data on the stream.  Additionally, Views can also be added at runtime to a job, with some exceptions.

To add a view or inspect the data in a View, you can also use the Streams Console or the Job Graph in IBM Cloud Pak for Data.

#### Quick facts about views

*   Views provide a _sample_ of the data on a Stream, and not all the tuples on the Stream.
*   Use a View to fetch data from a Stream only while the application is running.
*   The data retrieved by the View is read-only, so you cannot use a View to change the tuples on a Stream.

