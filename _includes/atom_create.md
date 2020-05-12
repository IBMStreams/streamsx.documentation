The general steps to create a new SPL project are:

1. Create an empty folder on your filesystem and import the folder into Atom.
2. Create a toolkit information file.

After you create your project, you can create applications. The entry point of any SPL application is called a _main composite_.

Create your first main composite by doing the following tasks:

1. Define a namespace to organize your code. This is not necessary but is good practice.
2. Create a main composite within a `.spl` file.


Create the project folder
---------------------------
* Create an empty folder on your file system, for example, `MyStreamsProject`.
* From Atom, go to **File > Add Project Folder** and select the project folder.

Create a toolkit information file
---------------------------------

SPL projects are also called toolkits.  Each toolkit folder must include a file called `info.xml` in the **top level** of the project. This file describes the toolkit and any other toolkits it depends on.


**Important**: This file must be in the top level of the project.


Create a file within the folder called `info.xml`.
Right-click your project folder, and select **New File**, and enter `info.xml` as the file name.

For your reference, the following code snippet is an overview of the contents of what needs to be present in the file. You can copy the contents into your `info.xml` file to get started.

  - `identity` tag contains general details about the project, name, version and required Streams version.
  - `dependencies` tag lists any toolkits you require.
  - `sabFiles` tag indicates which folders within the project contain files that your application will access at runtime.

```
<info:toolkitInfoModel
  xmlns:common="http://www.ibm.com/xmlns/prod/streams/spl/common"
   xmlns:info="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo">
  <info:identity>
    <info:name>MyStreamsToolkit</info:name>
    <info:description>My first toolkit</info:description>
    <info:version>1.0.0</info:version>
    <info:requiredProductVersion>4.0.0</info:requiredProductVersion>
  </info:identity>
  <info:dependencies>
    <info:toolkit>
      <common:name>com.ibm.streams.cep</common:name>
      <common:version>[2.1.1,3.0.0)</common:version>
    </info:toolkit>
  </info:dependencies>
  <info:sabFiles>
    <info:include path="data/**"/>
    <info:include path="etc/**"/>

  </info:sabFiles>
</info:toolkitInfoModel>

```
Learn more about the [toolkit information file in the documentation](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html).

Create a namespace
------------------------

You can use namespaces to organize your SPL code, similar to Python modules or Java&reg; packages. Any folder with an empty file called `.namespace` is treated as an SPL namespace.

Create a folder within your project with the target namespace with the following steps:
1. Select the project, right click, and click **New Folder**.
2. Enter a name for the namespace, e.g. `my.name.space`:
3. Create a new empty file within the `my.name.space` folder and call it `.namespace`. The final folder structure should look like this:
    - MyStreams project
      - `my.name.space`
        - `.namespace`
      - `info.xml`

Now that your namespace is created, you can create your first SPL source
file.

Create a main composite
--------------------------

Executable SPL applications are called main composites, and they are defined in SPL source files. These files have a `.spl` extension.

**Create a source file within a namespace**:

1. Right-click the `my.name.space` folder, right-click and choose **New File**.
2. Enter the name for the new SPL file, `Main.spl`.
3. Add the namespace declaration to the file with the following line:
    `namespace my.name.space;`

**Create a main composite**

The following code is a stub for a new main composite called `MyComposite` in the `my.name.space` namespace:

```
namespace my.name.space;

composite MyComposite {
}
```