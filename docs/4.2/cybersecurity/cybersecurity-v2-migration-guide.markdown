---
layout: docs
title: Cybersecurity Toolkit Migration Guide (v1.0.0 -> v2.0.0)
description: Migrating the Cybersecurity Toolkit to v2.0.0
weight: 10
published: true
---

# Cybersecurity Toolkit Migration Guide (v1.0.0 -> v2.0.0)

The Cybersecurity Toolkit provides operators that are capable of analyzing DNS
response records. The operators in this toolkit use machine learning models to
analyze DNS traffic and report on suspicious behaviour.

A number of significant features and improvements were made in v2.0.0 of the
toolkit. In order to support these improvements, some API breaking changes were
necessary. This guide will walk you through the steps needed to migrate your
existing applications to use v2.0.0.

## Migrating applications using the DomainProfiling operator

1. In v1.0.0, the **DomainProfiling** operator required an input attribute
    called *dstAddress* with a type of **rstring**. In other words, the operator
    only ingested string-based IP addresses.

    To improve performance, the operator now supports only *numeric* IP
    addresses. Thus, the operator now expects an input attribute called
    *dstAddress* with a type of **uint32**.

    The pre-defined *DPDNSResponseMessage_t* type has been updated to reflect
    this change. Applications using this type will need to modify upstream
    operators, such as the **DNSMessageParser** operator, to assign a numeric
    value to this attribute.

2. In v1.0.0, the **DomainProfiling** operator required input attributes called
    *answerData* and *additionalData*.

    To improve performance, the operator no longer requires this data in order
    to function. The operator has been updated to not expect these attributes to
    be present on the input schema.

    These attributes have been removed from the pre-defined
    *DPDNSResponseMessage_t* type. Applications using this pre-defined type
    may encounter an error when assigning values to these attributes (since they
    no longer exist in the schema). One of the following approaches can be taken
    to resolve this issue:

    - Remove the assignments from the upstream operator
    - Re-add these attributes to the output schema of the upstream operator

## Migrating applications using the HostProfiling operator

1. In v1.0.0, the **HostProfiling** operator required an input attribute
    called *dstAddress* with a type of **rstring**. In other words, the operator
    only ingested string-based IP addresses.

    To improve performance, the operator now supports only *numeric* IP
    addresses. Thus, the operator now expects an input attribute called
    *dstAddress* with a type of **uint32**.

    The pre-defined *HPDNSResponseMessage_t* type has been updated to reflect
    this change. Applications using this type will need to modify upstream
    operators, such as the **DNSMessageParser** operator, to assign a numeric
    value to this attribute.

2. In v1.0.0, the **HostProfiling** operator required input attributes called
    *answerData* and *additionalData*.

    To improve performance, the operator no longer requires this data in order
    to function. The operator has been updated to not expect these attributes to
    be present on the input schema.

    These attributes have been removed from the pre-defined
    *HPDNSResponseMessage_t* type. Applications using this pre-defined type
    may encounter an error when assigning values to these attributes (since they
    no longer exist in the schema). One of the following approaches can be taken
    to resolve this issue:

    - Remove the assignments from the upstream operator
    - Re-add these attributes to the output schema of the upstream operator

## Migrating applications using the PredictiveBlacklistingFE operator

1. In v1.0.0, the **PredictiveBlacklistingFE** operator required an input
    attribute called *dstAddress* with a type of **rstring**. In other words, the
    operator only ingested a string-based IP address for the destination address.

    To improve performance, the operator now supports only a *numeric* IP
    address for the destination address. Thus, the operator now expects an input attribute called *dstAddress* with a type of **uint32**.

    The pre-defined PBPDNSResponseMessage_t* type has been updated to reflect
    this change. Applications using this type will need to modify upstream
    operators, such as the **DNSMessageParser** operator, to assign a numeric
    value to this attribute.

2. In v1.0.0, the **PredictiveBlacklistingFE** operator required input
    attributes called *answerCount*, *nameserverCount* and *additionalCount*.

    To improve performance, the operator no longer requires this data in order
    to function. The operator has been updated to not expect these attributes to
    be present on the input schema.

    These attributes have been removed from the pre-defined
    *PBDNSResponseMessage_t* type. Applications using this pre-defined type
    may encounter an error when assigning values to these attributes (since they
    no longer exist in the schema). One of the following approaches can be taken
    to resolve this issue:

    - Remove the assignments from the upstream operator
    - Re-add these attributes to the output schema of the upstream operator


## Migrating applications using the BWListTagger operator

1. The *BWListTag_e* enum type contains the values output values for the
    **BWListTagger** operator. In v1.0.0, this type contains four possible
    values: **{*nonMatched*, *whiteList*, *blackListIP*, *blackListDomain*}**

    In order to simply the number of values that an application needs to check,
    the *blackListIP* and *blackListDomain* values have been removed and
    replaced with a value of *blackList*.

    Applications that check the values returned by the **BWListTagger** will
    need to be updated to reflect the above change.

2. In v1.0.0, the **BWListTagger** operator supported dynamic updates through
    4 control ports, where each control port accepted a filename to update
    a different internal lookup table (IP-whitelist, IP-blacklist,
    domain-whitelist or domain-blacklist).

    In v2.0.0, in order to support updating the internal tables from an
    arbitrary input source (i.e. files, K/V store lookup, messaging apps, etc),
    the operator has been modified to include only a single control port. This
    control port accepts a tuple of type *BWListUpdate_t*. This type has the
    following schema:

        type BWListUpdate_t = rstring domainIP, BWListAction_e action, BWListTag_e listTag

    Upstream operators can submit a tuple of *BWListUpdate_t* to the control
    port to add/remove and IP or domain to/from the internal lookup tables. The
    *BWListAction_e* enum type has the following values: **{*add*, *remove*}**.

    In order to maintain performance and to ensure that the operator continues
    to process tuples as fast as possible, any updates made to the internal
    lookup tables via the control port are not committed until the port
    receives a window punctuation. Once a a puctuation is received, the operator
    will stop processing tuples, apply the changes to the internal lookup
    tables and then resume processing.

    A sample application will be available on GitHub to demonstrate how to
    dynamically the update the operator using a file-based approach similar
    to v1.0.0 of the operator. Applications previously using the dynamic
    update feature of the operator should refer to this sample prior
    to making changes to their application.

3. In v1.0.0, The **BWListTagger** operator supported two output functions:
    *getDomainTags()* and *getIPTags()*. The return type for these functions
    were either *BWListTag_e* or *list<BWListTag_e>*, depending on whether the
    input attribute was a scalar value or a list (i.e. a single domain or a list
    or domains).

    In v2.0.0, the operator has been enhanced to support **nested custom output
    functions**. This feature allows the user to use expressions that include
    the output functions when specifying a value on the output port. As part of
    this effort, the return type for the *getDomainTags()* and *getIPTags()*
    output functions is now *list<BWListTag_e>*, regardless of whether the
    input attribute is a scalar or list.

    Applications that previously relied on the output functions returning a single
    **BWListTag_e** value can achieve the same result by accessing the list item
    at index 0. Take the following example of an existing application, where
    *domainTag* and *ipTag* are **BWListTag_e**:

        output
          BWListTagger_OutStream : domainTag = getDomainTags(), ipTag = getIPTags();

    To migrate this application to use v2.0.0, the output clause assignments
    need to modified to access the element at index 0:

        output
          BWListTagger_OutStream : domainTag = getDomainTags()[0], ipTag = getIPTags()[0];
