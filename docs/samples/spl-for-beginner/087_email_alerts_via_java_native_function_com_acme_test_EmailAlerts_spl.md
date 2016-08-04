---
layout: samples
title: 087_email_alerts_via_java_native_function
---

### 087_email_alerts_via_java_native_function

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/086_jms_source_sink_using_activemq_com_acme_test_JMSSourceSink_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/088_java_operator_params_and_multiple_input_output_ports_com_acme_test_JavaOperatorParams_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how one can send email alerts from within an SPL application.
It uses the Java APIs to send email alerts via the Streams Java native function feature.

In order to use this method, you should provide a valid SMTP server address available on your private or
corporate network. A valid SMTP server address must be passed as an argument to the
Java native function that will be called in the SPL code below.
*/
namespace com.acme.test;
// We will use the Java native function(s) defined within this namespace.
use com.acme.test.email::*;

composite EmailAlerts {
	graph
		// Create a Beacon signal to send an email to a group of recipients.
		stream<int32 dummy> MyData = Beacon() {
			param
				iterations: 1u;
		}

		// In this Custom operator, we will call a Java native function to
		// send the email alerts.
		// CAUTION:
		// 1) You must provide a valid SMTP server address for this to work correctly.
		// 2) You must provide a valid list of recipient email addresses.
		//
		// More importantly, use this technique sparingly not to flood someone's InBox with junk emails.
		() as MySink1 = Custom(MyData) {
			logic
				onTuple MyData: {
					// Let us call the Java native function to send the email alert.
					// You can find the Java native function code in the impl/java/src sub-directory of this SPL project.
					rstring subject = "Test email alert from IBM InfoSphere Streams";
					mutable rstring message = "This email is from the SPL example 087_email_alerts_via_java_native_function.\n";
					message += "It shows how to send email alerts from SPL applications." + "\n";
					message += "<<< End of Email >>>" + "\n";
					// You must REPLACE the dummy email addresses given below with correct email addresses of your recipients.
					mutable rstring recipients = "some-user-name@yahoo.com, different-user-name@gmail.com";
					// First argument is a valid SMTP server address name available on your network. (You must CHANGE it below)
					// Second argument is the email sender's address.
					// Third argument is the list of recipient email addresses.
					// Fourth argument is the email subject line.
					// Fifth argument is the email body content.
					sendEmail("my-smtp-server-name.com", "streams-test@acmedummy.com", recipients, subject, message);
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/086_jms_source_sink_using_activemq_com_acme_test_JMSSourceSink_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/088_java_operator_params_and_multiple_input_output_ports_com_acme_test_JavaOperatorParams_spl/"> > </a>
</div>

